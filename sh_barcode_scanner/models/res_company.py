# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class res_company(models.Model):
    _inherit = "res.company"

    #sale
    sh_sale_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR Code'),
        ('all','All'),
        ],default = 'barcode' ,string='Product Scan Options (sale)', translate=True)
    
    
    sh_sale_barcode_scanner_last_scanned_color = fields.Boolean(
        string='Last scanned Color? (sale)', translate=True)

    sh_sale_barcode_scanner_move_to_top = fields.Boolean(
        string='Last scanned Move To Top? (sale)', translate=True)

    sh_sale_barcode_scanner_warn_sound = fields.Boolean(
        string='Warning Sound? (sale)', translate=True)
    
    sh_sale_barcode_scanner_auto_close_popup = fields.Integer(
        string='Auto close alert/error message after (sale)', translate=True)

    #purchase
    sh_purchase_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR Code'),
        ('all','All'),
        ],default = 'barcode' ,string='Product Scan Options (Purchase)', translate=True)
    
    sh_purchase_barcode_scanner_last_scanned_color = fields.Boolean(
        string='Last scanned Color? (Purchase)', translate=True)

    sh_purchase_barcode_scanner_move_to_top = fields.Boolean(
        string='Last scanned Move To Top? (Purchase)', translate=True)

    sh_purchase_barcode_scanner_warn_sound = fields.Boolean(
        string='Warning Sound? (Purchase)', translate=True)    
    
    sh_purchase_barcode_scanner_auto_close_popup = fields.Integer(
        string='Auto close alert/error message after (Purchase)', translate=True)   
    
        

    #stock picking
    sh_inventory_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR Code'),
        ('all','All'),
        ],default = 'barcode' ,string='Product Scan Options (Picking)', translate=True)

    sh_inventory_barcode_scanner_is_add_product = fields.Boolean(string = "Is add new product in picking?",translate=True) 


    sh_inventory_barcode_scanner_last_scanned_color = fields.Boolean(
        string='Last scanned Color? (Picking)', translate=True)

    sh_inventory_barcode_scanner_move_to_top = fields.Boolean(
        string='Last scanned Move To Top? (Picking)', translate=True)

    sh_inventory_barcode_scanner_warn_sound = fields.Boolean(
        string='Warning Sound? (Picking)', translate=True)  
    
    
    sh_inventory_barcode_scanner_auto_close_popup = fields.Integer(
        string='Auto close alert/error message after (Picking)', translate=True)      
    
               
    
    #invoice
    sh_invoice_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR Code'),
        ('all','All'),
        ],default = 'barcode' ,string='Product Scan Options (Invoice)', translate=True)
      
    sh_invoice_barcode_scanner_last_scanned_color = fields.Boolean(
        string='Last scanned Color? (Invoice)', translate=True,readonly = False)
  
    sh_invoice_barcode_scanner_move_to_top = fields.Boolean(
        string='Last scanned Move To Top? (Invoice)', translate=True,readonly = False)
  
    sh_invoice_barcode_scanner_warn_sound = fields.Boolean(
        string='Warning Sound? (Invoice)', translate=True,readonly = False)      
      
    sh_invoice_barcode_scanner_auto_close_popup = fields.Integer(
        string='Auto close alert/error message after (Invoice)', translate=True,readonly = False)        
     
     
    
    

    #BOM
    sh_bom_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR Code'),
        ('all','All'),
        ],default = 'barcode' ,string='Product Scan Options (BOM)', translate=True)
    
    sh_bom_barcode_scanner_last_scanned_color = fields.Boolean(
        string='Last scanned Color? (BOM)', translate=True,readonly = False)

    sh_bom_barcode_scanner_move_to_top = fields.Boolean(
        string='Last scanned Move To Top? (BOM)', translate=True,readonly = False)

    sh_bom_barcode_scanner_warn_sound = fields.Boolean(
        string='Warning Sound? (BOM)', translate=True,readonly = False)     
    

    sh_bom_barcode_scanner_auto_close_popup = fields.Integer(
        string='Auto close alert/error message after (BOM)', translate=True,readonly = False)   

    
    
    #inventory adjustment
    sh_inven_adjt_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR Code'),
        ('all','All'),
        ],default = 'barcode' ,string='Product Scan Options', translate=True)
    
    
    sh_inven_adjt_barcode_scanner_last_scanned_color = fields.Boolean(
        string='Last scanned Color?', translate=True)

    sh_inven_adjt_barcode_scanner_move_to_top = fields.Boolean(
        string='Last scanned Move To Top?', translate=True)

    sh_inven_adjt_barcode_scanner_warn_sound = fields.Boolean(
        string='Warning Sound?', translate=True)  
    
        
    sh_inven_adjt_barcode_scanner_auto_close_popup = fields.Integer(
        string='Auto close alert/error message after', translate=True)       
    
    
        
    
    
    
    #scrap
    sh_scrap_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR Code'),
        ('all','All'),
        ],default = 'barcode', string='Product Scan Options (Scrap)', translate=True)
 
# TODO: Fix in v13 sound issue while warning    
#     sh_scrap_barcode_scanner_warn_sound = fields.Boolean(
#         string='Warning Sound? (Scrap)', translate=True,readonly = False)      
#      
#     sh_scrap_barcode_scanner_auto_close_popup = fields.Integer(
#         string='Auto close alert/error message after (Scrap)', translate=True,readonly = False)  
