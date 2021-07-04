# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
from odoo.tools.float_utils import float_round, float_compare, float_is_zero


class stock_move(models.Model):
    _inherit = "stock.move"
     
    sh_stock_move_barcode_mobile = fields.Char(string = "Mobile Barcode")
 

    def default_sh_stock_move_bm_is_cont_scan(self):
        if self.env.user and self.env.user.company_id:
            return self.env.user.company_id.sh_stock_bm_is_cont_scan
    

    sh_stock_move_bm_is_cont_scan = fields.Char(string='Continuously Scan?',default = default_sh_stock_move_bm_is_cont_scan, readonly=True)
    
    
    
    
    
    
    
 
    def sh_stock_move_barcode_mobile_has_tracking(self,CODE_SOUND_SUCCESS,CODE_SOUND_FAIL):
        barcode = self.sh_stock_move_barcode_mobile
        
        if self.picking_code == 'incoming':
            # FOR PURCHASE
            # LOT PRODUCT
            if self.product_id.tracking == 'lot':
                #First Time Scan
                lines = self.move_line_nosuggest_ids.filtered(lambda r: r.lot_name == False)
                if lines:
                    for line in lines:
                        line.qty_done += 1
                        line.lot_name = barcode    
                        
                        # success message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (self.product_id.name, line.qty_done, barcode)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})  
                                  
                                                                                            
                        break
                else:
                    #Second Time Scan
                    lines = self.move_line_nosuggest_ids.filtered(lambda r: r.lot_name == barcode)
                    if lines:                    
                        for line in lines:
                            line.qty_done += 1
#                             line.lot_name = barcode      

                            # success message here
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                                message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (self.product_id.name, line.qty_done, barcode)
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})  

                                                  
                            break
                        
                    else:                      
                        #New Barcode Scan then create new line                    
                        vals_line = {
                            'product_id': self.product_id.id,
                            'location_dest_id':self.location_dest_id.id,
                            'lot_name': barcode,
                            'qty_done':1,
                            'product_uom_id': self.product_uom.id,
                            'location_id': self.location_id.id,                                            
                        } 
                        self.update({
                            'move_line_nosuggest_ids': [(0,0,vals_line)]
                            })
                        
                        
                        # success message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (self.product_id.name, 1, barcode)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})  
                                     
                                  
                                  
                
            # SERIAL PRODUCT
            if self.product_id.tracking == 'serial':                                
                #VALIDATION SERIAL NO. ALREADY EXIST.
                lines = self.move_line_nosuggest_ids.filtered(lambda r: r.lot_name == barcode)   
                if lines:  
#                     warning_mess = {
#                             'title': _('Alert!'),
#                             'message' : 'Serial Number already exist!'
#                         }
#                     return {'warning': warning_mess} 
                
                
                    # failed message here
                    if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                        message = _(CODE_SOUND_FAIL + 'Serial Number already exist!')
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})   
                                        
                    return
                                 
            
                
                #First Time Scan
                lines = self.move_line_nosuggest_ids.filtered(lambda r: r.lot_name == False)
                if lines:
                    for line in lines:
                        line.qty_done += 1
                        line.lot_name = barcode   
                        
                        # success message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (self.product_id.name, line.qty_done, barcode)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})  
                                                 
                            
                        
                                                                             
                        break
                else:
                    #Create new line if not found any unallocated serial number line                    
                    vals_line = {
                        'product_id': self.product_id.id,
                        'location_dest_id':self.location_dest_id.id,
                        'lot_name': barcode,
                        'qty_done':1,
                        'product_uom_id': self.product_uom.id,
                        'location_id': self.location_id.id,                                            
                        } 
                    self.update({
                        'move_line_nosuggest_ids': [(0,0,vals_line)]
                        })
                    
                    # success message here
                    if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (self.product_id.name, 1, barcode)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})  
                                             
         
                   
                                       
                                                  
            
            # for odoo v13
            quantity_done = 0
            for move_line in self.move_line_nosuggest_ids:
                quantity_done += move_line.product_uom_id._compute_quantity(move_line.qty_done, self.product_uom, round=False)
            # for odoo v13   
                            
            
            if quantity_done == self.product_uom_qty + 1:                      
