from flask import Blueprint, request, jsonify
from models.order import Order
# Create blueprint
orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@orders_bp.route('/', methods=['GET'])
def get_orders():
    """Get all orders or filter by status"""
    try:
        status = request.args.get('status')
        email = request.args.get('email')
        
        if email:
            orders = Order.get_by_customer_email(email)
        elif status:
            orders = Order.get_by_status(status)
        else:
            orders = Order.get_all_orders()
        
        return jsonify({
            'success': True,
            'count': len(orders),
            'orders': [o.to_dict() for o in orders]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get single order by ID"""
    try:
        order = Order.get_by_id(order_id)
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404
        
        return jsonify({
            'success': True,
            'order': order.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orders_bp.route('/', methods=['POST'])
def create_order():
    """Create new order"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'total_amount' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: total_amount'
            }), 400
        
        # Create order
        order = Order(
            customer_name=data.get('customer_name'),
            customer_email=data.get('customer_email'),
            customer_phone=data.get('customer_phone'),
            total_amount=data['total_amount'],
            status=data.get('status', 'pending'),
            payment_method=data.get('payment_method', 'cash'),
            shipping_address=data.get('shipping_address')
        )
        order.save()
        
        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orders_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Update existing order"""
    try:
        order = Order.get_by_id(order_id)
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404
        
        data = request.get_json()
        order.update(**data)
        
        return jsonify({
            'success': True,
            'message': 'Order updated successfully',
            'order': order.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orders_bp.route('/<int:order_id>/status', methods=['PATCH'])
def update_order_status(order_id):
    """Update order status"""
    try:
        order = Order.get_by_id(order_id)
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404
        
        data = request.get_json()
        if 'status' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: status'
            }), 400
        
        success = order.update_status(data['status'])
        if not success:
            return jsonify({
                'success': False,
                'error': 'Invalid status value'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Order status updated successfully',
            'order': order.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@orders_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete order"""
    try:
        order = Order.get_by_id(order_id)
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404
        
        order.delete()
        
        return jsonify({
            'success': True,
            'message': 'Order deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
