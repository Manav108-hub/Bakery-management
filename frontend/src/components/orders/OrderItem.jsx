export default function OrderItem({ order }) {
    return (
      <div>
        <h3>Order #{order.id}</h3>
        <p>Product: {order.product_id}</p>
        <p>Quantity: {order.quantity}</p>
      </div>
    );
  }