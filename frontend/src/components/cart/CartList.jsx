import { useEffect, useState } from 'react';
import api from '../services/api';
import CartItem from './CartItem';

export default function CartList() {
  const [cartItems, setCartItems] = useState([]);

  useEffect(() => {
    const fetchCart = async () => {
      try {
        const { data } = await api.get('/cart');
        setCartItems(data);
      } catch (error) {
        console.error('Failed to fetch cart', error);
      }
    };
    fetchCart();
  }, []);

  return (
    <div className="max-w-2xl mx-auto mt-8">
      <h2 className="text-2xl font-bold mb-4">Your Cart</h2>
      {cartItems.map(item => (
        <CartItem key={item.id} item={item} />
      ))}
    </div>
  );
}