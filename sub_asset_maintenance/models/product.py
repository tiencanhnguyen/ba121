# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_asset = fields.Boolean(string="Is a Asset ?", default=False)
    is_equipment = fields.Boolean(string="Is a Equipment ?", default=False)
    asset_product_ids = fields.Many2many('product.product', 'asset_product_accessory_rel', 'product_template_id', 'product_product_id',
                                             string='Asset Accessory Products')