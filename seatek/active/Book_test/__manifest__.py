{
    'name': 'Book Store Management',
    'description': 'This is the book store management',
    'version': '12.0.0.0.2',
    'category': 'Book Store',
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/product_book_view.xml',
    ],
    'depends': [
        'product',
    ],
    'installable': True,
}