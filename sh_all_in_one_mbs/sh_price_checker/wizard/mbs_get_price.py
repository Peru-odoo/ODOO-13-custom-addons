# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.


from odoo import api, fields, models, _
from odoo.exceptions import UserError


class mbs_get_price(models.TransientModel):
    _name = "mbs.get.price"
    _description = "Get Price Mobile Barcode Scanner"

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
        
    post_msg = fields.Html(
        'Message', translate=True,
        help='Message displayed after having scan product')    
    
    def default_sh_price_checker_bm_is_cont_scan(self):
        if self.env.user and self.env.user.company_id:
            return self.env.user.company_id.sh_price_checker_bm_is_cont_scan
    
    sh_price_checker_barcode_mobile = fields.Char(string = "Mobile Barcode")
    
    sh_price_checker_bm_is_cont_scan = fields.Char(string='Continuously Scan?',default = default_sh_price_checker_bm_is_cont_scan, readonly=True)
    
        
    
    @api.onchange('sh_price_checker_barcode_mobile')
    def _onchange_sh_price_checker_barcode_mobile(self):
        
        if self.sh_price_checker_barcode_mobile in ['',"",False,None]:
            return
        
        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""
        if self.env.user.company_id.sudo().sh_price_checker_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"
        
        if self.env.user.company_id.sudo().sh_price_checker_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"       
            
            
                 
        if self and self.sh_price_checker_barcode_mobile:          
            domain = []
            if self.env.user.company_id.sudo().sh_price_checker_barcode_mobile_type == "barcode":            
                domain = [("barcode","=",self.sh_price_checker_barcode_mobile)]
              
            elif self.env.user.company_id.sudo().sh_price_checker_barcode_mobile_type == "int_ref":              
                domain = [("default_code","=",self.sh_price_checker_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_price_checker_barcode_mobile_type == "sh_qr_code":              
                domain = [("sh_qr_code","=",self.sh_price_checker_barcode_mobile)]
                                  
            elif self.env.user.company_id.sudo().sh_price_checker_barcode_mobile_type == "all":            
                domain = ["|","|",
                    ("default_code","=",self.sh_price_checker_barcode_mobile),
                    ("barcode","=",self.sh_price_checker_barcode_mobile),
                    ("sh_qr_code","=",self.sh_price_checker_barcode_mobile)                
                ]                                            


            search_product = self.env["product.product"].search(domain, limit = 1)
            if search_product:
                
                
                self.post_msg = _('''<div><h4>
        <span>Product: %(product)s</span> <br/><br/>
        Price: <font color="red">%(price)s </font>
        </div></h4>''') % {
                    'product': search_product.display_name,
                    'price': search_product.lst_price,
                }                
                
                
                if self.env.user.company_id.sudo().sh_price_checker_bm_is_notify_on_success:
                    message = _(CODE_SOUND_SUCCESS + 'Product: %s Price: %s') % (search_product.display_name,search_product.lst_price)                        
                    self.env['bus.bus'].sendone(
                        (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                        {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})                
                
                  
            else:
                if self.env.user.company_id.sudo().sh_price_checker_bm_is_notify_on_fail:    
                    message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')                  
                    self.env['bus.bus'].sendone(
                        (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                        {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True}) 
                 
                