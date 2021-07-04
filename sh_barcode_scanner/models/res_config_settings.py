# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import api, fields, models


class res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    #sale
    sh_sale_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
         ('sh_qr_code','QR Code'),
         ('all','All'),
        ],related='company_id.sh_sale_barcode_scanner_type', string='Product Scan Options', translate=True,readonly = False)
    
    sh_sale_barcode_scanner_last_scanned_color = fields.Boolean(
        related='company_id.sh_sale_barcode_scanner_last_scanned_color', 
        string='Last scanned Color?', translate=True,readonly = False)

    sh_sale_barcode_scanner_move_to_top = fields.Boolean(
        related='company_id.sh_sale_barcode_scanner_move_to_top', 
        string='Last scanned Move To Top?', translate=True,readonly = False)

    sh_sale_barcode_scanner_warn_sound = fields.Boolean(
        related='company_id.sh_sale_barcode_scanner_warn_sound', 
        string='Warning Sound?', translate=True,readonly = False)
    
    sh_sale_barcode_scanner_auto_close_popup = fields.Integer(
        related='company_id.sh_sale_barcode_scanner_auto_close_popup', 
        string='Auto close alert/error message after', translate=True,readonly = False)
        
        
    #purchase
    sh_purchase_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
         ('sh_qr_code','QR Code'),
         ('all','All'),
        ],related='company_id.sh_purchase_barcode_scanner_type', string='Product Scan Options', translate=True, readonly = False)

    sh_purchase_barcode_scanner_last_scanned_color = fields.Boolean(
        related='company_id.sh_purchase_barcode_scanner_last_scanned_color', 
        string='Last scanned Color?', translate=True,readonly = False)

    sh_purchase_barcode_scanner_move_to_top = fields.Boolean(
        related='company_id.sh_purchase_barcode_scanner_move_to_top', 
        string='Last scanned Move To Top?', translate=True,readonly = False)

    sh_purchase_barcode_scanner_warn_sound = fields.Boolean(
        related='company_id.sh_purchase_barcode_scanner_warn_sound', 
        string='Warning Sound?', translate=True,readonly = False)    
    
    
    sh_purchase_barcode_scanner_auto_close_popup = fields.Integer(
        related='company_id.sh_purchase_barcode_scanner_auto_close_popup', 
        string='Auto close alert/error message after', translate=True,readonly = False)    
    
    
    #stock picking
    sh_inventory_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
         ('sh_qr_code','QR Code'),
         ('all','All'),
        ],related='company_id.sh_inventory_barcode_scanner_type', string='Product Scan Options', translate=True,readonly = False)
    
    sh_inventory_barcode_scanner_is_add_product = fields.Boolean(
            related = "company_id.sh_inventory_barcode_scanner_is_add_product",
            string = "Is add new product in picking?",
            translate = True,
            readonly = False)
    
    sh_inventory_barcode_scanner_last_scanned_color = fields.Boolean(
        related='company_id.sh_inventory_barcode_scanner_last_scanned_color', 
        string='Last scanned Color?', translate=True,readonly = False)

    sh_inventory_barcode_scanner_move_to_top = fields.Boolean(
        related='company_id.sh_inventory_barcode_scanner_move_to_top', 
        string='Last scanned Move To Top?', translate=True,readonly = False)

    sh_inventory_barcode_scanner_warn_sound = fields.Boolean(
        related='company_id.sh_inventory_barcode_scanner_warn_sound', 
        string='Warning Sound?', translate=True,readonly = False)     
    
    sh_inventory_barcode_scanner_auto_close_popup = fields.Integer(
        related='company_id.sh_inventory_barcode_scanner_auto_close_popup', 
        string='Auto close alert/error message after', translate=True,readonly = False)       
    
     
     
    
    
    #invoice
    sh_invoice_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
         ('sh_qr_code','QR Code'),
         ('all','All'),
        ],related='company_id.sh_invoice_barcode_scanner_type', string='Product Scan Options', translate=True,readonly = False)
  
      
      
    sh_invoice_barcode_scanner_last_scanned_color = fields.Boolean(
        related='company_id.sh_invoice_barcode_scanner_last_scanned_color', 
        string='Last scanned Color?', translate=True,readonly = False)
  
    sh_invoice_barcode_scanner_move_to_top = fields.Boolean(
        related='company_id.sh_invoice_barcode_scanner_move_to_top', 
        string='Last scanned Move To Top?', translate=True,readonly = False)
  
    sh_invoice_barcode_scanner_warn_sound = fields.Boolean(
        related='company_id.sh_invoice_barcode_scanner_warn_sound', 
        string='Warning Sound?', translate=True,readonly = False)    
      
    sh_invoice_barcode_scanner_auto_close_popup = fields.Integer(
        related='company_id.sh_invoice_barcode_scanner_auto_close_popup', 
        string='Auto close alert/error message after', translate=True,readonly = False)       
     
    
    #BOM
    sh_bom_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
         ('sh_qr_code','QR Code'),
         ('all','All'),
        ],related='company_id.sh_bom_barcode_scanner_type', string='Product Scan Options', translate=True,readonly = False)

    sh_bom_barcode_scanner_last_scanned_color = fields.Boolean(
        related='company_id.sh_bom_barcode_scanner_last_scanned_color', 
        string='Last scanned Color?', translate=True,readonly = False)

    sh_bom_barcode_scanner_move_to_top = fields.Boolean(
        related='company_id.sh_bom_barcode_scanner_move_to_top', 
        string='Last scanned Move To Top?', translate=True,readonly = False)

    sh_bom_barcode_scanner_warn_sound = fields.Boolean(
        related='company_id.sh_bom_barcode_scanner_warn_sound', 
        string='Warning Sound?', translate=True,readonly = False) 
    
    sh_bom_barcode_scanner_auto_close_popup = fields.Integer(
        related='company_id.sh_bom_barcode_scanner_auto_close_popup', 
        string='Auto close alert/error message after', translate=True,readonly = False)           
    
    
    
   
   
    
    # inventory adjustment
    sh_inven_adjt_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
         ('sh_qr_code','QR Code'),
         ('all','All'),
        ],related='company_id.sh_inven_adjt_barcode_scanner_type', string='Product Scan Options', translate=True,readonly = False)
    
    sh_inven_adjt_barcode_scanner_last_scanned_color = fields.Boolean(
        string='Last scanned Color?', 
        related='company_id.sh_inven_adjt_barcode_scanner_last_scanned_color',
        translate=True,readonly = False)

    sh_inven_adjt_barcode_scanner_move_to_top = fields.Boolean(
        string='Last scanned Move To Top?', 
        related='company_id.sh_inven_adjt_barcode_scanner_move_to_top',
        translate=True,readonly = False)

    sh_inven_adjt_barcode_scanner_warn_sound = fields.Boolean(
        string='Warning Sound?', 
        related='company_id.sh_inven_adjt_barcode_scanner_warn_sound',
        translate=True,readonly = False)      
    
    
    sh_inven_adjt_barcode_scanner_auto_close_popup = fields.Integer(
        related='company_id.sh_inven_adjt_barcode_scanner_auto_close_popup', 
        string='Auto close alert/error message after', translate=True,readonly = False)     
   
    
    #scrap barcode
    sh_scrap_barcode_scanner_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
         ('sh_qr_code','QR Code'),
         ('all','All'),
        ],related='company_id.sh_scrap_barcode_scanner_type', string='Product Scan Options', translate=True,readonly = False)
    

# TODO: Fix in v13 sound issue while warning    
#     sh_scrap_barcode_scanner_warn_sound = fields.Boolean(
#         string='Warning Sound?', 
#         related='company_id.sh_scrap_barcode_scanner_warn_sound',
#         translate=True,readonly = False)   
#     
#     sh_scrap_barcode_scanner_auto_close_popup = fields.Integer(
#         related='company_id.sh_scrap_barcode_scanner_auto_close_popup', 
#         string='Auto close alert/error message after', translate=True,readonly = False)       
  
    
        
    
    