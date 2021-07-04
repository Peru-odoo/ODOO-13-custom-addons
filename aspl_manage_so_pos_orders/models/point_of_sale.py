# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

import logging
from odoo import tools, models, fields, api, _
from datetime import datetime
import psycopg2
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = 'pos.config'

    sale_order_operations = fields.Selection([('draft', 'Quotations'),
                                              ('confirm', 'Confirm'), ('paid', 'Paid')], "Operation", default="draft")
    sale_order_last_days = fields.Char("Load Sale Orders to Last days")
    sale_order_record_per_page = fields.Char("Sale Order Per Page")
    order_last_days = fields.Char("Load Orders to Last days")
    order_record_per_page = fields.Char("Record Per Page")
    paid_amount_product = fields.Many2one('product.product', string='Paid Amount Product',
                                          domain=[('available_in_pos', '=', True)])
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    sale_order_invoice = fields.Boolean("Invoice")
    enable_reorder = fields.Boolean("Order Management")


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _process_order(self, order, draft, existing_order):
        if order.get('data').get('old_order_id'):
            pos_line_obj = self.env['pos.order.line']
            order = order['data']
            pos_order = self.browse([order.get('old_order_id')])
            old_order = self.search_read([('id', '=', pos_order.id)])
            pos_line_ids = pos_line_obj.search([('order_id', '=', pos_order.id)])
            if pos_line_ids:
                if not order.get('cancel_order'):
                    for line_id in pos_line_ids:
                        line_id.unlink()
                temp = order.copy()
                temp['name'] = old_order[0]['pos_reference']
                temp['pos_reference'] = old_order[0]['pos_reference']
                old_order[0]['pos_session_id'] = temp['pos_session_id']
                old_order[0]['lines'] = temp['lines']
                total_price = 0.00
                total_price += sum([line[2].get('price_subtotal_incl') for line in temp.get('lines')])
                temp['amount_total'] = total_price
                pos_order.write(self._order_fields(temp))
            for payments in order['statement_ids']:
                pos_order.with_context({'from_pos': True}).add_payment(self._payment_fields(pos_order, payments[2]))
            if not draft:
                try:
                    pos_order.action_pos_order_paid()
                except psycopg2.DatabaseError:
                    # do not hide transactional errors, the order(s) won't be saved!
                    raise
                except Exception as e:
                    _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))

            return pos_order.id

        else:
            to_invoice = order['to_invoice'] if not draft else False
            order = order['data']
            pos_session = self.env['pos.session'].browse(order['pos_session_id'])
            if pos_session.state == 'closing_control' or pos_session.state == 'closed':
                order['pos_session_id'] = self._get_valid_session(order).id

            pos_order = False
            if not existing_order:
                temp = order.copy()
                pos_order1 = self.browse([order.get('name')])
                pos_order = self.create(self._order_fields(temp))
            else:
                pos_order = existing_order
                pos_order.lines.unlink()
                order['user_id'] = pos_order.user_id.id
                pos_order.write(self._order_fields(order))
            self._process_payment_lines(order, pos_order, pos_session, draft)
            if not draft:
                try:
                    pos_order.action_pos_order_paid()
                except psycopg2.DatabaseError:
                    # do not hide transactional errors, the order(s) won't be saved!
                    raise
                except Exception as e:
                    _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))

            if to_invoice:
                pos_order.action_pos_order_invoice()
                pos_order.account_move.sudo().with_context(force_company=self.env.user.company_id.id).post()

            self._process_payment_lines(order, pos_order, pos_session, draft)
            return pos_order.id

    @api.model
    def ac_pos_search_read(self, domain):
        domain = domain.get('domain')
        search_vals = self.search_read(domain,
                                       ['create_date', 'state', 'date_order', 'name', 'pos_reference',
                                        'write_date', 'id', 'partner_id', 'lines', 'amount_total',
                                        'company_id', 'payment_ids'])

        local = pytz.timezone(self._context.get('tz', 'utc') or 'utc')
        result = []
        for val in search_vals:
            order_date = pytz.utc.localize(
                datetime.strptime(str(val.get('date_order')), DEFAULT_SERVER_DATETIME_FORMAT))
            final_converted_date = datetime.strftime(order_date.astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
            val.update({'date_order': final_converted_date})
            result.append(val)

        for res in result:
            line_dict = self.env['pos.order.line'].browse(res.get('lines'))
            if line_dict:
                res['lines'] = line_dict.read()
        return result


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create_from_ui(self, partner):
        if partner.get('property_product_pricelist'):
            price_list_id = int(partner.get('property_product_pricelist'))
            partner.update({'property_product_pricelist': price_list_id})
        return super(ResPartner, self).create_from_ui(partner)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
