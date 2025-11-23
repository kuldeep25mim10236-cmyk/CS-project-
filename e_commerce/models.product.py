from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    """Product model for storing product information"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(10), default='📦')
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        """Convert product object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'description': self.description,
            'icon': self.icon,
            'stock': self.stock,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_all_products():
        """Get all products"""
        return Product.query.all()
    
    @staticmethod
    def get_by_id(product_id):
        """Get product by ID"""
        return Product.query.get(product_id)
    
    @staticmethod
    def get_by_category(category):
        """Get products by category"""
        return Product.query.filter_by(category=category).all()
    
    @staticmethod
    def search_products(search_term):
        """Search products by name or description"""
        search = f"%{search_term}%"
        return Product.query.filter(
            (Product.name.ilike(search)) | 
            (Product.description.ilike(search))
        ).all()
