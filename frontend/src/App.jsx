// src/App.jsx (no directory changes)
import { useState, useEffect } from 'react';
import { useAuth } from './components/context/AuthContext';
import Navbar from './components/Navbar';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import ProductForm from './components/products/ProductForm';
import Cart from './components/cart/CartList';
import OrderItem from './components/orders/OrderItem';
import { toast } from 'react-hot-toast';
import ProductList from './components/products/ProductList';
import LandingPage from './components/loading/LandingPage';

function App() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('home');
  const protectedTabs = ['cart', 'orders', 'admin'];

  useEffect(() => {
    if (!user && protectedTabs.includes(activeTab)) {
      setActiveTab('login');
    }
  }, [user, activeTab]);

  const renderContent = () => {
    switch (activeTab) {
      case 'home':
        return <LandingPage setActiveTab={setActiveTab} />;
      case 'login':
        return <Login onSuccess={() => {
          setActiveTab('home');
          toast.success('Logged in successfully!');
        }} />;
      case 'register':
        return <Register onSuccess={() => {
          setActiveTab('login');
          toast.success('Registration successful! Please login.');
        }} />;
      case 'products':
        return <ProductList />;
      case 'cart':
        return user ? <Cart /> : toast.error('Please login to view cart');
      case 'product-form':
        return user?.is_admin ? <ProductForm /> : toast.error('Admin access required');
      case 'orders':
        return user ? <OrderItem /> : toast.error('Please login to view orders');
      default:
        return <LandingPage setActiveTab={setActiveTab} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-7xl mx-auto">
          {renderContent()}
        </div>
      </main>
    </div>
  );
}

export default App;