import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Store, ArrowRight, CheckCircle2 } from 'lucide-react';
import axios from 'axios';

const BusinessOnboarding: React.FC = () => {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    business_name: '',
    contact: '',
    categories: '',
    currency: '₦'
  });
  const [result, setResult] = useState<any>(null);
  const navigate = useNavigate();

  const handleCreate = async () => {
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8001/create-business', {
        ...formData,
        categories: formData.categories.split(',').map(c => c.trim())
      });
      setResult(res.data);
      setStep(2);
    } catch (err) {
      alert('Failed to create business.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-xl p-10">
        <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center text-white mb-8 mx-auto shadow-lg shadow-blue-200">
          <Store size={24} />
        </div>

        {step === 1 ? (
          <>
            <div className="text-center mb-10">
              <h1 className="text-2xl font-bold text-gray-900">Create your AI Store</h1>
              <p className="text-gray-500 mt-2">Start selling automatically in minutes.</p>
            </div>

            <div className="space-y-6">
              <div className="space-y-2">
                <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Business Name</label>
                <input 
                  type="text" 
                  placeholder="e.g. Rae Glow Skincare"
                  value={formData.business_name}
                  onChange={(e) => setFormData({...formData, business_name: e.target.value})}
                  className="w-full p-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none text-gray-800 transition-all"
                />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">WhatsApp Number</label>
                <input 
                  type="text" 
                  placeholder="+234..."
                  value={formData.contact}
                  onChange={(e) => setFormData({...formData, contact: e.target.value})}
                  className="w-full p-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none text-gray-800 transition-all"
                />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Categories (comma separated)</label>
                <input 
                  type="text" 
                  placeholder="perfumes, lipsticks"
                  value={formData.categories}
                  onChange={(e) => setFormData({...formData, categories: e.target.value})}
                  className="w-full p-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-blue-500 outline-none text-gray-800 transition-all"
                />
              </div>

              <button 
                onClick={handleCreate}
                disabled={!formData.business_name || loading}
                className="w-full flex items-center justify-center gap-2 py-4 bg-gray-900 text-white rounded-2xl hover:bg-black transition-all font-bold shadow-lg active:scale-95 disabled:opacity-50 mt-4"
              >
                {loading ? 'Creating...' : 'Get Started'}
                <ArrowRight size={18} />
              </button>
            </div>
          </>
        ) : (
          <div className="text-center animate-in fade-in zoom-in duration-300">
            <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckCircle2 size={32} />
            </div>
            <h1 className="text-2xl font-bold text-gray-900">Your bot is live! 🎉</h1>
            <p className="text-gray-500 mt-2 mb-8">
              Business ID: <span className="font-bold text-blue-600">{result.business_id}</span>
            </p>

            <div className="space-y-3">
              <button 
                onClick={() => navigate(`/admin/${result.business_id}`)}
                className="w-full py-4 bg-blue-600 text-white rounded-2xl hover:bg-blue-700 transition-all font-bold shadow-md shadow-blue-100"
              >
                Go to Dashboard
              </button>
              <button 
                onClick={() => navigate(`/chat/${result.business_id}`)}
                className="w-full py-4 bg-gray-100 text-gray-700 rounded-2xl hover:bg-gray-200 transition-all font-bold"
              >
                Try the Bot
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BusinessOnboarding;
