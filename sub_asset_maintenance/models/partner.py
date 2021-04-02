# -*- coding: utf-8 -*-

from odoo import api, fields, tools, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    area = fields.Selection([('north', 'North'), ('south', 'South'), ('middle', 'Middle')], 'Area')
