# -*- coding: utf-8 -*-
{
    'name': "Anexos",

    'summary': """
        Agrega opcion para habilitar o desabilitar campos dte en anexos""",

    'description': """
        Coloca un campo en el Libro de Ventas/Compras con el cual se habilita 
        o desabilitar campo que agrega o quita las columnas de datos del DET 
        en los archivos descargables de Anexos y Sujetos Excluidos
    """,

    'author': "Mario Roberto",
    'website': "https://mrgomezsv.github.io/",

    'category': 'Accounting/Accounting',
    'version': '0.1',

    'depends': ['base', 'account', 'treming_sv_dte', 'treming_sv_fiscal_f07', 'treming_sv_fiscal'],

    'data': [
        'views/fiscal_book.xml',
    ],
}
