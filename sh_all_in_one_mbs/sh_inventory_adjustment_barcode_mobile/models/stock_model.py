# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError

class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"
        
    
    sequence = fields.Integer(string='Sequence', default=0)
    sh_inventory_adjt_barcode_mobile_is_last_scanned = fields.Boolean(string = "Last Scanned?")  
    
class StockInventory(models.Model):
    _name = "stock.inventory"
    _inherit = ['barcodes.barcode_events_mixin', 'stock.inventory']
    
   
    
   
   
    def sh_inventory_adjt_barcode_mobile_get_inventory_lines_values(self,product_id):
        # TDE CLEANME: is sql really necessary ? I don't think so
        locations = self.env['stock.location']
        if self.location_ids:
            locations = self.env['stock.location'].search([('id', 'child_of', self.location_ids.ids)])
        else:
            locations = self.env['stock.location'].search([('company_id', '=', self.company_id.id), ('usage', 'in', ['internal', 'transit'])])
        domain = ' sq.location_id in %s AND sq.quantity != 0 AND pp.active'
        args = (tuple(locations.ids),)

        vals = []
        Product = self.env['product.product']
        # Empty recordset of products available in stock_quants
        quant_products = self.env['product.product']

        # If inventory by company
        if self.company_id:
            domain += ' AND sq.company_id = %s'
            args += (self.company_id.id,)
        
        # ==============================
        # softhealer custom code        
        
        if product_id:
            domain += ' AND sq.product_id in %s'
            args += (tuple(  [product_id] ),)

        # ==============================
        # softhealer custom code
            
            

        self.env['stock.quant'].flush(['company_id', 'product_id', 'quantity', 'location_id', 'lot_id', 'package_id', 'owner_id'])
        self.env['product.product'].flush(['active'])
        self.env.cr.execute("""SELECT sq.product_id, sum(sq.quantity) as product_qty, sq.location_id, sq.lot_id as prod_lot_id, sq.package_id, sq.owner_id as partner_id
            FROM stock_quant sq
            LEFT JOIN product_product pp
            ON pp.id = sq.product_id
            WHERE %s
            GROUP BY sq.product_id, sq.location_id, sq.lot_id, sq.package_id, sq.owner_id """ % domain, args)

        for product_data in self.env.cr.dictfetchall():
            product_data['company_id'] = self.company_id.id
            product_data['inventory_id'] = self.id
            
            
            # ==============================
            # softhealer custom code
            product_data['sh_inventory_adjt_barcode_mobile_is_last_scanned'] = True
            product_data['sequence'] = -1
            # ==============================
            # softhealer custom code
            
                                                
            # replace the None the dictionary by False, because falsy values are tested later on
            for void_field in [item[0] for item in product_data.items() if item[1] is None]:
                product_data[void_field] = False
            product_data['theoretical_qty'] = product_data['product_qty']
            if self.prefill_counted_quantity == 'zero':
                product_data['product_qty'] = 0
            if product_data['product_id']:
                product_data['product_uom_id'] = Product.browse(product_data['product_id']).uom_id.id
                quant_products |= Product.browse(product_data['product_id'])
            vals.append(product_data)
        return vals   
   
   
   
   
   
   
   
   
   
   
   
   
    def default_sh_inventory_adjt_bm_is_cont_scan(self):
        if self.env.user and self.env.user.company_id:
            return self.env.user.company_id.sh_inventory_adjt_bm_is_cont_scan
    
    sh_inventory_adjt_barcode_mobile = fields.Char(string = "Mobile Barcode")
    
    sh_inventory_adjt_bm_is_cont_scan = fields.Char(string='Continuously Scan?',default = default_sh_inventory_adjt_bm_is_cont_scan, readonly=True)
        
 
       
   
   
    def action_start_sh_inventory_adjust_barcode_scanning(self):
        self.ensure_one()
        action_tree = self.action_start()  
        action = {
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('stock.view_inventory_form').id, 'form')],
            'view_mode': 'form',
            'res_id':self.id,
            'name': _(self.name or 'Inventory'),
            'res_model': 'stock.inventory',
            'target':'current',
        }
        action['context'] = action_tree.get('context',{})
        action['domain'] = action_tree.get('domain',[])
        return action          
    
                           






    @api.onchange('sh_inventory_adjt_barcode_mobile')
    def _onchange_sh_inventory_adjt_barcode_mobile(self):
        
        
        if self.sh_inventory_adjt_barcode_mobile in ['',"",False,None]:
            return
        
        domain = []
        
        
        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""
        if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"
        
        if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"
                    
        #step 1: state validation.
        if self and self.state != 'confirm':
            selections = self.fields_get()['state']['selection']
            value = next((v[1] for v in selections if v[0] == self.state), self.state)
            
            if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL + 'You can not scan item in %s state.')% (value)
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                
            return
        
        elif self and self.sh_inventory_adjt_barcode_mobile:
                
            self.line_ids.update({
                'sh_inventory_adjt_barcode_mobile_is_last_scanned': False,
                'sequence': 0,
                })   
                                                       
            search_lines = False
                        
            if self.env.user.company_id.sudo().sh_inventory_adjt_barcode_mobile_type == 'barcode':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.barcode == self.sh_inventory_adjt_barcode_mobile)
                domain = [("barcode","=",self.sh_inventory_adjt_barcode_mobile)]
            
            elif self.env.user.company_id.sudo().sh_inventory_adjt_barcode_mobile_type == 'int_ref':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.default_code == self.sh_inventory_adjt_barcode_mobile)
                domain = [("default_code","=",self.sh_inventory_adjt_barcode_mobile)]
                            
            
            elif self.env.user.company_id.sudo().sh_inventory_adjt_barcode_mobile_type == 'sh_qr_code':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.sh_qr_code == self.sh_inventory_adjt_barcode_mobile)
                domain = [("sh_qr_code","=",self.sh_inventory_adjt_barcode_mobile)]                
                
            elif self.env.user.company_id.sudo().sh_inventory_adjt_barcode_mobile_type == 'all':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.barcode == self.sh_inventory_adjt_barcode_mobile 
                                                      or l.product_id.default_code == self.sh_inventory_adjt_barcode_mobile
                                                      or l.product_id.sh_qr_code == self.sh_inventory_adjt_barcode_mobile)

            
                domain = ["|","|",
                    ("default_code","=",self.sh_inventory_adjt_barcode_mobile),
                    ("barcode","=",self.sh_inventory_adjt_barcode_mobile),
                    ("sh_qr_code","=",self.sh_inventory_adjt_barcode_mobile),                    
                ]  
                                
            if search_lines:
                for line in search_lines:
                    line.product_qty += 1
                    line.sh_inventory_adjt_barcode_mobile_is_last_scanned = True,
                    line.sequence = -1   
                    
                    if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_success:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (line.product_id.name,line.product_qty)                        
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                                            
                                     
                    break
            else:
                # =========================================
                # Create Inventory Line Here
                
                product = self.env['product.product'].search(domain,limit = 1)
                       
                if product:
                    lines_vals = self.sh_inventory_adjt_barcode_mobile_get_inventory_lines_values(product.id)
                    
                    # add sequence and last scanned here
                    if len(lines_vals) == 1:
                        lines_vals[0].update({
                            "product_qty": 1
                            })
                        
                        
                    if not lines_vals:                        
                        if self.location_ids:
                            lines_vals = [{
                            
                                'product_id': product.id, 
                                'product_qty': 1, 
                                'location_id': self.location_ids[0].ids[0], 
                                'prod_lot_id': False, 
                                'package_id': False, 
                                'partner_id': False, 
                                'inventory_id':self.id,
                                'sh_inventory_adjt_barcode_mobile_is_last_scanned': True, 
                                'sequence': -1, 
                                'product_uom_id': product.uom_id.id if product.uom_id else False,
                            
                            }]
                        else:                                            
                            if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_fail:    
                                message = _(CODE_SOUND_FAIL + 'Please specify at least one location in inventory')                  
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})                        
                                
                            return 
                        
                    
                    self.env['stock.inventory.line'].create( lines_vals )    
                    
                    
                                                        
                    message = _(CODE_SOUND_SUCCESS + 'Product: %s') % (product.name)                        
                    
                    if len(lines_vals) == 1:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (product.name, 1 )                     
                    
                    if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_success:
