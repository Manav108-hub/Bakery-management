from flask import Blueprint, jsonify, request
from src.models.models import Product, Order
from src.extension import db
from src.app import db
import pika

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'description': p.description
    } for p in products])

@api_blueprint.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(product_id=data['product_id'])
    db.session.add(new_order)
    db.session.commit()
    
    # Send to RabbitMQ
    connection = pika.BlockingConnection(
        pika.URLParameters('amqp://rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='orders')
    channel.basic_publish(
        exchange='',
        routing_key='orders',
        body=str(new_order.id))
    connection.close()
    
    return jsonify({
        'id': new_order.id,
        'status': new_order.status
    }), 201

@api_blueprint.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({
        'id': order.id,
        'product_id': order.product_id,
        'status': order.status,
        'created_at': order.created_at.isoformat()
    })