# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class FiscalBook(models.Model):
    _inherit = 'fiscal.book'

    dte_annexes = fields.Boolean(string="DTE en Anexos")

    # @api.onchange('dte_annexes')
    # def _onchange_dte_annexes(self):
    #     if self.dte_annexes:
    #         # Lanza una alerta en el navegador
    #         raise UserError("DTE en Anexos está activado. ¡Atención!")

    def get_resolution_line(self, invoice_id, comp_date=False):
        if not comp_date:
            comp_date = invoice_id.invoice_date

        lines = invoice_id.doc_type_id.journal_id.doc_resolution_ids.filtered(
            lambda x: x.doc_type_id.id == invoice_id.doc_type_id.id and (
                    x.sequence_id.prefix or '') in invoice_id.name and x.auth_date <= comp_date)
        doc_number = ""
        target = None  # Valor por defecto
        if lines:
            sorted_lines = lines.sorted(key=lambda x: x.auth_date, reverse=True)
            target = sorted_lines[0]
            doc_number = invoice_id.name.replace(target.sequence_id.prefix, "")

        return sorted_lines, target, doc_number

    def generate_csv_sale(self):
        consumer_types = self.company_id.doc_type_cons_ids.ids
        for_consumer = self.sale_ids.filtered(lambda x: x.doc_type.doc_type_id.id in consumer_types)
        order_consumer = for_consumer.sorted(key=lambda x: (x.doc_date, x.pos_number, str(x.doc_number)))
        for rec in self:
            row = ""
            for inv in rec.sale_ids.filtered(
                    lambda x: x.invoice_id.doc_type_id.doc_type_id.id in rec.company_id.doc_type_cons_ids.ids
                              and x.invoice_id.state == "posted"):
                # if inv.doc_date:
                # Fecha documento
                row += self.csv_delimiter_tr.format(inv.doc_date.strftime('%d/%m/%Y') or '')
                # Clase de documento
                doc_type = inv.invoice_id.doc_type_id.doc_type_id
                row += self.csv_delimiter_tr.format(doc_type.doc_class_f07_id.code or '')
                # Tipo de documento
                row += self.csv_delimiter_tr.format(doc_type.doc_type_f07_id.code or '')
                # No. Resolucion/No interno DEL/
                lines, target, doc_number = self.get_resolution_line(inv.invoice_id)
                clean_number = target.calc_clean_number_tr()
                row += self.csv_delimiter_tr.format(clean_number["number"])
                row += self.csv_delimiter_tr.format(target.sequence_id.prefix or '')
                doc_number = inv.invoice_id.calc_f7_sale_dn_tr(doc_number)

                row += self.csv_delimiter_tr.format(doc_number)
                row += self.csv_delimiter_tr.format(doc_number)
                row += self.csv_delimiter_tr.format(doc_number)
                row += self.csv_delimiter_tr.format(doc_number)
                holder = self.calc_machine_number(inv.invoice_id, target)
                row += self.csv_delimiter_tr.format(holder)
                # Ventas Exentas
                row += self.csv_delimiter_tr.format(inv.exempt or 0.00)
                # Ventas Internas Exentas no sujetas a proporcionalidad
                row += self.csv_delimiter_tr.format(inv.nosubject or 0.00)
                # Ventas no sujetas
                row += self.csv_delimiter_tr.format(inv.nosubject or 0.00)
                # Ventas Gravadas local
                row += self.csv_delimiter_tr.format(inv.taxed_internal or 0.00)
                # Exportaciones dentro de centroamerica
                export_val = inv.invoice_id.calc_export_f7_value_tr()
                row += self.csv_delimiter_tr.format(export_val["inside_ca"])
                # Exportaciones fuera de centroamerica
                row += self.csv_delimiter_tr.format(export_val["outside_ca"])
                # Exportaciones de servicios
                row += self.csv_delimiter_tr.format(export_val["service"])
                # Ventas Zonas francas
                row += self.csv_delimiter_tr.format(export_val["free_zone"])
                # Ventas cuentas de terceros no domiciliados
                row += self.csv_delimiter_tr.format(0.00)
                if rec.dte_annexes:  # Agrega las siguientes líneas solo si dte_annexes es True
                    # Agregar campos de account.move DTE
                    row += self.csv_delimiter_tr.format(inv.invoice_id.dte_uuid_tr or '')
                    row += self.csv_delimiter_tr.format(inv.invoice_id.dte_received_stamp_tr or '')
                    row += self.csv_delimiter_tr.format(inv.invoice_id.dte_received_state_tr or '')
                total = 0
                to_sum = ["exempt", "nosubject", "nosubject", "taxed_internal"]
                for key in to_sum:
                    total += inv[key]
                total = inv.invoice_id.calc_round_tr(total)

                # Total
                row += self.csv_delimiter_tr.format(total or 0.00)
                # No. Anexo
                row += "{}\n".format(2)
            txt_file = base64.encodebytes(row.encode(self.csv_encoding_tr))
            rec.write({
                'csv_file': txt_file,
                'csv_filename': "Anexo_Consumidor_Final.csv",
            })
        return True

    def generate_csv_taxp(self):
        for rec in self:
            rows = rec.csv_taxpayer_lines()
            row = ""
            for line in rows:
                # Fecha documento
                row += self.csv_delimiter_tr.format(line.get('doc_date', ""))
                # Clase de documento
                row += self.csv_delimiter_tr.format(line.get('class_document', ""))
                # Tipo de documento
                row += self.csv_delimiter_tr.format(line.get('type_document', ""))
                # No. Resolucion/No interno DEL/
                row += self.csv_delimiter_tr.format(line.get('resolution', ""))
                # Serie de documento
                row += self.csv_delimiter_tr.format(line.get('serie', ""))
                # No. de documento
                row += self.csv_delimiter_tr.format(line.get('doc_number', ""))
                # No. Interno de documento
                row += self.csv_delimiter_tr.format(line.get('doc_number', ""))
                # No. Interno de documento
                row += self.csv_delimiter_tr.format(line.get('nit', ""))
                # Razon social del cliente
                row += self.csv_delimiter_tr.format(line.get('customer', ""))
                # Ventas Exentas
                row += self.csv_delimiter_tr.format(line.get('exempt', 0.00))
                # Ventas no sujetas
                row += self.csv_delimiter_tr.format(line.get('nosubject', 0.00))
                # Ventas Gravadas local
                row += self.csv_delimiter_tr.format(line.get('taxed_internal', 0.00))
                # Debito fiscal
                row += self.csv_delimiter_tr.format(line.get('fiscal_debit', 0.00))
                # Ventas a cuentas de terceros no domiciliados
                row += self.csv_delimiter_tr.format(0.00)
                # Debito fiscal no domiciliados
                row += self.csv_delimiter_tr.format(0.00)
                if rec.dte_annexes:  # Agrega las siguientes líneas solo si dte_annexes es True
                    # Agregar campos de account.move DTE
                    row += self.csv_delimiter_tr.format(line.get('dte_uuid_tr', "") or '')
                    row += self.csv_delimiter_tr.format(line.get('dte_received_stamp_tr', "") or '')
                    row += self.csv_delimiter_tr.format(line.get('dte_received_state_tr', "") or '')
                # Total
                row += self.csv_delimiter_tr.format(line.get('total', 0.00))
                # DUI
                row += self.csv_delimiter_tr.format(line.get('dui', ""))
                # No. Anexo
                row += "{}\n".format(1)
            txt_file = base64.encodebytes(row.encode(self.csv_encoding_tr))
            rec.write({
                'csv_file': txt_file,
                'csv_filename': "Anexo_Contribuyentes.csv",
            })
        return True
