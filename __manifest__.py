{
    'name': 'Dev Jobs',
    'version': '1.0',
    'summary': 'Dev Jobs React App',
    'sequence': 200,
    'description': """Developed by Md. Ashikuzzaman.""",
    'category': '',
    'website': '',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/views_menu.xml',
        'report/job_details_template.xml',
        'report/report.xml',
        'report/dev_jobs_sale_report.xml',
        'report/test_sale_report.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'assets': {},
    'license': 'LGPL-3',
}
