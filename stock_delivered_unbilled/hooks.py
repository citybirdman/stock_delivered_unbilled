app_name = "stock_delivered_unbilled"
app_title = "Stock Delivered Unbilled"
app_publisher = "Aerele Technologies Private Limited"
app_description = "This app enables the parking account for Stock Delivered But Not Billed"
app_email = "hello@aerele.in"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/stock_delivered_unbilled/css/stock_delivered_unbilled.css"
# app_include_js = "/assets/stock_delivered_unbilled/js/stock_delivered_unbilled.js"

# include js, css files in header of web template
# web_include_css = "/assets/stock_delivered_unbilled/css/stock_delivered_unbilled.css"
# web_include_js = "/assets/stock_delivered_unbilled/js/stock_delivered_unbilled.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "stock_delivered_unbilled/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "stock_delivered_unbilled/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "stock_delivered_unbilled.utils.jinja_methods",
#	"filters": "stock_delivered_unbilled.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "stock_delivered_unbilled.install.before_install"
after_install = "stock_delivered_unbilled.patches.add_default_parking_account_field.execute"

# Uninstallation
# ------------

# before_uninstall = "stock_delivered_unbilled.uninstall.before_uninstall"
# after_uninstall = "stock_delivered_unbilled.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "stock_delivered_unbilled.utils.before_app_install"
# after_app_install = "stock_delivered_unbilled.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "stock_delivered_unbilled.utils.before_app_uninstall"
# after_app_uninstall = "stock_delivered_unbilled.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "stock_delivered_unbilled.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Sales Invoice": "stock_delivered_unbilled.stock_delivered_unbilled.overrides.sales_invoice.CustomSalesInvoice",
	"Delivery Note": "stock_delivered_unbilled.stock_delivered_unbilled.overrides.delivery_note.CustomDeliveryNote"
}

from erpnext.stock import get_item_details as original_get_item_details
from stock_delivered_unbilled.stock_delivered_unbilled.overrides import get_basic_details as overridden_get_basic_details
original_get_item_details.get_basic_details = overridden_get_basic_details.get_basic_details


from erpnext.stock.doctype.repost_item_valuation import repost_item_valuation as original_repost_item_valuation
from stock_delivered_unbilled.stock_delivered_unbilled.overrides import repost_item_valuation as overridden_repost_item_valuation
original_repost_item_valuation.repost = overridden_repost_item_valuation.repost

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"stock_delivered_unbilled.tasks.all"
#	],
#	"daily": [
#		"stock_delivered_unbilled.tasks.daily"
#	],
#	"hourly": [
#		"stock_delivered_unbilled.tasks.hourly"
#	],
#	"weekly": [
#		"stock_delivered_unbilled.tasks.weekly"
#	],
#	"monthly": [
#		"stock_delivered_unbilled.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "stock_delivered_unbilled.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "stock_delivered_unbilled.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "stock_delivered_unbilled.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["stock_delivered_unbilled.utils.before_request"]
# after_request = ["stock_delivered_unbilled.utils.after_request"]

# Job Events
# ----------
# before_job = ["stock_delivered_unbilled.utils.before_job"]
# after_job = ["stock_delivered_unbilled.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"stock_delivered_unbilled.auth.validate"
# ]
