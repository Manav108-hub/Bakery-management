// src/components/products/ProductForm.jsx
import { useState } from 'react';
import { createProduct } from '../services/api'; // Correct import

export default function ProductForm() {
  const [formData, setFormData] = useState({
    name: '',
    price: 0,
    description: '',
    stock: 0
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createProduct(formData);
      alert('Product created!');
    } catch (error) {
      alert('Failed to create product');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="name"
        value={formData.name}
        onChange={(e) => setFormData({...formData, name: e.target.value})}
        placeholder="Product name"
        required
      />
      <input
        name="price"
        type="number"
        value={formData.price}
        onChange={(e) => setFormData({...formData, price: e.target.value})}
        placeholder="Price"
        required
      />
      <textarea
        name="description"
        value={formData.description}
        onChange={(e) => setFormData({...formData, description: e.target.value})}
        placeholder="Description"
      />
      <input
        name="stock"
        type="number"
        value={formData.stock}
        onChange={(e) => setFormData({...formData, stock: e.target.value})}
        placeholder="Stock"
      />
      <button type="submit">Create Product</button>
    </form>
  );
}