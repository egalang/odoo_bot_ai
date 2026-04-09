# -*- coding: utf-8 -*-
{
    'name': "odoo_bot_ai",

    'summary': "Integrates with an external AI service",

    'description': """
        This Odoo module integrates with an external AI service to provide chatbot functionality within Odoo's Discuss application and allows for PDF document uploads for AI knowledge enrichment.
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','im_livechat'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/views.xml',
        'views/odoobotai_views.xml',
        'views/res_config_settings_view.xml',
    ],
    'assets': {
        'web.assets_backend': {
            'odoo_bot_ai/static/src/core/*',
        }
        
    },
    'demo': [
        'demo/demo.xml',
    ],
    # 'installable': True,
    # 'auto_install': True,
}

