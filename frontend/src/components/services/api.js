// src/components/services/api.js
import axios from 'axios';

const baseURL = 'http://localhost:8000/api'; // Set your backend URL

const api = axios.create({
  baseURL: baseURL,
  withCredentials: true
});

// api.interceptors.request.use(config => {
//   const token = document.cookie
//     .split('; ')
//     .find(row => row.startsWith('token='))
//     ?.split('=')[1];

//   if (token) config.headers.Authorization = `Bearer ${token}`;
//   return config;
// });

// Function to create a product
export const createProduct = async (productData) => {
  try {
    const response = await api.post('/products', productData); // Assuming your product creation endpoint is /api/products
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default api;