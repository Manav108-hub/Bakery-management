// src/components/landing/LandingPage.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

const LandingPage = ({ setActiveTab }) => {
  return (
    <div className="text-center py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl mb-8">
          Welcome to The Bread Basket
        </h1>
        
        <div className="mb-12">
          <img 
            src="https://images.unsplash.com/photo-1509440159596-0249088772ff?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80" 
            alt="Fresh bread" 
            className="rounded-lg shadow-xl mx-auto h-64 object-cover"
          />
        </div>

        <div className="text-lg text-gray-600 mb-12 space-y-4">
          <p className="text-xl">
            🥖 Artisanal Breads Crafted with Love 🥐
          </p>
          <p>
            Since 1995, we've been baking traditional breads using time-honored recipes and 
            the finest natural ingredients. Our passion for perfect crust and fluffy interior 
            makes every loaf a masterpiece.
          </p>
          <div className="flex justify-center items-center gap-4 text-gray-700">
            <span>★ Fresh Daily ★</span>
            <span>★ Organic Ingredients ★</span>
            <span>★ Family Owned ★</span>
          </div>
        </div>

        <button
          onClick={() => setActiveTab('products')}
          className="bg-amber-600 hover:bg-amber-700 text-white font-bold py-3 px-8 rounded-full 
                     transition-all duration-300 transform hover:scale-105"
        >
          Shop Now →
        </button>
      </div>
    </div>
  );
};

export default LandingPage;