#                 warning_mess = {
#                         'title': _('Alert!'),
#                         'message' : 'Becareful! Quantity exceed than initial demand!'
#                     }
#                 return {'warning': warning_mess}  
            
                # failed message here
                if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                    message = _(CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
                    self.env['bus.bus'].sendone(
                        (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                        {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})   
                
                return               
            
                            
    #             else:
    #                 raise UserError(_("Scanned Internal Reference/Barcode not exist in any product!"))                            
                                              
                                        
        elif self and self.picking_code in ['outgoing','internal']:           
            # FOR SALE
            # LOT PRODUCT
            quant_obj = self.env['stock.quant']
            
            # FOR LOT PRODUCT
            if self.product_id.tracking == 'lot':
                #First Time Scan
                quant = quant_obj.search([
                    ('product_id','=',self.product_id.id),
                    ('quantity','>',0),
                    ('location_id.usage','=', 'internal'),
                    ('lot_id.name','=',barcode),    
                    ('location_id','child_of',self.location_id.id)     
                    ],limit = 1)
                
                if not quant:
#                     raise UserError(_("There are no available qty for this lot/serial."))   
                
                    # failed message here
                    if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                        message = _(CODE_SOUND_FAIL + 'There are no available qty for this lot: %s') % (barcode)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True}) 
                                        
                    return
                                
                                 
                
                lines = self.move_line_ids.filtered(lambda r: r.lot_id == False)
                if lines:
                    for line in lines:
                        line.qty_done += 1
                        line.lot_id = quant.lot_id.id
                        
                        # success message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (self.product_id.name, line.qty_done, quant.lot_id.name)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})  
                                                 
                             
                                                                          
                        break
                else:
                    #Second Time Scan
                    lines = self.move_line_ids.filtered(lambda r: r.lot_id.name == barcode)
                    if lines:
                        for line in lines:
                            line.qty_done += 1
#                             line.lot_name = barcode    

                            # success message here
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                                message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (self.product_id.name, line.qty_done, quant.lot_id.name)
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})  
                                                     
            

                                                    
                            break
                    else:
                        #New Barcode Scan then create new line                    
                        vals_line = {
                            'product_id': self.product_id.id,
                            'location_dest_id':self.location_dest_id.id,
                            'lot_id': quant.lot_id.id,
                            'qty_done':1,
                            'product_uom_id': self.product_uom.id,
                            'location_id': quant.location_id.id,                                            
                        } 
                        self.update({
                            'move_line_ids': [(0,0,vals_line)]
                            })    
                        
                        
                        # success message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (self.product_id.name, 1, quant.lot_id.name)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})  
                                                 
         
                                            
            
            # FOR SERIAL PRODUCT
            if self.product_id.tracking == 'serial':
                #First Time Scan                   
                lines = self.move_line_ids.filtered(lambda r: r.lot_id.name == barcode)
                if lines:
                    for line in lines:
                        line.qty_done += 1
                        
                        # success message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (self.product_id.name, line.qty_done, barcode)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})  
                                                 
                                 
                                  
                                                          
                        
                        res = {}
                        if float_compare(line.qty_done, 1.0, precision_rounding=line.product_id.uom_id.rounding) != 0:
#                             message = _('You can only process 1.0 %s of products with unique serial number.') % line.product_id.uom_id.name
#                             res['warning'] = {'title': _('Warning'), 'message': message}
#                             return res   
                        
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                                message = _(CODE_SOUND_FAIL + 'You can only process 1.0 %s of products with unique serial number.') % line.product_id.uom_id.name
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})                         
                           
                            
                                                                                    
                        break
                else:
                    list_allocated_serial_ids = []
                    if self.move_line_ids:
                        for line in self.move_line_ids:
                            if line.lot_id:
                                list_allocated_serial_ids.append(line.lot_id.id)
                                
                        
                    # if need new line.
                    quant = quant_obj.search([
                        ('product_id','=',self.product_id.id),
                        ('quantity','>',0),
                        ('location_id.usage','=', 'internal'),
                        ('lot_id.name','=',barcode),    
                        ('location_id','child_of',self.location_id.id),
                        ('lot_id.id','not in',list_allocated_serial_ids),
                        ],limit = 1)
                    
                    if not quant:
