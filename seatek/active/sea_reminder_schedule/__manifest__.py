# -*- coding: utf-8 -*-
{
    "name": "Tools sent Mail Reminders",
    "version": "1.0.1",
    "category": "seacorp",
    "author": "DuyBQ",
    "website": "https://seacorp.vn",
    "depends": ["mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/web_view.xml",
        "data/mail_template.xml",
        "data/cron.xml"
        ],
    "external_dependencies": {
        "python": ["xlsxwriter"],
        },
    "summary": "Tools schedule send mail reminders",
    "description": """
            Tools schedule send mail reminders
        """,
    "application": True,
    "installable": True,
    "auto_install": False,
}