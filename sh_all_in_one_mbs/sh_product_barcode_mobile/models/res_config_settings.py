# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import api, fields, models


class res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_product_barcode_mobile_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR code'),        
        ('all','All')
        ],related='company_id.sh_product_barcode_mobile_type', string='Product Scan Options In Mobile', translate=True,readonly = False)


    sh_product_bm_is_cont_scan = fields.Boolean(related='company_id.sh_product_bm_is_cont_scan', string='Product Continuously Scan?', translate=True,readonly = False)
    
    sh_product_bm_is_notify_on_success = fields.Boolean(related='company_id.sh_product_bm_is_notify_on_success',string='Product Notification On Product Succeed?', translate=True,readonly = False)
    
    sh_product_bm_is_notify_on_fail = fields.Boolean(related='company_id.sh_product_bm_is_notify_on_fail',string='Product Notification On Product Failed?', translate=True,readonly = False)
    
    sh_product_bm_is_sound_on_success = fields.Boolean(related='company_id.sh_product_bm_is_sound_on_success', string='Product Play Sound On Product Succeed?', translate=True, readonly = False)
    
    sh_product_bm_is_sound_on_fail = fields.Boolean(related='company_id.sh_product_bm_is_sound_on_fail', string='Product Play Sound On Product Failed?', translate=True, readonly = False)
        



    sh_product_bm_is_default_code = fields.Boolean(related='company_id.sh_product_bm_is_default_code', string='Show Internal Reference?', translate=True, readonly = False)
                
    sh_product_bm_is_lst_price = fields.Boolean(related='company_id.sh_product_bm_is_lst_price', string='Show Sale Price?', translate=True, readonly = False)
    
    sh_product_bm_is_qty_available = fields.Boolean(related='company_id.sh_product_bm_is_qty_available', string='Show Quantity On Hand?', translate=True, readonly = False)
    
    sh_product_bm_is_virtual_available = fields.Boolean(related='company_id.sh_product_bm_is_virtual_available', string='Show Forecast Quantity?', translate=True, readonly = False)
    