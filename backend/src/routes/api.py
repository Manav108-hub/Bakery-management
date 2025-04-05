from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.models import Product, Order, User, db
import pika
import os
from sqlalchemy.exc import SQLAlchemyError

api_blueprint = Blueprint('api', __name__)

def make_error_response(message, status_code):
    return jsonify({"error": message}), status_code

# Product Endpoints
@api_blueprint.route('/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        products = Product.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'description': p.description,
            'stock': p.stock
        } for p in products])
    except SQLAlchemyError:
        return make_error_response("Database error", 500)

@api_blueprint.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID"""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'description': product.description,
            'stock': product.stock
        })
    except SQLAlchemyError:
        return make_error_response("Database error", 500)

@api_blueprint.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    """Add new product (Admin only)"""
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return make_error_response("Unauthorized", 403)
    
    try:
        data = request.get_json()
        required_fields = ['name', 'price', 'stock']
        if not all(field in data for field in required_fields):
            return make_error_response(f"Missing required fields: {required_fields}", 400)

        if Product.query.filter_by(name=data['name']).first():
            return make_error_response("Product name already exists", 409)

        try:
            new_product = Product(
                name=data['name'],
                price=float(data['price']),
                description=data.get('description', ''),
                stock=int(data['stock'])
            )
            db.session.add(new_product)
            db.session.commit()
            
            return jsonify({
                'id': new_product.id,
                'name': new_product.name,
                'price': float(new_product.price),
                'description': new_product.description,
                'stock': new_product.stock
            }), 201
        except ValueError:
            return make_error_response("Invalid price or stock format", 400)
    except SQLAlchemyError:
        db.session.rollback()
        return make_error_response("Database error", 500)

# Order Endpoints
@api_blueprint.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user's orders"""
    current_user = get_jwt_identity()
    try:
        orders = Order.query.filter_by(user_id=current_user['id']).all()
        return jsonify([{
            'id': o.id,
            'product': {
                'id': o.product.id,
                'name': o.product.name,
                'price': float(o.product.price)
            },
            'quantity': o.quantity,
            'status': o.status,
            'created_at': o.created_at.isoformat()
        } for o in orders])
    except SQLAlchemyError:
        return make_error_response("Database error", 500)

@api_blueprint.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get specific order"""
    current_user = get_jwt_identity()
    try:
        order = Order.query.filter_by(id=order_id, user_id=current_user['id']).first_or_404()
        return jsonify({
            'id': order.id,
            'product': {
                'id': order.product.id,
                'name': order.product.name,
                'price': float(order.product.price),
                'description': order.product.description
            },
            'quantity': order.quantity,
            'status': order.status,
            'created_at': order.created_at.isoformat()
        })
    except SQLAlchemyError:
        return make_error_response("Database error", 500)

@api_blueprint.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    """Create new order"""
    current_user = get_jwt_identity()
    try:
        data = request.get_json()
        required_fields = ['product_id', 'quantity']
        if not all(field in data for field in required_fields):
            return make_error_response(f"Missing required fields: {required_fields}", 400)

        product = Product.query.get(data['product_id'])
        if not product:
            return make_error_response("Product not found", 404)
            
        if product.stock < data['quantity']:
            return make_error_response("Insufficient stock", 400)

        new_order = Order(
            product_id=product.id,
            user_id=current_user['id'],
            quantity=data['quantity'],
            status='pending'
        )
        
        product.stock -= new_order.quantity
        db.session.add(new_order)
        db.session.commit()

        # RabbitMQ integration
        try:
            connection = pika.BlockingConnection(
                pika.URLParameters(os.getenv('RABBITMQ_URL', 'amqp://localhost')))
            channel = connection.channel()
            channel.queue_declare(queue='orders', durable=True)
            channel.basic_publish(
                exchange='',
                routing_key='orders',
                body=str(new_order.id),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    headers={'user_id': current_user['id']}
                )
            )
            connection.close()
        except Exception as e:
            print(f"RabbitMQ Error: {str(e)}")

        return jsonify({
            'id': new_order.id,
            'product_id': new_order.product_id,
            'quantity': new_order.quantity,
            'status': new_order.status,
            'created_at': new_order.created_at.isoformat()
        }), 201
    except SQLAlchemyError:
        db.session.rollback()
        return make_error_response("Database error", 500)
    
