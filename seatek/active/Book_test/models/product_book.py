from odoo import fields, models

class Author(models.Model):
    _name = "product.author"
    _description = "Author of Book"

    name = fields.Char(string="Full Name")
    age = fields.Integer(string="Age")
    country = fields.Char(string="Country")
    gender = fields.Selection([
        ("male", "Male"),
        ("female", "Female"),
    ], string="Gender", default="male")


class Published(models.Model):
    _name = "product.published"
    _description = "Publish of product"

    name = fields.Char(string="Publish name")

class Language(models.Model):
    _name = "product.language"
    _description = "Language of book"

    name = fields.Char(string="Language")

class Category(models.Model):
    _name = "product.category1"
    _description = "Product Category"

    name = fields.Char(string="Category of product")

class ProductBook(models.Model):
    _inherit = 'product.product'

    is_book = fields.Boolean(string="It is book?", default=False)
    author = fields.Many2one('product.author', string="Author of book")
    published = fields.Many2one('product.published', string="Publish of product")
    language = fields.Many2one('product.language', string="Language of products")
    category = fields.Many2one('product.category1',  string="Category of product")
    coverimage = fields.Binary(string="Cover image")
    topic = fields.Char(string="Topic of book")
    releasedate = fields.Date(string="Release date of book")
    numberofpage = fields.Integer(string="Number of page")
    shelves = fields.Char(string="Shelves to storage book")