#                         message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (product.name, 1 )                       
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                                                
                else:    
                    if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_fail:    
                        message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')                  
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                    return
                   
                   

               












    def action_sh_scan_inventory_adjt_tree(self,barcode):
        
        if barcode in ['',"",False,None]:
            return
        
        domain = []
        
        
        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""

        if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"
         
        if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"
                    
        #step 1: state validation.
        if self and self.state != 'confirm':
            selections = self.fields_get()['state']['selection']
            value = next((v[1] for v in selections if v[0] == self.state), self.state)
             
            if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL + 'You can not scan item in %s state.')% (value)
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                 
            return
        
        elif self and barcode:
                
#             self.line_ids.update({
#                 'sh_inventory_adjt_barcode_mobile_is_last_scanned': False,
#                 'sequence': 0,
#                 })   
                                                       
            search_lines = False
                        
            if self.env.user.company_id.sudo().sh_inventory_adjt_barcode_mobile_type == 'barcode':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.barcode == barcode)
                domain = [("barcode","=",barcode)]
            
            elif self.env.user.company_id.sudo().sh_inventory_adjt_barcode_mobile_type == 'int_ref':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.default_code == barcode)
                domain = [("default_code","=",barcode)]
                            
            
            elif self.env.user.company_id.sudo().sh_inventory_adjt_barcode_mobile_type == 'sh_qr_code':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.sh_qr_code == barcode)
                domain = [("sh_qr_code","=",barcode)]                
                
            elif self.env.user.company_id.sudo().sh_inventory_adjt_barcode_mobile_type == 'all':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.barcode == barcode 
                                                      or l.product_id.default_code == barcode
                                                      or l.product_id.sh_qr_code == barcode)

            
                domain = ["|","|",
                    ("default_code","=",barcode),
                    ("barcode","=",barcode),
                    ("sh_qr_code","=",barcode),                    
                ]  
                       
            if search_lines:
                for line in search_lines:
                    line.product_qty += 1
                    line.sh_inventory_adjt_barcode_mobile_is_last_scanned = True,
                    line.sequence = -1   
                    
                    
                    # =====================================

                    
                    if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_success:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (line.product_id.name,line.product_qty)                        
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                                            
                                     
                    break
            else:
                # =========================================
                # Create Inventory Line Here
                
                product = self.env['product.product'].search(domain,limit = 1)
                
                if product:
                    lines_vals = self.sh_inventory_adjt_barcode_mobile_get_inventory_lines_values(product.id)
                    
                    # add sequence and last scanned here
                    if len(lines_vals) == 1:
                        lines_vals[0].update({
                            "product_qty": 1
                            })
                        
                        
                    if not lines_vals:                        
                        if self.location_ids:
                            lines_vals = [{
                            
                                'product_id': product.id, 
                                'product_qty': 1, 
                                'location_id': self.location_ids[0].ids[0], 
                                'prod_lot_id': False, 
                                'package_id': False, 
                                'partner_id': False, 
                                'inventory_id':self.id,
                                'sh_inventory_adjt_barcode_mobile_is_last_scanned': True, 
                                'sequence': -1, 
                                'product_uom_id': product.uom_id.id if product.uom_id else False,
                            
                            }]
                        else:                                            
                            if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_fail:    
                                message = _(CODE_SOUND_FAIL + 'Please specify at least one location in inventory')                  
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})                        
                                
                            return 
                        
                    
                    self.env['stock.inventory.line'].create( lines_vals )    
                    
                    
                                                        
                    message = _(CODE_SOUND_SUCCESS + 'Product: %s') % (product.name)                        
                    
                    if len(lines_vals) == 1:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (product.name, 1 )                     
                    
                    if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_success:
#                         message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (product.name, 1 )                       
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                                                
                else:    
                    if self.env.user.company_id.sudo().sh_inventory_adjt_bm_is_notify_on_fail:    
                        message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')                  
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                    return
                   
                   








                                    