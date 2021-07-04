# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import Warning,UserError

class sale_order_line(models.Model):
    _inherit = "sale.order.line"
    
    sh_sale_barcode_scanner_is_last_scanned = fields.Boolean(string = "Last Scanned?")

class sale_order(models.Model):
    _name = "sale.order"
    _inherit = ["barcodes.barcode_events_mixin", "sale.order"]   
       
    
    def _add_product(self, barcode):        
        
        is_last_scanned = False
        sequence = 0
        warm_sound_code = ""   
        
        if self.env.user.company_id.sudo().sh_sale_barcode_scanner_last_scanned_color:  
            is_last_scanned = True          
        
        if self.env.user.company_id.sudo().sh_sale_barcode_scanner_move_to_top:
            sequence = -1
            
        if self.env.user.company_id.sudo().sh_sale_barcode_scanner_warn_sound:
            warm_sound_code = "SH_BARCODE_SCANNER_"      

        if self.env.user.company_id.sudo().sh_sale_barcode_scanner_auto_close_popup:
            warm_sound_code += "AUTO_CLOSE_AFTER_" + str(self.env.user.company_id.sudo().sh_sale_barcode_scanner_auto_close_popup) + "_MS&"   
        
        #step 1 make sure order in proper state.
        if self and self.state in ["cancel","done"]:
            selections = self.fields_get()["state"]["selection"]
            value = next((v[1] for v in selections if v[0] == self.state), self.state)
            raise UserError(_(warm_sound_code + "You can not scan item in %s state.") %(value))
                
        #step 2 increaset product qty by 1 if product not in order line than create new order line.
        elif self:
                             
            self.order_line.update({
                'sh_sale_barcode_scanner_is_last_scanned': False,
                'sequence': 0,
                })   
                     
            
            search_lines = False
            domain = []
            if self.env.user.company_id.sudo().sh_sale_barcode_scanner_type == "barcode":            
                search_lines = self.order_line.filtered(lambda ol: ol.product_id.barcode == barcode)
                domain = [("barcode","=",barcode)]
             
            elif self.env.user.company_id.sudo().sh_sale_barcode_scanner_type == "int_ref":            
                search_lines = self.order_line.filtered(lambda ol: ol.product_id.default_code == barcode)   
                domain = [("default_code","=",barcode)]
                 
            elif self.env.user.company_id.sudo().sh_sale_barcode_scanner_type == "sh_qr_code":            
                search_lines = self.order_line.filtered(lambda ol: ol.product_id.sh_qr_code == barcode)   
                domain = [("sh_qr_code","=",barcode)]
            
            elif self.env.user.company_id.sudo().sh_sale_barcode_scanner_type == "all":            
                search_lines = self.order_line.filtered(lambda ol: ol.product_id.barcode == barcode or 
                                                        ol.product_id.default_code == barcode or 
                                                        ol.product_id.sh_qr_code == barcode                                                        
                                                        )   
                domain = ["|","|",
                          
                    ("default_code","=",barcode),
                    ("barcode","=",barcode),
                    ("sh_qr_code","=",barcode)
                    
                ]                                            
            if search_lines:
                for line in search_lines:
                    line.product_uom_qty += 1
                    line.sh_sale_barcode_scanner_is_last_scanned = is_last_scanned
                    line.sequence = sequence                    
                    line.product_id_change()
                    
                    line._onchange_discount()                    
                    break
            else:
                search_product = self.env["product.product"].search(domain, limit = 1)
                if search_product:
                    vals = {
                        'product_id': search_product.id,
                        'name': search_product.name,
                        'product_uom': search_product.uom_id.id,
                        'product_uom_qty': 1,
                        'price_unit': search_product.lst_price,
                        'sh_sale_barcode_scanner_is_last_scanned': is_last_scanned,
                        'sequence' : sequence,                        
                    }
                    if search_product.uom_id:
                        vals.update({
                            "product_uom": search_product.uom_id.id,                            
                        })  
                                                         
                    new_order_line = self.order_line.with_context({'default_order_id':self.id}).new(vals)
                    new_order_line.product_id_change()
                    new_order_line.product_uom_change()
                    new_order_line._onchange_discount()
                    self.order_line += new_order_line                     
                else:                   
                    raise UserError(_(warm_sound_code + "Scanned Internal Reference/Barcode not exist in any product!"))                          
                
                
            
                
    def on_barcode_scanned(self, barcode):
        self._add_product(barcode)

            
                