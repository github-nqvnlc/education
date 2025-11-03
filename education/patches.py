# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See LICENSE

import frappe

def execute():
	"""Apply cookie domain sharing patches"""
	
	# Import our custom classes
	from education.auth import CustomLoginManager, setup_custom_auth
	from education.cookie_manager import CustomCookieManager
	
	# Apply the patches
	setup_custom_auth()
	
	frappe.msgprint("Cookie domain sharing has been enabled!")

