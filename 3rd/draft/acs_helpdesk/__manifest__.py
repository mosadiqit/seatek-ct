# -*- coding: utf-8 -*-
#╔══════════════════════════════════════════════════════════════════╗
#║                                                                  ║
#║                ╔═══╦╗       ╔╗  ╔╗     ╔═══╦═══╗                 ║
#║                ║╔═╗║║       ║║ ╔╝╚╗    ║╔═╗║╔═╗║                 ║
#║                ║║ ║║║╔╗╔╦╦══╣╚═╬╗╔╬╗ ╔╗║║ ╚╣╚══╗                 ║
#║                ║╚═╝║║║╚╝╠╣╔╗║╔╗║║║║║ ║║║║ ╔╬══╗║                 ║
#║                ║╔═╗║╚╣║║║║╚╝║║║║║╚╣╚═╝║║╚═╝║╚═╝║                 ║
#║                ╚╝ ╚╩═╩╩╩╩╩═╗╠╝╚╝╚═╩═╗╔╝╚═══╩═══╝                 ║
#║                          ╔═╝║     ╔═╝║                           ║
#║                          ╚══╝     ╚══╝                           ║
#║ SOFTWARE DEVELOPED AND SUPPORTED BY ALMIGHTY CONSULTING SERVICES ║
#║                   COPYRIGHT (C) 2016 - TODAY                     ║
#║                   http://www.almightycs.com                      ║
#║                                                                  ║
#╚══════════════════════════════════════════════════════════════════╝
{
    'name': 'Website Helpdesk Support & Ticket Management',
    'category': 'Extra-addons',
    'version': '1.0.2',
    'author': 'Almighty Consulting Services',
    'support': 'info@almightycs.com',
    'website': 'http://www.almightycs.com',
    'summary': """Manage Website Helpdesk Support Tickets for Service Industry or Support after Sales.""",
    'description': """Manage Website Helpdesk Support Tickets for Service Industry or Support after Sales. website helpdesk support ticket management. support portal by almightycs. customer support ticket after sales
        website ticket management customer support management helpdesk management helpdesk tickets

        Gérez les tickets de support du site Web du support technique pour le secteur des services ou le support après-vente. gestion des tickets d'assistance du site web helpdesk. portail de support par almightycs. ticket de support client après-vente
         site web gestion des tickets gestion de l'assistance clientèle gestion de l'aide helpdesk tickets

        Verwalten Sie Support-Tickets für das Website-Helpdesk für das Dienstleistungsgewerbe oder den Kundendienst. Website-Helpdesk-Support-Ticketverwaltung. Unterstützungsportal von almightycs. Kundensupportticket nach dem Verkauf
         Website Ticket Management Customer Support Management Helpdesk Management Helpdesk-Tickets

        Gestione los tickets de soporte de Helpdesk para la industria de servicios o soporte postventa. Soporte técnico del sitio web de soporte de tickets. Portal de soporte por almightycs. ticket de atención al cliente postventa
         sitio web gestión de tickets atención al cliente gestión helpdesk gestión helpdesk tickets

        Beheer Website Helpdesk Support Tickets voor Service Industry of Support after sales. website helpdesk ondersteuning ticketbeheer. ondersteuningsportaal door almightycs. klantenondersteuning ticket na verkoop
         website ticket management klantenondersteuning management helpdesk management helpdesk tickets
    """,
    'depends': ['hr_timesheet','portal','website','document','account','rating'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/mail_template.xml',
        'views/assets.xml',
        'views/helpdesk_rating_view.xml',
        'views/helpdesk_view.xml',
        'views/helpdesk_stage_view.xml',
        'views/helpdesk_team_view.xml',
        'views/helpdesk_ticket_view.xml',
        'views/helpdesk_team_view.xml',
        'views/partner_view.xml',
        'views/res_config_view.xml',
        'views/portal_templates.xml',
        'views/menu_item.xml',
    ],
    'images': [
        'static/description/almightycs_helpdesk_cover.jpg',
    ],
    'sequence': 1,
    'application': True,
    'installable': True,
    'auto_install': False,
    'price': 36,
    'currency': 'EUR',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
