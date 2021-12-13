# Last modifier 12/04/2020 by htkhoa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Last modified Dec42020
{
    "name": "Experience Management 0.2",
    "version": "12.0.1.0.3",
    "author": "Savoir-faire Linux,"
              "OpenSynergy Indonesia,"
              "Numigi,"
              "KhoaHuynh,"
              "Odoo Community Association (OCA)",
    "website": "https://github.com/oca/hr",
    "license": "AGPL-3",
    "category": "Human Resources",
    "depends": ["hr"],
    "data": [
        "security/hr_security.xml",
        "security/ir.model.access.csv",
        "views/hr_employee_view.xml",
        "views/hr_academic_view.xml",
        "views/hr_professional_view.xml",
        "views/hr_skill.xml",
    ],
    'installable': True
}