#                         raise UserError(_("There are no available qty for this lot/serial.")) 
                        # failed message here
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(CODE_SOUND_FAIL + 'There are no available qty for this lot/serial: %s') % (barcode)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                        
                        return
                                        
                                    
                    
                    #New Barcode Scan then create new line                    
                    vals_line = {
                        'product_id': self.product_id.id,
                        'location_dest_id':self.location_dest_id.id,
                        'lot_id': quant.lot_id.id,
                        'qty_done':1,
                        'product_uom_id': self.product_uom.id,
                        'location_id': quant.location_id.id,                                            
                    } 
                    self.update({
                        'move_line_ids': [(0,0,vals_line)]
                        })  
                    
                    # success message here
                    if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s lot/serial: %s') % (self.product_id.name, 1, quant.lot_id.name)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})  
                                             
                             
                    
                                    
            
            
            # for odoo v13
            quantity_done = 0
            for move_line in self._get_move_lines():
                quantity_done += move_line.product_uom_id._compute_quantity(move_line.qty_done, self.product_uom, round=False)
            # for odoo v13          
            
            if self.picking_code == 'outgoing' and quantity_done == self.product_uom_qty + 1:                      
#                 warning_mess = {
#                         'title': _('Alert!'),
#                         'message' : 'Becareful! Quantity exceed than initial demand!'
#                     }
#                 return {'warning': warning_mess}
                # failed message here
                if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                    message = _(CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
                    self.env['bus.bus'].sendone(
                        (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                        {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True}) 
                
                return  
                        
                         
                         
        
        else:
#             raise UserError(_("Picking type is not outgoing or incoming or internal transfer."))
            # failed message here
            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL + 'Picking type is not outgoing or incoming or internal transfer.')
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True}) 
                        

        
    
    
    
    
    
    
    def sh_stock_move_barcode_mobile_no_tracking(self,CODE_SOUND_SUCCESS,CODE_SOUND_FAIL):                    


                        
        move_lines = False
        
        # INCOMING
        # ===================================
        if self.picking_code in ['incoming']:
            move_lines = self.move_line_nosuggest_ids

        # OUTGOING AND TRANSFER
        # ===================================         
        elif self.picking_code in ['outgoing','internal']:
            move_lines = self.move_line_ids            
         
        if move_lines:
            for line in move_lines:
                if self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'barcode':
                    if self.product_id.barcode == self.sh_stock_move_barcode_mobile:
                        line.qty_done += 1
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (self.product_id.name,line.qty_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                                                    
                        
                        
                        if self.quantity_done == self.product_uom_qty + 1:                      
#                             warning_mess = {
#                                     'title': _('Alert!'),
#                                     'message' : 'Becareful! Quantity exceed than initial demand!'
#                                 }
#                             return {'warning': warning_mess}    
                        
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                                message = _(CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})
                                                                      
                        break
                    else:
    
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                            
                        return  
                                                               
                      
                elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'int_ref':
                    if self.product_id.default_code == self.sh_stock_move_barcode_mobile:
                        line.qty_done += 1
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (self.product_id.name,line.qty_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                                                    
                        if self.quantity_done == self.product_uom_qty + 1:                      
#                             warning_mess = {
#                                     'title': _('Alert!'),
#                                     'message' : 'Becareful! Quantity exceed than initial demand!'
#                                 }
#                             return {'warning': warning_mess}     
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                                message = _(CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})                        
                                                      
                        break
                    else:
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                            
                        return                              
                                          
                      
                elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'sh_qr_code':
                    if self.product_id.sh_qr_code == self.sh_stock_move_barcode_mobile:
                        line.qty_done += 1
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (self.product_id.name,line.qty_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                                                    
                        if self.quantity_done == self.product_uom_qty + 1:                        
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                                message = _(CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})                        
                                                      
                        break
                    else:
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                            
                        return                          
                      
                      
                elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'all':
                    
                    if self.product_id.barcode == self.sh_stock_move_barcode_mobile or self.product_id.default_code == self.sh_stock_move_barcode_mobile or self.product_id.sh_qr_code == self.sh_stock_move_barcode_mobile:
                        line.qty_done += 1
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (self.product_id.name,line.qty_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                                                    
                        if self.quantity_done == self.product_uom_qty + 1:                    
#                             warning_mess = {
#                                     'title': _('Alert!'),
#                                     'message' : 'Becareful! Quantity exceed than initial demand!'
#                                 }
#                             return {'warning': warning_mess}    
                            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                                message = _(CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Alert!'), 'message': message, 'sticky': False, 'warning': True})  
                                                              
                        break
                    else:
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                            
                        return                           
                  
        else:
            
            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL + 'Pls add all product items in line than rescan.')
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                
            return           
         
    
        
    
    
    
    
    
        
     
    @api.onchange('sh_stock_move_barcode_mobile')
    def _onchange_sh_stock_move_barcode_mobile(self):
        
        if self.sh_stock_move_barcode_mobile in ['',"",False,None]:
            return
        
        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""
        if self.env.user.company_id.sudo().sh_stock_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"
        
        if self.env.user.company_id.sudo().sh_stock_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"    
                     
         
        if self.picking_id.state not in ['confirmed','assigned']:
            selections = self.picking_id.fields_get()['state']['selection']
            value = next((v[1] for v in selections if v[0] == self.picking_id.state), self.picking_id.state)
            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL + 'You can not scan item in %s state.')% (value)
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                
            return
        
        
        
        
        
        
        if self.sh_stock_move_barcode_mobile:
            if self.has_tracking != 'none':
                self.sh_stock_move_barcode_mobile_has_tracking(CODE_SOUND_SUCCESS,CODE_SOUND_FAIL)
                
            else:
                self.sh_stock_move_barcode_mobile_no_tracking(CODE_SOUND_SUCCESS,CODE_SOUND_FAIL)          

    
        
    
            
