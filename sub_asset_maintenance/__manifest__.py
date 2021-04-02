{
    'name' : 'Sub Asset Maintenance',
    'version' : '2.0.0',
    'author' : 'Baotnp',
    'description': """
Sub Asset Maintenance
====================================

    """,
    'category': 'custom',
    'depends': ['base','point_of_sale'],
    'data':[
        'views/product_view.xml',
        'views/asset_view.xml',
        'views/partner_view.xml',
        'views/maintenance_view.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'report/asset_reports.xml',
        'report/account_asset_asset.xml',
        ],
    'qweb': [
    ],
    'installable': True,
}
