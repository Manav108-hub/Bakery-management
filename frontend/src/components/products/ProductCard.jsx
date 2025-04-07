import { useAuth } from '../context/AuthContext';
import { useState } from 'react';
import api from '../services/api';
import { toast } from 'react-hot-toast';

export default function ProductCard({ product }) {
  const { user } = useAuth();
  const [isAdding, setIsAdding] = useState(false);
  const [quantity, setQuantity] = useState(1); // Default quantity to 1

  const handleAddToCart = async () => {
    if (!user) {
      return toast.error('Please login to add items to cart');
    }

    try {
      setIsAdding(true);
      const response = await api.post('/cart/add', {
        product_id: product.id,
        quantity: parseInt(quantity, 10), // Ensure quantity is an integer
      });

      if (!response.data.success) {
        throw new Error('Failed to add to cart');
      }

      toast.success(`${product.name} added to cart!`);
    } catch (error) {
      toast.error(error.message || 'Failed to add item');
    } finally {
      setIsAdding(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <div className="h-48 bg-gray-100 flex items-center justify-center relative">
        {product.image_url && (
          <img
            src={product.image_url}
            alt={product.name}
            className="max-h-full max-w-full object-contain"
          />
        )}
        {!product.image_url && (
          <div className="text-gray-400 text-sm">No image available</div>
        )}
      </div>
      <div className="p-4">
        <h3 className="font-semibold text-lg mb-2 line-clamp-2">{product.name}</h3>
        <p className="text-gray-600 mb-2">${product.price}</p>
        <p className="text-sm text-gray-500 mb-4 line-clamp-3">{product.description}</p>

        <div className="flex items-center mb-2">
          <label htmlFor={`quantity-${product.id}`} className="mr-2 text-sm text-gray-700">Qty:</label>
          <input
            type="number"
            id={`quantity-${product.id}`}
            className="w-16 border border-gray-300 rounded-md py-1 text-center text-sm"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            min="1"
          />
        </div>

        <button
          onClick={handleAddToCart}
          disabled={isAdding}
          className={`w-full py-2 px-4 rounded-md text-white transition-colors duration-200 ${
            isAdding
              ? 'bg-indigo-300 cursor-not-allowed'
              : 'bg-indigo-600 hover:bg-indigo-700'
          }`}
        >
          {isAdding ? 'Adding...' : 'Add to Cart'}
        </button>
      </div>
    </div>
  );
}