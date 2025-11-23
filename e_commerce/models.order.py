from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Order(db.Model):
    """Order model for storing order information"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    customer_email = db.Column(db.String(100))
    customer_phone = db.Column(db.String(20))
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, cancelled
    payment_method = db.Column(db.String(50), default='cash')
    shipping_address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Order {self.id} - {self.customer_name}>'
    
    def to_dict(self):
        """Convert order object to dictionary"""
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'total_amount': self.total_amount,
            'status': self.status,
            'payment_method': self.payment_method,
            'shipping_address': self.shipping_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_all_orders():
        """Get all orders"""
        return Order.query.all()
    
    @staticmethod
    def get_by_id(order_id):
        """Get order by ID"""
        return Order.query.get(order_id)
    
    @staticmethod
    def get_by_status(status):
        """Get orders by status"""
        return Order.query.filter_by(status=status).all()
    
    @staticmethod
    def get_by_customer_email(email):
        """Get orders by customer email"""
        return Order.query.filter_by(customer_email=email).all()
    
    def save(self):
        """Save order to database"""
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete order from database"""
        db.session.delete(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """Update order attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def update_status(self, new_status):
        """Update order status"""
        valid_statuses = ['pending', 'processing', 'completed', 'cancelled']
        if new_status in valid_statuses:
            self.status = new_status
            self.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        return False
