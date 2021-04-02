# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _

class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    asset_category_code = fields.Char(string='Asset Category Code', related='category_id.sub_asset_category_id.code')
    asset_code = fields.Char(string='Asset Code', readonly=True)
    notes = fields.Char(string='Notes')
    product_id = fields.Many2one('product.product', string='Product')
    quant_ids = fields.One2many('stock.quant', compute="_compute_quant_ids",
                                string='Asset Location')

    @api.multi
    def _compute_quant_ids(self):
        for asset in self:
            related_recordset = self.env["stock.quant"].search([("product_id", "=", asset.product_id.id),
                                                                ("location_id.usage", "=", 'internal')])
            asset.quant_ids = related_recordset

    @api.model
    def create(self, vals):
        if vals.get('category_id'):
            category_id = vals.get('category_id')
            # asset_category = self.env['sub.asset.category'].browse(category_id)
            asset_category = self.env['account.asset.category'].browse(category_id)
            if asset_category:
                number_next = asset_category.sub_asset_category_id.sequence_id._next()
                vals['asset_code'] = asset_category.sub_asset_category_id.code + number_next
        return super(AccountAssetAsset, self).create(vals)


class AccountAssetCategory(models.Model):
    _inherit = 'account.asset.category'

    parent_id = fields.Many2one('account.asset.category', 'Parent Asset Type', index=True, ondelete='cascade')
    sub_asset_category_id = fields.Many2one('sub.asset.category', string='Asset Category')
    asset_count = fields.Integer(
        '# Asset', compute='_asset_count',
        help="The number of assets under this category")
    asset_line_ids = fields.One2many('account.asset.asset', 'category_id', string='Assets',
                                     domain=[('state', 'in', ['draft', 'open'])], readonly=True)

    @api.multi
    def open_asset_list(self):
        asset_ids = []
        for asset in self:
            for asset_line in asset.asset_line_ids:
                asset_ids.append(asset_line.id)
        return {
            'name': _('Assets'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.asset.asset',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', asset_ids)],
        }

    def _asset_count(self):
        for asset in self:
            res = self.env['account.asset.asset'].search_count([('category_id', '=', asset.id)])
            asset.asset_count = res


class SubAssetCategory(models.Model):
    _name = "sub.asset.category"
    _description = "Asset Category Code"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    sequence_id = fields.Many2one('ir.sequence', string='Asset Category IDs Sequence',
                                  help="This sequence is automatically created by Odoo but you can change it "
                                       , copy=False)

    _sql_constraints = [
        ('code_uniq', 'unique (code)', "Code already exists !"),
    ]