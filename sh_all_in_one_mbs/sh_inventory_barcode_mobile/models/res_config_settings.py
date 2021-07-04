# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import api, fields, models


class res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    sh_stock_barcode_mobile_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR code'),        
        ('all','All')
        ],default = 'barcode', string='Inventory Product Scan Options In Mobile',related = "company_id.sh_stock_barcode_mobile_type", translate=True, readonly = False)

    sh_stock_bm_is_cont_scan = fields.Boolean(string='Inventory Continuously Scan?',related = "company_id.sh_stock_bm_is_cont_scan", translate=True, readonly = False)
    
    sh_stock_bm_is_notify_on_success = fields.Boolean(string='Inventory Notification On Product Succeed?', related = "company_id.sh_stock_bm_is_notify_on_success",translate=True, readonly = False)
    
    sh_stock_bm_is_notify_on_fail = fields.Boolean(string='Inventory Notification On Product Failed?', related = "company_id.sh_stock_bm_is_notify_on_fail",translate=True, readonly = False)
        
    sh_stock_bm_is_sound_on_success = fields.Boolean(string='Inventory Play Sound On Product Succeed?',related = "company_id.sh_stock_bm_is_sound_on_success", translate=True, readonly = False)
    
    sh_stock_bm_is_sound_on_fail = fields.Boolean(string='Inventory Play Sound On Product Failed?', related = "company_id.sh_stock_bm_is_sound_on_fail",translate=True, readonly = False)
            
    sh_stock_bm_is_add_product = fields.Boolean(string = "Inventory Is add new product in picking?",related = "company_id.sh_stock_bm_is_add_product",translate=True, readonly = False) 



    
    
    
    
    