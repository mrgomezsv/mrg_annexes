# -*- coding: utf-8 -*-
{
    'name': "Anexos",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Mario Roberto",
    'website': "https://mrgomezsv.github.io/",

    'category': 'Accounting/Accounting',
    'version': '0.1',

    'depends': ['base', 'account', 'treming_sv_dte', 'treming_sv_fiscal_f07', 'treming_sv_fiscal'],

    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
}
