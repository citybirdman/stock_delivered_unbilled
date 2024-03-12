import frappe
from frappe import _
from erpnext.stock.doctype.repost_item_valuation.repost_item_valuation import (
	repost_sl_entries, 
	repost_gl_entries, 
	notify_error_to_stock_managers, 
	_get_directly_dependent_vouchers,
	in_configured_timeslot
)
from frappe.utils import cint, get_link_to_form, get_weekday, getdate, now, nowtime
from erpnext.accounts.general_ledger import toggle_debit_credit_if_negative
from erpnext.accounts.utils import get_future_stock_vouchers, repost_gle_for_stock_vouchers, _delete_accounting_ledger_entries
from erpnext.stock.stock_ledger import (
	get_affected_transactions,
	get_items_to_be_repost,
	repost_future_sle,
)

from rq.timeouts import JobTimeoutException
from frappe.exceptions import QueryDeadlockError, QueryTimeoutError

RecoverableErrors = (JobTimeoutException, QueryDeadlockError, QueryTimeoutError)


def queue_affected_sales_invoices():
	"""
	This will collect all the affected delivery notes from "Repost Item Valuation"
	and adds the associated sales invoice to the "Repost Sales Invoice" list.
	"""

	riv_entries = frappe.db.sql(
		""" SELECT name from `tabRepost Item Valuation`
		WHERE status in ('Completed') and creation <= %s and docstatus = 1 and modified > now() - interval 36 hour
		ORDER BY timestamp(posting_date, posting_time) asc, creation asc, status asc
		""",
		now(),
		as_dict=1,
		)

	for row in riv_entries:
		doc = frappe.get_doc("Repost Item Valuation", row.name)
		if doc.status in ("Completed"):
			try:
				_queue_affected_sales_invoices(doc)

			except Exception as e:
				frappe.db.rollback()
				traceback = frappe.get_traceback()
				doc.log_error("Unable to fetch affected invoices")
			finally:
				if not frappe.flags.in_test:
					frappe.db.commit()
	return

def _queue_affected_sales_invoices(doc):
	directly_dependent_transactions = _get_directly_dependent_vouchers(doc)
	repost_affected_transaction = get_affected_transactions(doc)
	all_affected_transactions = directly_dependent_transactions + list(repost_affected_transaction)
	affected_invoices = []
	for affected_transaction in all_affected_transactions:
		document_type, document_name = affected_transaction
		if document_type == "Delivery Note":
			invoice_list = frappe.get_all("Sales Invoice Item", fields=["name", "parent"], filters={"delivery_note": document_name})
			for invoice in invoice_list:
				docstatus = frappe.db.get_value("Sales Invoice", invoice.parent, "docstatus")
				if docstatus == 1:
					affected_invoices.append(invoice.parent)

	for inv in affected_invoices:
		if not frappe.db.exists(
			"Repost Sales Invoice", {"repost_item_valuation": doc.name, "affected_sales_invoice": inv}):
			rsi = frappe.new_doc("Repost Sales Invoice")
			rsi.repost_item_valuation = doc.name
			rsi.affected_sales_invoice = inv
			rsi.completed = 0
			rsi.insert(ignore_permissions=True)
			

