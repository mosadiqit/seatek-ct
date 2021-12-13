# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright © 2016 Techspawn Solutions. (<http://techspawn.in>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': "SeaTek Warehouse Restrictions",

    'summary': """
         Warehouse and Stock Location Restriction on Users.""",

    'description': """
        Restrict  Users from Accessing Warehouse and Process Stock Moves other than allowed to Warehouses and Stock Locations.
        12.0.0.2 -> Restrict Operation Type Also
    """,

    'author': "SeaTek",
    'website': "http://www.seatek.vn",
    'license':'OPL-1',	
    'category': 'Warehouse',
    'version': '12.0.0.2',
    'images': ['static/description/seacorp.jpg'],
    'depends': ['base', 'stock', 'sale_stock', 'purchase_stock'],

    'data': [

        'users_view.xml',
        'security/security.xml',
        # 'security/ir.model.access.csv',
    ],
    
    
}
