import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { AdminLayout } from '../../components/admin/AdminLayout';
import { Save } from 'lucide-react';
import axios from 'axios';

const SettingsManager: React.FC = () => {
  const { businessId } = useParams();
  const [config, setConfig] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    axios.get(`http://localhost:8001/business/${businessId}`)
      .then(res => {
        setConfig(res.data);
        setLoading(false);
      })
      .catch(err => console.error(err));
  }, [businessId]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await axios.put(`http://localhost:8001/business/${businessId}`, {
        name: config.name,
        contact: config.contact,
        delivery: config.delivery
      });
      alert('Settings updated successfully!');
    } catch (err) {
      alert('Failed to update settings.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="p-8">Loading settings...</div>;

  return (
    <AdminLayout>
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-500 mt-1">Configure your business identity and delivery info.</p>
      </header>

      <form onSubmit={handleSave} className="max-w-2xl bg-white p-8 rounded-2xl shadow-sm border border-gray-100 space-y-8">
        <div className="space-y-2">
          <label className="text-sm font-bold text-gray-700">Business Name</label>
          <input 
            type="text" 
            value={config.name}
            onChange={(e) => setConfig({...config, name: e.target.value})}
            className="w-full p-4 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-blue-500 outline-none text-gray-800"
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-bold text-gray-700">WhatsApp Contact Number</label>
          <input 
            type="text" 
            value={config.contact}
            onChange={(e) => setConfig({...config, contact: e.target.value})}
            className="w-full p-4 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-blue-500 outline-none text-gray-800"
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-bold text-gray-700">Delivery Information</label>
          <textarea 
            rows={3}
            value={config.delivery}
            onChange={(e) => setConfig({...config, delivery: e.target.value})}
            className="w-full p-4 bg-gray-50 border-none rounded-xl focus:ring-2 focus:ring-blue-500 outline-none text-gray-800"
          />
        </div>

        <button 
          type="submit"
          disabled={saving}
          className="w-full flex items-center justify-center gap-2 py-4 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all font-bold shadow-md active:scale-95 disabled:opacity-50"
        >
          <Save size={18} />
          {saving ? 'Saving...' : 'Save Settings'}
        </button>
      </form>
    </AdminLayout>
  );
};

export default SettingsManager;
