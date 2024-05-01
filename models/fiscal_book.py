# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class FiscalBook(models.Model):
    _inherit = 'fiscal.book'

    dte_annexes = fields.Boolean(string="DTE en Anexos")

    @api.onchange('dte_annexes')
    def _onchange_dte_annexes(self):
        if self.dte_annexes:
            # Lanza una alerta en el navegador
            raise UserError("DTE en Anexos está activado. ¡Atención!")