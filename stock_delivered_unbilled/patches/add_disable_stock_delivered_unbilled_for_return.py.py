
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	create_parking_account_field()

def create_parking_account_field():
	custom_field = {
		"Company": [
			dict(
				fieldname="disable_stock_delivered_but_not_billed_in_sr",
				label="Disable Stock Delivered But Not Billed in Sales Return",
				fieldtype="Check",
				insert_after="stock_delivered_but_not_billed",
				ignore_user_permissions=1,
				no_copy=1,
			),
		]
	}
	create_custom_fields(custom_field, ignore_validate=frappe.flags.in_patch, update=True)