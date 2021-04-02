# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    product_id = fields.Many2one('product.product', string='Product')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    reference = fields.Char(string='Maintenance No.', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    # area = fields.Char(string='Area',
    #                                related='warehouse_id.partner_id.area')
    area = fields.Selection([('north', 'North'), ('south', 'South'), ('middle', 'Middle')], 'Area', readonly=True,
                            related='warehouse_id.partner_id.area')
    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['reference'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('maintenance.request') or _('New')
            else:
                vals['reference'] = self.env['ir.sequence'].next_by_code('maintenance.request') or _('New')
        result = super(MaintenanceRequest, self).create(vals)
        return result