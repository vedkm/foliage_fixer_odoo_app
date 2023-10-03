# -*- coding: utf-8 -*-
{
    'name': "Foliage Fixer",

    'summary': """
       An app for automatically detecting disease in tomato plants.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ved Mahadeo",
    'website': "https://vedmahadeo.pythonanywhere.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/foliage_fixer',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'base_automation', 'web_tour'],

    'external_dependencies': {'python': ['requests', 'python-dotenv', 'responses']},

    # always loaded
    'data': [
        'security/foliage_fixer_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/plant_view.xml',
        'views/scan_view.xml',
        'views/foliage_fixer_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'application': True,

    'sequence': -100
}
