# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class FiscalBook(models.Model):
    _inherit = 'fiscal.book'

    dte_annexes = fields.Boolean(string="DTE en Anexos")

    @api.onchange('dte_annexes')
    def _onchange_dte_annexes(self):
        if self.dte_annexes:
            _logger.info("El campo dte_annexes se ha activado y su valor es True")
            # Devuelve False para desactivar el campo dte_annexes
            return {'value': False}



    # def generate_csv_purchase(self):
    #     for rec in self:
    #         row = ""
    #         internment_docs_tr_ids = rec.company_id.internment_docs_tr_ids
    #         goods_declaration_ids = rec.company_id.goods_declaration_ids
    #         target_docs = rec.purchase_ids.filtered(
    #             lambda x: x.doc_type.doc_type_id.id not in rec.company_id.doc_type_excluded_ids.ids)
    #         for inv in target_docs:
    #             # Fecha documento
    #             comm_line = inv.invoice_id.common_doc_line_tr_id
    #             row += self.csv_delimiter_tr.format(inv.doc_date.strftime('%d/%m/%Y') or '')
    #             row += self.csv_delimiter_tr.format(
    #                 comm_line.doc_class_id.code if comm_line else "")
    #             row += self.csv_delimiter_tr.format(
    #                 comm_line.doc_type_id.doc_type_f07_id.code if comm_line else '')
    #             # No de documento
    #             row += self.csv_delimiter_tr.format(inv.invoice_id.ref or '')
    #             # NCR
    #             partner = inv.invoice_id.partner_id
    #             clean_data = partner.calc_clean_docs_tr()
    #             clean_nrc = clean_data["nrc"]
    #             clean_nit = clean_data["nit"]
    #             holder_doc = clean_nrc if partner.is_company else clean_nit
    #             if not partner.is_company and not clean_data["dui"]:
    #                 holder_doc = partner.with_context(ignore_type=True).calc_clean_docs_tr()["nit"]
    #
    #             row += self.csv_delimiter_tr.format(holder_doc)
    #             # Proveedor
    #             row += self.csv_delimiter_tr.format(inv.provider or '')
    #             # Compras Internas Exentas
    #             row += self.csv_delimiter_tr.format(inv.exempt_internal or 0.00)
    #             # Internaciones exentas y/o no sujetas
    #             invoice_id = inv.invoice_id
    #
    #             sign = 1
    #             doc_type_id = invoice_id.doc_type_id.doc_type_id
    #
    #             exempt_interment = 0
    #             taxed_interment = 0
    #             if doc_type_id.id in internment_docs_tr_ids.ids:
    #                 if invoice_id.import_exempt_tr and invoice_id.import_purchase_type_tr:
    #                     exempt_interment = invoice_id.import_base_amount + invoice_id.amount_untaxed
    #
    #                 if not invoice_id.import_exempt_tr and invoice_id.import_purchase_type_tr:
    #                     taxed_interment = invoice_id.import_base_amount + invoice_id.amount_untaxed
    #
    #             row += self.csv_delimiter_tr.format(exempt_interment)
    #
    #             # Importaciones exentas y/o no sujetas
    #             exempt_imports = 0
    #             taxed_imports = 0
    #             taxed_imports_services = 0
    #             if doc_type_id.id in goods_declaration_ids.ids:
    #                 if invoice_id.import_exempt_tr and invoice_id.import_purchase_type_tr:
    #                     exempt_imports = invoice_id.import_base_amount + invoice_id.amount_untaxed
    #
    #                 if not invoice_id.import_exempt_tr and invoice_id.import_purchase_type_tr == "good":
    #                     taxed_imports = invoice_id.import_base_amount + invoice_id.amount_untaxed
    #
    #                 if not invoice_id.import_exempt_tr and invoice_id.import_purchase_type_tr == "service":
    #                     taxed_imports_services = invoice_id.import_base_amount + invoice_id.amount_untaxed
    #
    #             row += self.csv_delimiter_tr.format(exempt_imports)
    #
    #             # Compras internas gravadas
    #             row += self.csv_delimiter_tr.format(abs(inv.taxed_internal) or 0.00)
    #             # Internaciones gravadas de bienes
    #             row += self.csv_delimiter_tr.format(abs(taxed_interment))
    #             # Importaciones gravadas de bienes
    #             row += self.csv_delimiter_tr.format(abs(taxed_imports))
    #             # Importaciones gravadas de Servicios
    #             row += self.csv_delimiter_tr.format(abs(taxed_imports_services))
    #             # Credito Fiscal
    #             row += self.csv_delimiter_tr.format(abs(inv.fiscal_credit) or 0.00)
    #             # Total
    #             total = inv.exempt_internal + exempt_interment + exempt_imports + inv.taxed_internal + taxed_interment
    #             total += taxed_imports + taxed_imports_services + inv.fiscal_credit
    #             total = abs(total)
    #             row += self.csv_delimiter_tr.format(total or 0.00)
    #             # DUI
    #             row += self.csv_delimiter_tr.format(clean_data["dui"])
    #             # Campos de ANEXOS
    #             row += self.csv_delimiter_tr.format(inv.invoice_id.type_operation)
    #             row += self.csv_delimiter_tr.format(inv.invoice_id.classification)
    #             row += self.csv_delimiter_tr.format(inv.invoice_id.sector)
    #             row += self.csv_delimiter_tr.format(inv.invoice_id.type_cost_expense)
    #             # No. Anexo
    #             row += "{}\n".format(3)
    #
    #             # Campos DTE
    #             row += self.csv_delimiter_tr.format(inv.invoice_id.dte_uuid_tr)
    #             row += self.csv_delimiter_tr.format(inv.invoice_id.dte_ctrl_number_tr)
    #             row += self.csv_delimiter_tr.format(inv.invoice_id.dte_received_stamp_tr)
    #
    #         txt_file = base64.encodebytes(row.encode(self.csv_encoding_tr))
    #         rec.write({
    #             'csv_file': txt_file,
    #             'csv_filename': "Anexo_Compras.csv",
    #         })
    #     return True


    # def csv_excluded_subject(self):
    #     res = super().csv_excluded_subject()
    #     excludes_types = self.company_id.doc_type_excluded_ids.ids
    #     counter = 1
    #     res = []
    #     invoices = self.purchase_ids.filtered(lambda x: x.doc_type.doc_type_id.id in excludes_types)
    #     invoices_sorted = invoices.sorted(key=lambda x: (x.doc_date, x.doc_number))
    #     for inv in invoices_sorted:
    #         lines, target, doc_number = self.get_resolution_line(inv.invoice_id)
    #         prefix = target.sequence_id.prefix
    #         number = doc_number
    #         holder_value = inv.invoice_id.calc_amount_for_book_tr(self.company_id.excluded_ret_tax_tr_ids)
    #         item = {
    #             'type_doc': inv.invoice_id.partner_id.mh_doc_type_tr_id.code_f07,
    #             'number_doc': (inv.invoice_id.partner_id.calc_dte_doc_number_tr() or "").replace("-", ""),
    #             'provider': inv.provider,
    #             'invoice_date': inv.doc_date.strftime('%d/%m/%Y'),
    #             'serie': prefix or "",
    #             'number': number or "",
    #             'amount': inv.excluded_subject or 0.00,
    #             'retention': abs(holder_value) or 0.00,
    #             'total': inv.total or 0.00,
    #             #ANEXOS
    #             'type_operation': inv.invoice_id.type_operation,
    #             'classification': inv.invoice_id.classification,
    #             'sector': inv.invoice_id.sector,
    #             'type_cost_expense': inv.invoice_id.type_cost_expense,
    #         }
    #         res.append(item)
    #     return res
    #
    #
    #
    # def generate_csv_exclude(self):
    #     for rec in self:
    #         rows = rec.csv_excluded_subject()
    #         row = ""
    #         for line in rows:
    #             # Tipo docuemnto
    #             row += self.csv_delimiter_tr.format(line.get('type_doc', ""))
    #             # numero docuemnto
    #             row += self.csv_delimiter_tr.format(line.get('number_doc', ""))
    #             # Proveedor
    #             row += self.csv_delimiter_tr.format(line.get('provider', ""))
    #             # Fecha documento
    #             row += self.csv_delimiter_tr.format(line.get('invoice_date', ""))
    #             # Serie de documento
    #             row += self.csv_delimiter_tr.format(line.get('serie', ""))
    #             # No. de documento
    #             row += self.csv_delimiter_tr.format(line.get('number', ""))
    #             #
    #             row += self.csv_delimiter_tr.format(line.get('amount', 0.00))
    #             # Debito fiscal
    #             row += self.csv_delimiter_tr.format(line.get('retention', 0.00))
    #
    #             # ANEXOS
    #             row += self.csv_delimiter_tr.format(line.get('type_operation', ""))
    #             row += self.csv_delimiter_tr.format(line.get('classification', ""))
    #             row += self.csv_delimiter_tr.format(line.get('sector', ""))
    #             row += self.csv_delimiter_tr.format(line.get('type_cost_expense', ""))
    #
    #             # No. Anexo
    #             row += "{}\n".format(5)
    #
    #         # Convertir la cadena CSV a base64
    #         csv_base64 = base64.encodebytes(row.encode(self.csv_encoding_tr))
    #
    #         # Escribir los datos en el registro actual
    #         rec.write({
    #             'csv_file': csv_base64,
    #             'csv_filename': "Anexo_Sujetos_Excluidos.csv",
    #         })
    #     return True
    #
