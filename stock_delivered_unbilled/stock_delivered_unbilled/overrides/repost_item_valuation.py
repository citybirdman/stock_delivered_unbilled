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


def repost_invoice_entries():
	"""
	Pick and repost the invoices listed in Repost Sales Invoice List.
	"""

	riv_entries = frappe.db.get_all(
		"Repost Sales Invoice",
		filters={"completed": 0},
		fields=["repost_item_valuation", "affected_sales_invoice", "name"],
	)

	for row in riv_entries:
		voucher_obj = frappe.get_doc("Sales Invoice", row.affected_sales_invoice)
		expected_gle = toggle_debit_credit_if_negative(voucher_obj.get_gl_entries())
		_delete_accounting_ledger_entries("Sales Invoice", row.affected_sales_invoice)
		voucher_obj.make_gl_entries(gl_entries=expected_gle, from_repost=True)
		frappe.db.commit()
		frappe.db.set_value('Repost Sales Invoice', row.name, 'completed', 1)
		
	return

def validate_expense_accoount(self,method):
	stock_delivered_but_not_billed_account = None
	stock_delivered_but_not_billed_account = frappe.db.get_value("Company", self.company, "stock_delivered_but_not_billed")


	disable_sdbnb_in_sr = frappe.db.get_value("Company", self.company, "disable_sdbnb_in_sr")
	default_expense_account = frappe.db.get_value("Company", self.company, "default_expense_account")

	if stock_delivered_but_not_billed_account:
		if disable_sdbnb_in_sr and self.is_return:
			if default_expense_account:
				for item in self.items:
					item.expense_account = default_expense_account
		else:
			for item in self.items:
				item.expense_account = stock_delivered_but_not_billed_account