class stock_picking(models.Model):
    _inherit = "stock.picking"

      
    
    def default_sh_stock_bm_is_cont_scan(self):
        if self.env.user and self.env.user.company_id:
            return self.env.user.company_id.sh_stock_bm_is_cont_scan
    
    sh_stock_barcode_mobile = fields.Char(string = "Mobile Barcode")
    
    sh_stock_bm_is_cont_scan = fields.Char(string='Continuously Scan?',default = default_sh_stock_bm_is_cont_scan, readonly=True)
        
 
     
            
    
    
    
    @api.onchange('sh_stock_barcode_mobile')
    def _onchange_sh_stock_barcode_mobile(self):
        
                    
        if self.sh_stock_barcode_mobile in ['',"",False,None]:
            return
        
        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""
        if self.env.user.company_id.sudo().sh_stock_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"
        
        if self.env.user.company_id.sudo().sh_stock_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"       
                    
        if self and self.state not in ['assigned','draft','confirmed']:
            selections = self.fields_get()['state']['selection']
            value = next((v[1] for v in selections if v[0] == self.state), self.state)
                    
            if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL + 'You can not scan item in %s state.')% (value)
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                
            return
                    
        
        elif self and self.picking_type_code == 'outgoing':
            search_mls = False
            domain = []
             
            
            if self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'barcode':
                search_mls = self.move_line_ids_without_package.filtered(lambda ml: ml.product_id.barcode == self.sh_stock_barcode_mobile)
                domain = [("barcode","=",self.sh_stock_barcode_mobile)]
            
            elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'int_ref':
                search_mls = self.move_line_ids_without_package.filtered(lambda ml: ml.product_id.default_code == self.sh_stock_barcode_mobile)
                domain = [("default_code","=",self.sh_stock_barcode_mobile)]                

            elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'sh_qr_code':
                search_mls = self.move_line_ids_without_package.filtered(lambda ml: ml.product_id.sh_qr_code == self.sh_stock_barcode_mobile)
                domain = [("sh_qr_code","=",self.sh_stock_barcode_mobile)]   
                
            elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'all':
                search_mls = self.move_line_ids_without_package.filtered(lambda ml: ml.product_id.barcode == self.sh_stock_barcode_mobile 
                                                                         or ml.product_id.default_code == self.sh_stock_barcode_mobile
                                                                         or ml.product_id.sh_qr_code == self.sh_stock_barcode_mobile
                                                                         )
                domain = ["|","|",
                    ("default_code","=",self.sh_stock_barcode_mobile),
                    ("barcode","=",self.sh_stock_barcode_mobile),
                    ("sh_qr_code","=",self.sh_stock_barcode_mobile)                    
                ]  
                                                                 
            if search_mls:
                for move_line in search_mls:
                    
