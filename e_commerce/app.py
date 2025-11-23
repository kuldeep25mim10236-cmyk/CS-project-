from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///megastore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Database Models
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(10), default='📦')
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'description': self.description,
            'icon': self.icon,
            'stock': self.stock
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    customer_email = db.Column(db.String(100))
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'total_amount': self.total_amount,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Routes
@app.route('/')
def index():
    return jsonify({
        'message': 'MegaStore API - All-in-One Shopping',
        'version': '1.0',
        'categories': ['electronics', 'fashion', 'home', 'books', 'sports', 'beauty', 'toys'],
        'endpoints': {
            'products': '/api/products',
            'orders': '/api/orders',
            'categories': '/api/categories'
        }
    })

@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    if category and category != 'all':
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Product.category).distinct().all()
    return jsonify([c[0] for c in categories])

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(
        name=data['name'],
        category=data['category'],
        price=data['price'],
        description=data['description'],
        icon=data.get('icon', '📦'),
        stock=data.get('stock', 0)
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders])

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(
        customer_name=data.get('customer_name'),
        customer_email=data.get('customer_email'),
        total_amount=data['total_amount'],
        status='pending'
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201

# Initialize database with sample data
def init_db():
    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:
            sample_products = [
                # Electronics
                Product(name='Macbook Air M4', category='electronics', price=125000,
                       description='High-performance laptop, M4, 512GB SSD',
                       icon='💻', stock=10),
                Product(name='iPhone 17 Pro', category='electronics', price=134900,
                       description='Latest iPhone with A19 Pro chip, 256GB storage',
                       icon='📱', stock=15),
                Product(name='Sony Headphones', category='electronics', price=24900,
                       description='Active noise cancellation, premium sound quality',
                       icon='🎧', stock=20),
                Product(name='4K Smart TV 55"', category='electronics', price=54999,
                       description='Ultra HD display, smart features, HDR support',
                       icon='📺', stock=8),
                
                # Fashion
                Product(name='Nike Running Shoes', category='fashion', price=8999,
                       description='Comfortable running shoes, all sizes available',
                       icon='👟', stock=30),
                Product(name='Levi\'s Denim Jacket', category='fashion', price=4999,
                       description='Classic denim jacket, premium quality fabric',
                       icon='🧥', stock=25),
                Product(name='Ray-Ban Sunglasses', category='fashion', price=12999,
                       description='Polarized lenses, UV protection, iconic style',
                       icon='🕶️', stock=15),
                Product(name='Leather Handbag', category='fashion', price=6999,
                       description='Genuine leather, spacious compartments',
                       icon='👜', stock=20),
                
                # Home & Living
                Product(name='Coffee Maker', category='home', price=8999,
                       description='Automatic coffee machine, 12-cup capacity',
                       icon='☕', stock=12),
                Product(name='Vacuum Cleaner', category='home', price=15999,
                       description='Powerful suction, HEPA filter, bagless design',
                       icon='🧹', stock=10),
                Product(name='Table Lamp', category='home', price=2999,
                       description='Modern design, adjustable brightness, LED',
                       icon='💡', stock=25),
                Product(name='Sofa Set 3-Seater', category='home', price=45999,
                       description='Comfortable fabric sofa, modern design',
                       icon='🛋️', stock=5),
                
                # Books
                Product(name='The Great Gatsby', category='books', price=499,
                       description='Classic novel by F. Scott Fitzgerald',
                       icon='📖', stock=50),
                Product(name='Atomic Habits', category='books', price=699,
                       description='Bestseller on building good habits',
                       icon='📕', stock=40),
                Product(name='Python Programming', category='books', price=899,
                       description='Complete guide to Python development',
                       icon='📘', stock=35),
                Product(name='Cookbook Collection', category='books', price=799,
                       description='500+ recipes from around the world',
                       icon='📗', stock=30),
                
                # Sports
                Product(name='Yoga Mat', category='sports', price=1499,
                       description='Non-slip, eco-friendly, 6mm thickness',
                       icon='🧘', stock=40),
                Product(name='Football', category='sports', price=1299,
                       description='Official size 5, durable synthetic leather',
                       icon='⚽', stock=35),
                Product(name='Dumbbells Set', category='sports', price=3999,
                       description='Adjustable weight, 2.5kg to 25kg',
                       icon='🏋️', stock=20),
                Product(name='Cricket Bat', category='sports', price=4999,
                       description='Kashmir willow, professional grade',
                       icon='🏏', stock=15),
                
                # Beauty
                Product(name='Face Cream', category='beauty', price=1999,
                       description='Anti-aging formula, SPF 30, all skin types',
                       icon='🧴', stock=50),
                Product(name='Lipstick Set', category='beauty', price=2499,
                       description='10 shades, matte finish, long-lasting',
                       icon='💄', stock=45),
                Product(name='Hair Straightener', category='beauty', price=3499,
                       description='Ceramic plates, adjustable temperature',
                       icon='🎀', stock=25),
                Product(name='Perfume', category='beauty', price=5999,
                       description='Premium fragrance, 100ml, long-lasting',
                       icon='🌸', stock=30),
                
                # Toys
                Product(name='LEGO Building Set', category='toys', price=4999,
                       description='1000+ pieces, creative building blocks',
                       icon='🧱', stock=20),
                Product(name='Teddy Bear', category='toys', price=1299,
                       description='Soft plush, huggable, 18 inches tall',
                       icon='🧸', stock=40),
                Product(name='Remote Control Car', category='toys', price=2999,
                       description='High-speed RC car, rechargeable battery',
                       icon='🚗', stock=25),
                Product(name='Board Game Set', category='toys', price=1999,
                       description='Family game collection, 5 games included',
                       icon='🎲', stock=30)
            ]
            for product in sample_products:
                db.session.add(product)
            db.session.commit()
            print("✓ MegaStore initialized with 28 products across 8 categories!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
