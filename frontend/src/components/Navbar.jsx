import { useAuth } from './context/AuthContext';
import { ChevronDownIcon } from '@heroicons/react/24/outline';
import { Fragment } from 'react';
import { Menu, Transition } from '@headlessui/react';

export default function Navbar({ activeTab, setActiveTab }) {
  const { user, logout, loading } = useAuth();

  if (loading) {
    return <div className="h-16 bg-gradient-to-r from-indigo-600 to-blue-500 animate-pulse"></div>;
  }

  const handleTabClick = (tab) => {
    const protectedTabs = ['cart', 'orders', 'profile'];
    const adminTabs = ['admin'];
    
    if (protectedTabs.includes(tab) && !user) {
      setActiveTab('login');
      return;
    }
    
    if (adminTabs.includes(tab) && (!user || !user.is_admin)) {
      setActiveTab('products');
      return;
    }
    
    setActiveTab(tab);
  };

  return (
    <nav className="bg-gradient-to-r from-indigo-600 to-blue-500 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div 
              className="flex-shrink-0 text-white text-2xl font-bold cursor-pointer"
              onClick={() => handleTabClick('home')}
            >
              The Bread Basket
            </div>
            <div className="hidden md:block ml-10 flex space-x-4">
              {/* Home */}
              <button
                onClick={() => handleTabClick('home')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === 'home' 
                    ? 'bg-blue-700 text-white' 
                    : 'text-white hover:bg-blue-600 hover:bg-opacity-75'
                }`}
              >
                Home
              </button>

              {/* Products */}
              <button
                onClick={() => handleTabClick('products')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === 'products' 
                    ? 'bg-blue-700 text-white' 
                    : 'text-white hover:bg-blue-600 hover:bg-opacity-75'
                }`}
              >
                Products
              </button>

              {/* Cart */}
              <button
                onClick={() => handleTabClick('cart')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === 'cart' 
                    ? 'bg-blue-700 text-white' 
                    : 'text-white hover:bg-blue-600 hover:bg-opacity-75'
                }`}
              >
                Cart
              </button>

              {/* Orders */}
              <button
                onClick={() => handleTabClick('orders')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  activeTab === 'orders' 
                    ? 'bg-blue-700 text-white' 
                    : 'text-white hover:bg-blue-600 hover:bg-opacity-75'
                }`}
              >
                Orders
              </button>

              {/* Admin Section */}
              {user?.is_admin && (
                <button
                  onClick={() => handleTabClick('admin')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    activeTab === 'admin' 
                      ? 'bg-blue-700 text-white' 
                      : 'text-white hover:bg-blue-600 hover:bg-opacity-75'
                  }`}
                  >
                  Admin
                </button>
              )}
            </div>
          </div>

          <div className="hidden md:block">
            <div className="ml-4 flex items-center md:ml-6">
              {user ? (
                <Menu as="div" className="ml-3 relative">
                  <div>
                    <Menu.Button className="max-w-xs bg-blue-700 rounded-full flex items-center text-sm text-white p-2 hover:bg-blue-800">
                      <span className="sr-only">Open user menu</span>
                      <span className="px-2">{user.username}</span>
                      <ChevronDownIcon className="h-4 w-4" aria-hidden="true" />
                    </Menu.Button>
                  </div>
                  <Transition
                    as={Fragment}
                    enter="transition ease-out duration-100"
                    enterFrom="transform opacity-0 scale-95"
                    enterTo="transform opacity-100 scale-100"
                    leave="transition ease-in duration-75"
                    leaveFrom="transform opacity-100 scale-100"
                    leaveTo="transform opacity-0 scale-95"
                  >
                    <Menu.Items className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
                      <Menu.Item>
                        {({ active }) => (
                          <button
                            onClick={() => handleTabClick('profile')}
                            className={`${
                              active ? 'bg-gray-100' : ''
                            } block px-4 py-2 text-sm text-gray-700 w-full text-left`}
                          >
                            Profile
                          </button>
                        )}
                      </Menu.Item>
                      <Menu.Item>
                        {({ active }) => (
                          <button
                            onClick={() => {
                              logout();
                              setActiveTab('products');
                            }}
                            className={`${
                              active ? 'bg-gray-100' : ''
                            } block px-4 py-2 text-sm text-gray-700 w-full text-left`}
                          >
                            Logout
                          </button>
                        )}
                      </Menu.Item>
                    </Menu.Items>
                  </Transition>
                </Menu>
              ) : (
                <div className="flex space-x-4">
                  <button
                    onClick={() => handleTabClick('login')}
                    className="px-3 py-2 rounded-md text-sm font-medium text-white hover:bg-blue-600 hover:bg-opacity-75"
                  >
                    Login
                  </button>
                  <button
                    onClick={() => handleTabClick('register')}
                    className="px-3 py-2 rounded-md text-sm font-medium text-white bg-blue-700 hover:bg-blue-800"
                  >
                    Register
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}