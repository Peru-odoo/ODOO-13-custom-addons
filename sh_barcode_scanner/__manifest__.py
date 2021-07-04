# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name": "All In One Barcode Scanner-Basic | Sale Order Barcode Scanner | Purchase Order Barcode Scanner | Invoice Barcode Scanner | Inventory Barcode Scanner | Bill Of Material Barcode Scanner | Scrap Barcode Scanner | Warehouse Barcode Scanner",

    'author' : 'Softhealer Technologies',
    
    'website': 'https://www.softhealer.com',
        
    "support": "support@softhealer.com",    
        
    'version': '13.0.9',
        
    "category": "Extra Tools",

    "summary": "Barcode Scanner Package,Sales Barcode Scanner,Purchase Barcode Scanner Module,Account Barcode Scanner,Stock Barcode Scanner,BOM Barcode Scanner,Request For Quotation Barcode Scanner,Bill Barcode Scanner,PO Barcode Scanner,RFQ Barcode Scanner Odoo",   
        
    'description': """Do your time-wasting in sales, purchases, invoices, inventory, bill of material, scrap operations by manual product selection? So here are the solutions these modules useful do quick operations of sales, purchases, invoicing and inventory, bill of material, scrap using barcode scanner. You no need to select the product and do one by one. scan it and you do! So be very quick in all operations of odoo and cheers!

 All In One Barcode Scanner - Sales, Purchase, Invoice, Inventory, BOM, Scrap Odoo.
Operations Of Sales, Purchase Using Barcode, Invoice Using Barcode, Inventory Using Barcode, Bill Of Material Using Barcode, Scrap Using Barcode Module, Sales Barcode Scanner,Purchase Barcode Scanner, Invoice Barcode Scanner, Inventory Barcode Scanner,Bom Barcode Scanner, Single Product Multi Barcode Odoo.
 
 Barcode Scanner App,Package All in one barcode scanner,  Operations Of Sales, Purchase In Barcode Module, Invoice In Barcode, Inventory In Barcode, Bom In Barcode, Scrap Using Barcode, Single Product Multi Barcode, Sales Barcode Scanner,Purchase Barcode Scanner, Invoice Barcode Scanner, Inventory Barcode Scanner,Bom Barcode Scanner, Single Product Multi Barcode Odoo.


Add products by barcode    
Add products using barcode    

sales mobile barcode scanner
so barcode scanner
so mobile barcode scanner
sale mobile barcode scanner

po mobile barcode scanner
purchase order mobile barcode scanner
purchase order barcode scanner
po barcode scanner
    
inventory mobile barcode scanner    
stock mobile barcode scanner
inventory barcode scanner
stock barcode scanner

inventory adjustment mobile barcode scanner
stock adjustment mobile barcode scanner
inventory adjustment barcode scanner
stock adjustment barcode scanner

invoice barcode scanner
bill barcode scanner
credit note barcode scanner
debit note barcode scanner
invoice barcode mobile scanner
bill barcode mobile scanner
credit note barcode mobile scanner
debit note barcode mobile scanner

     """,
    
    "depends": [
        
                'purchase',
                'sale_management',
                'barcodes',
                'account',
                'stock',
                'mrp',
                'sale',
                'sh_product_qrcode_generator',
                
                ],
    
    "data": [
        
    "views/res_config_settings_views.xml",
    "views/sale_view.xml",
    "views/purchase_view.xml",
    "views/stock_view.xml",
    "views/account_view.xml",
    "views/mrp_view.xml",
    "views/assets.xml",
    
    
    ],    
    'images': ['static/description/background.png',],            
    
    "installable": True,    
    "application": True,    
    "autoinstall": False,
    "price": 35,
    "currency": "EUR"        
}
