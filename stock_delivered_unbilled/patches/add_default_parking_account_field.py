
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	create_parking_account_field()

def create_parking_account_field():
	print("In the Patch")
	custom_field = {
		"Company": [
			dict(
				fieldname="stock_delivered_but_not_billed",
				label="Stock Delivered But Not Billed",
				fieldtype="Link",
				options="Account",
				insert_after="stock_received_but_not_billed",
				ignore_user_permissions=1,
				no_copy=1,
			)
		]
	}
	create_custom_fields(custom_field, ignore_validate=frappe.flags.in_patch, update=True)