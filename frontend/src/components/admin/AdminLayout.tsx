import React from 'react';
import { NavLink, useParams } from 'react-router-dom';
import { LayoutDashboard, ShoppingBag, Settings, Store, ExternalLink } from 'lucide-react';

export const AdminLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { businessId } = useParams();

  const navItems = [
    { to: `/admin/${businessId}`, icon: LayoutDashboard, label: 'Dashboard' },
    { to: `/admin/${businessId}/products`, icon: ShoppingBag, label: 'Products' },
    { to: `/admin/${businessId}/settings`, icon: Settings, label: 'Settings' },
  ];

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-6 border-b border-gray-100 flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white">
            <Store size={18} />
          </div>
          <span className="font-bold text-gray-800">Store Admin</span>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
                  isActive 
                    ? 'bg-blue-50 text-blue-600' 
                    : 'text-gray-500 hover:bg-gray-50 hover:text-gray-700'
                }`
              }
            >
              <item.icon size={18} />
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-gray-100">
          <a
            href={`/chat/${businessId}`}
            target="_blank"
            rel="noreferrer"
            className="flex items-center justify-between w-full px-4 py-3 bg-gray-900 text-white rounded-xl text-xs font-medium hover:bg-gray-800 transition-colors"
          >
            View Live Bot
            <ExternalLink size={14} />
          </a>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <div className="p-8 max-w-5xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
};
