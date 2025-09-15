import os
from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database.index import db
from models.your_model import MenuItem, Chef, Category

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/restaurant_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    db.init_app(app)
    return app

app = create_app()

with app.app_context():
    db.create_all()

def parse_price(val):
    try:
        return Decimal(val)
    except Exception:
        return None

@app.route('/')
def index():
    q = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)

    query = MenuItem.query.order_by(MenuItem.id.desc())
    if q:
        query = query.filter(MenuItem.name.ilike(f'%{q}%'))

    pagination = query.paginate(page=page, per_page=6, error_out=False)
    items = pagination.items

    return render_template('index.html', items=items, pagination=pagination, q=q)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price_raw = request.form.get('price', '').strip()
        category_id = request.form.get('category_id') or None
        chef_ids = request.form.getlist('chefs')

        errors = []
        if not name:
            errors.append('Name is required.')
        price = parse_price(price_raw)
        if price is None:
            errors.append('Price must be a valid number.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            chefs = Chef.query.all()
            categories = Category.query.all()
            return render_template('create.html', chefs=chefs, categories=categories, form=request.form)

        item = MenuItem(name=name, description=description, price=price)
        if category_id:
            item.category_id = int(category_id)
        if chef_ids:
            chefs = Chef.query.filter(Chef.id.in_(chef_ids)).all()
            item.chefs = chefs

        db.session.add(item)
        db.session.commit()
        flash('Menu item created successfully.', 'success')
        return redirect(url_for('index'))

    chefs = Chef.query.all()
    categories = Category.query.all()
    return render_template('create.html', chefs=chefs, categories=categories)

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    item = MenuItem.query.get_or_404(item_id)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price_raw = request.form.get('price', '').strip()
        category_id = request.form.get('category_id') or None
        chef_ids = request.form.getlist('chefs')

        errors = []
        if not name:
            errors.append('Name is required.')
        price = parse_price(price_raw)
        if price is None:
            errors.append('Price must be a valid number.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            chefs = Chef.query.all()
            categories = Category.query.all()
            return render_template('edit.html', item=item, chefs=chefs, categories=categories)

        item.name = name
        item.description = description
        item.price = price
        item.category_id = int(category_id) if category_id else None
        if chef_ids:
            item.chefs = Chef.query.filter(Chef.id.in_(chef_ids)).all()
        else:
            item.chefs = []
        db.session.commit()
        flash('Menu item updated.', 'success')
        return redirect(url_for('index'))

    chefs = Chef.query.all()
    categories = Category.query.all()
    return render_template('edit.html', item=item, chefs=chefs, categories=categories)

@app.route('/details/<int:item_id>')
def details(item_id):
    item = MenuItem.query.get_or_404(item_id)
    return render_template('details.html', item=item)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Menu item deleted.', 'success')
    return redirect(url_for('index'))

@app.route('/chefs')
def list_chefs():
    chefs = Chef.query.order_by(Chef.name).all()
    return render_template('chefs.html', chefs=chefs)

@app.route('/stats')
def stats():
    counts = db.session.query(Category.name, db.func.count(MenuItem.id))\
        .join(MenuItem, MenuItem.category_id == Category.id, isouter=True)\
        .group_by(Category.name).all()

    price_buckets = db.session.query(
        db.func.count(MenuItem.id),
        db.func.sum(MenuItem.price)
    ).all()

    labels = [row[0] or 'Uncategorized' for row in counts]
    values = [int(row[1]) for row in counts]

    avg_per_cat = db.session.query(
        Category.name,
        db.func.avg(MenuItem.price)
    ).join(MenuItem, MenuItem.category_id == Category.id, isouter=True).group_by(Category.name).all()

    avg_labels = [row[0] or 'Uncategorized' for row in avg_per_cat]
    avg_values = [float(row[1] or 0) for row in avg_per_cat]

    return render_template('stats.html',
                           labels=labels, values=values,
                           avg_labels=avg_labels, avg_values=avg_values)

if __name__ == '__main__':
    app.run(debug=True)
