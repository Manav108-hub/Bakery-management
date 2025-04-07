// src/index.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css'
import App from './App.jsx';
import { AuthProvider } from './components/context/AuthContext';
import { BrowserRouter } from 'react-router-dom'; // Import BrowserRouter

const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AuthProvider>
      <BrowserRouter> {/* Wrap App with BrowserRouter */}
        <App />
      </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>
);