
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	create_parking_account_field()
	create_disable_in_return_field()

def create_parking_account_field():
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

def create_disable_in_return_field():
	custom_field = {
		"Company": [
			dict(
				fieldname="disable_sdbnb_in_sr",
				label="Disable Stock Delivered But Not Billed in Sales Return",
				fieldtype="Check",
				insert_after="stock_delivered_but_not_billed",
				ignore_user_permissions=1,
				no_copy=1,
			),
		]
	}
	create_custom_fields(custom_field, ignore_validate=frappe.flags.in_patch, update=True)