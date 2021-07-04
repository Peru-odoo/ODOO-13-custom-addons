# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class res_company(models.Model):
    _inherit = "res.company"

    sh_stock_barcode_mobile_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR code'),        
        ('all','All')
        ],default = 'barcode', string='Inventory Product Scan Options In Mobile', translate=True)

    sh_stock_bm_is_cont_scan = fields.Boolean(string='Inventory Continuously Scan?', translate=True)
    
    sh_stock_bm_is_notify_on_success = fields.Boolean(string='Inventory Notification On Product Succeed?', translate=True)
    
    sh_stock_bm_is_notify_on_fail = fields.Boolean(string='Inventory Notification On Product Failed?', translate=True)
        
    sh_stock_bm_is_sound_on_success = fields.Boolean(string='Inventory Play Sound On Product Succeed?', translate=True)
    
    sh_stock_bm_is_sound_on_fail = fields.Boolean(string='Inventory Play Sound On Product Failed?', translate=True)
            
    sh_stock_bm_is_add_product = fields.Boolean(string = "Inventory Is add new product in picking?",translate=True) 



