import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { AdminLayout } from '../../components/admin/AdminLayout';
import { MessageSquare, ShoppingCart, TrendingUp, Users } from 'lucide-react';
import axios from 'axios';

const AdminDashboard: React.FC = () => {
  const { businessId } = useParams();
  const [config, setConfig] = useState<any>(null);

  useEffect(() => {
    axios.get(`http://localhost:8001/business/${businessId}`)
      .then(res => setConfig(res.data))
      .catch(err => console.error(err));
  }, [businessId]);

  const stats = [
    { label: 'Total Chats', value: '128', icon: MessageSquare, color: 'bg-blue-500' },
    { label: 'Orders Started', value: '42', icon: ShoppingCart, color: 'bg-green-500' },
    { label: 'Customers', value: '89', icon: Users, color: 'bg-purple-500' },
    { label: 'Conv. Rate', value: '32%', icon: TrendingUp, color: 'bg-orange-500' },
  ];

  if (!config) return <div className="p-8">Loading dashboard...</div>;

  return (
    <AdminLayout>
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Welcome, {config.name}</h1>
        <p className="text-gray-500 mt-1">Here is how your AI assistant is performing today.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <div className="flex items-center gap-4">
              <div className={`${stat.color} p-3 rounded-xl text-white`}>
                <stat.icon size={24} />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-500">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Recent Activity</h2>
          <div className="space-y-6">
            {[1, 2, 3].map(i => (
              <div key={i} className="flex gap-4 items-start">
                <div className="w-2 h-2 mt-2 bg-blue-500 rounded-full" />
                <div>
                  <p className="text-sm font-medium text-gray-800">New order initiated for Shoes</p>
                  <p className="text-xs text-gray-400">2 minutes ago</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Bot Health</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Response Accuracy</span>
              <span className="text-sm font-bold text-green-600">98%</span>
            </div>
            <div className="w-full bg-gray-100 h-2 rounded-full overflow-hidden">
              <div className="bg-green-500 h-full w-[98%]" />
            </div>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

export default AdminDashboard;
