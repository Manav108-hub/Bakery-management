export default function CartItem({ item }) {
    return (
      <div className="flex justify-between items-center p-4 border-b">
        <div>
          <h3 className="font-semibold">{item.product.name}</h3>
          <p>Quantity: {item.quantity}</p>
          <p>Price: ${(item.product.price * item.quantity).toFixed(2)}</p>
        </div>
      </div>
    );
  }