#                     if move_line.product_id.tracking != 'none':
#                                    
#                         if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
#                             message = _(CODE_SOUND_FAIL + 'You can not scan product item for lot/serial directly here, Pls click detail button (at end each line) and than rescan your product item.')
#                             self.env['bus.bus'].sendone(
#                                 (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
#                                 {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
#                             
#                         return
                                   
                                                   
                                      
                    if self.state == 'draft':
                        move_line.qty_done += 1
                        
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (move_line.product_id.name,move_line.qty_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                                                
                    else:
                        move_line.qty_done = move_line.qty_done + 1
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (move_line.product_id.name,move_line.qty_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})    
                                                                    
#                         if move_line.qty_done == move_line.product_uom_qty + 1:                    
#                         
#                             if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
#                                 message = _(CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
#                                 self.env['bus.bus'].sendone(
#                                     (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
#                                     {'type': 'simple_notification', 'title': _('Alert'), 'message': message, 'sticky': False, 'warning': True})
                                
                                                        
                    
                    break
                                    
            elif self.state == 'draft':
                if self.env.user.company_id.sudo().sh_stock_bm_is_add_product:
                    if not self.picking_type_id:
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(CODE_SOUND_FAIL + 'You must first select a Operation Type.')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                            
                        return  
                                                                      
                        
                    search_product = self.env["product.product"].search(domain, limit = 1)
                    if search_product:                           
                        stock_move_line_vals = {
#                            "name": search_product.name,
                           "product_id": search_product.id,
#                            "product_uom_qty": 1,
#                            "price_unit": search_product.lst_price,
                           "qty_done" : 1,
                           "location_id" : self.location_id.id,
                           "location_dest_id": self.location_dest_id.id,
#                            'date' : str(fields.date.today())
                           'date' : self.scheduled_date or fields.date.today(),
                           'company_id' : self.company_id.id if self.company_id else self.env.user.company_id.id                           
                        }      
                        if search_product.uom_id:
                            stock_move_line_vals.update({
                                "product_uom_id": search_product.uom_id.id,                            
                            })    
                            
                        old_lines = self.move_line_ids_without_package
                        new_order_line = self.move_line_ids_without_package.create(stock_move_line_vals)
                        self.move_line_ids_without_package = old_lines + new_order_line
                        new_order_line.onchange_product_id()  
                        
                        
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (new_order_line.product_id.name,new_order_line.product_uom_qty)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})   
                                                                            
                                            
                    else:   
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                            
                        return  
                                                                                   
                                           
                else:
                    if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                        message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                        
                    return    
            else:
                if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                    message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                    self.env['bus.bus'].sendone(
                        (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                        {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                    
                return    
        
        
        elif self and self.picking_type_code == 'incoming':            
            search_mls = False
            domain = []
                        
            if self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'barcode':
                search_mls = self.move_ids_without_package.filtered(lambda ml: ml.product_id.barcode == self.sh_stock_barcode_mobile)
                domain = [("barcode","=",self.sh_stock_barcode_mobile)]
            
            elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'int_ref':
                search_mls = self.move_ids_without_package.filtered(lambda ml: ml.product_id.default_code == self.sh_stock_barcode_mobile)
                domain = [("default_code","=",self.sh_stock_barcode_mobile)]                

            elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'sh_qr_code':
                search_mls = self.move_ids_without_package.filtered(lambda ml: ml.product_id.sh_qr_code == self.sh_stock_barcode_mobile)
                domain = [("sh_qr_code","=",self.sh_stock_barcode_mobile)]  
                
            elif self.env.user.company_id.sudo().sh_stock_barcode_mobile_type == 'all':
                search_mls = self.move_ids_without_package.filtered(lambda ml: ml.product_id.barcode == self.sh_stock_barcode_mobile or ml.product_id.default_code == self.sh_stock_barcode_mobile)
                domain = ["|","|",
                    ("default_code","=",self.sh_stock_barcode_mobile),
                    ("barcode","=",self.sh_stock_barcode_mobile),
                    ("sh_qr_code","=",self.sh_stock_barcode_mobile),                    
                ]  
                                                                      
            if search_mls:
                for move_line in search_mls:
                    if move_line.product_id.tracking != 'none':
                                   
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(CODE_SOUND_FAIL + 'You can not scan product item for lot/serial directly here, Pls click detail button (at end each line) and than rescan your product item.')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                            
                        return
                                   
                                                   
                                      
                    if self.state == 'draft':
                        move_line.quantity_done += 1            
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (move_line.product_id.name,move_line.quantity_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                                                
                    else:
                        move_line.quantity_done = move_line.quantity_done + 1
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (move_line.product_id.name,move_line.quantity_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})    
                                                                    
#                         if move_line.quantity_done == move_line.product_qty + 1:                    
#                             if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
#                                 message = _(CODE_SOUND_FAIL + 'Becareful! Quantity exceed than initial demand!')
#                                 self.env['bus.bus'].sendone(
#                                     (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
#                                     {'type': 'simple_notification', 'title': _('Alert'), 'message': message, 'sticky': False, 'warning': True})
                                
                                                        
                    
                    break
                                    
            elif self.state == 'draft':
                if self.env.user.company_id.sudo().sh_stock_bm_is_add_product:
                    if not self.picking_type_id:
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(CODE_SOUND_FAIL + 'You must first select a Operation Type.')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                            
                        return  
                                                                      
                        
                    search_product = self.env["product.product"].search(domain, limit = 1)
                    if search_product:  
                        stock_move_vals = {
                            "name": search_product.name,
                            "product_id": search_product.id,
#                             "product_qty": 1,
                            "price_unit": search_product.lst_price,
                            "quantity_done" : 1,
                            "location_id" : self.location_id.id,
                            "location_dest_id": self.location_dest_id.id,
                            'date_expected' : self.scheduled_date or fields.date.today()
                        }      
                        if search_product.uom_id:
                            stock_move_vals.update({
                                "product_uom": search_product.uom_id.id,                            
                            })    
                            
                        old_lines = self.move_ids_without_package
                        new_order_line = self.move_ids_without_package.create(stock_move_vals)
                        self.move_ids_without_package = old_lines + new_order_line
                        new_order_line.onchange_product_id()  
                        
                        
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (new_order_line.product_id.name,new_order_line.quantity_done)
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})   
                                                                            
                                            
                    else:   
                        if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                            message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                            
                        return  
                                                                                   
                                           
                else:
                    if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                        message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                        
                    return    
                
            else:
                if self.env.user.company_id.sudo().sh_stock_bm_is_notify_on_fail:
                    message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')
                    self.env['bus.bus'].sendone(
                        (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                        {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                    
                return                
            
            
             
        