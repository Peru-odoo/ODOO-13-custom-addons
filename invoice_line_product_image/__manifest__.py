# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
	'name': "AadPlus Invoice Reporting",
	'version': "13.0.0.0",
	'category': "Accounting",
	'summary': "Display product image on invoice line print product image on invoice report print image on invoice line product image print product image on invoice line product image in invoice line print Product image on vendor bill line",
	'description': """
						
			Display product image on invoice/vendor bill line. It will also display product image on invoice/vendor bill report. 
			
			Product Image On Invoice/Vendor Bill Line in odoo,
			Invoice/Vendor bill report with product image in odoo,
			Product image on invoice/vendor bill line and invoice/vendor bill report in odoo,
			Identify product via image in odoo,
			Identify priduct via image on invoice/vendor bill report in odoo,

	""",
	'author': "BrowseInfo",
	"website" : "https://www.browseinfo.in",
    'depends': ['base', 'account' , 'base_setup'],
	'data': [
			'report/invoice_report.xml',
			'views/view_invoice.xml',
			'views/res_config_settings_views.xml',
			],
	'demo': [],
	'installable': True,
	'auto_install': False,
	'application': True,
	"live_test_url":'https://youtu.be/mOq1yluwBTc',
	 "images":['static/description/Banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
