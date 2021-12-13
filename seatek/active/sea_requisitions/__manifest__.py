# -*- coding: utf-8 -*-
{
    'name': 'Requisitions Process system',
    'version': '2.0.1',
    'summary': """This module allow your users/employees to create Requisitions to approve. Request approved transfer to PO/Picking.""",
    'description': """
    Requisitions Process
    Module allowed Requisition Process of employee.
    - Email notifications to Department Manager, Requisition Manager for approval.
    - Request for Requisition Order will go to stock/warehouse as internal picking / internal order and purchase order.
    """,
    'author': 'DuyBQ',
    'website': 'https://www.seacorp.com',
    'category': 'seacorp',
    'depends': [
                'stock',
                'hr',
                'purchase',
                ],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/requisition_sequence.xml',
        'data/purchase_approval_template.xml',
        'data/requisition_email_confirm.xml',
        'report/requisition_report.xml',
        'views/requisition_view.xml',
        'views/hr_employee_view.xml',
        'views/hr_department_view.xml',
        'views/stock_picking_view.xml',
    ],
    'installable' : True,
    'application' : True,
}
