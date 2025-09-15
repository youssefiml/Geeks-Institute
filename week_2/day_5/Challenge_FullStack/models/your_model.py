from database.index import db

menu_items_chefs = db.Table(
    'menu_items_chefs',
    db.Column('menu_item_id', db.Integer, db.ForeignKey('menu_items.id', ondelete='CASCADE'), primary_key=True),
    db.Column('chef_id', db.Integer, db.ForeignKey('chefs.id', ondelete='CASCADE'), primary_key=True)
)

class Chef(db.Model):
    __tablename__ = 'chefs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(30))
    menu_items = db.relationship('MenuItem', secondary=menu_items_chefs, back_populates='chefs')

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    menu_items = db.relationship('MenuItem', back_populates='category', passive_deletes=True)

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(8,2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    category = db.relationship('Category', back_populates='menu_items')
    chefs = db.relationship('Chef', secondary=menu_items_chefs, back_populates='menu_items')
