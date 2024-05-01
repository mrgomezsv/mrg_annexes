# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FiscalBook(models.Model):
    _inherit = 'fiscal.book'

    dte_annexes = fields.Boolean(string="DTE en Anexos")
