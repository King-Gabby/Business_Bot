import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { AdminLayout } from '../../components/admin/AdminLayout';
import { Plus, Trash2, Save, ShoppingBag } from 'lucide-react';
import axios from 'axios';

const ProductsManager: React.FC = () => {
  const { businessId } = useParams();
  const [products, setProducts] = useState<any>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchProducts();
  }, [businessId]);

  const fetchProducts = () => {
    axios.get(`http://localhost:8001/business/${businessId}`)
      .then(res => {
        setProducts(res.data.products || {});
        setLoading(false);
      })
      .catch(err => console.error(err));
  };

  const updateProduct = (key: string, field: string, value: string) => {
    setProducts({
      ...products,
      [key]: {
        ...products[key],
        [field]: value
      }
    });
  };

  const removeProduct = (key: string) => {
    const newProducts = { ...products };
    delete newProducts[key];
    setProducts(newProducts);
  };

  const addProduct = () => {
    const tempKey = 'new_product_' + Date.now();
    setProducts({
      ...products,
      [tempKey]: {
        display_name: 'New Product',
        price: '₦0',
        aliases: []
      }
    });
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await axios.put(`http://localhost:8001/business/${businessId}`, {
        products: products
      });
      alert('Products updated successfully!');
    } catch (err) {
      alert('Failed to update products.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="p-8">Loading products...</div>;

  return (
    <AdminLayout>
      <header className="flex justify-between items-end mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Products</h1>
          <p className="text-gray-500 mt-1">Manage your inventory and bot pricing.</p>
        </div>
        <div className="flex gap-3">
          <button 
            onClick={addProduct}
            className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-all font-medium text-sm"
          >
            <Plus size={18} />
            Add Product
          </button>
          <button 
            onClick={handleSave}
            disabled={saving}
            className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all font-bold text-sm shadow-md disabled:opacity-50"
          >
            <Save size={18} />
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </header>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <table className="w-full text-left">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-100">
              <th className="px-6 py-4 text-xs font-bold text-gray-400 uppercase tracking-wider">Product Display Name</th>
              <th className="px-6 py-4 text-xs font-bold text-gray-400 uppercase tracking-wider">Price (incl. Currency)</th>
              <th className="px-6 py-4 text-xs font-bold text-gray-400 uppercase tracking-wider text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {Object.entries(products).map(([key, p]: [string, any]) => (
              <tr key={key} className="hover:bg-gray-50/50 transition-colors">
                <td className="px-6 py-4">
                  <input 
                    type="text" 
                    value={p.display_name}
                    onChange={(e) => updateProduct(key, 'display_name', e.target.value)}
                    className="w-full bg-transparent border-none focus:ring-0 font-medium text-gray-800"
                  />
                </td>
                <td className="px-6 py-4">
                  <input 
                    type="text" 
                    value={p.price}
                    onChange={(e) => updateProduct(key, 'price', e.target.value)}
                    className="bg-transparent border-none focus:ring-0 text-blue-600 font-bold"
                  />
                </td>
                <td className="px-6 py-4 text-right">
                  <button 
                    onClick={() => removeProduct(key)}
                    className="p-2 text-gray-300 hover:text-red-500 transition-colors"
                  >
                    <Trash2 size={18} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {Object.keys(products).length === 0 && (
          <div className="p-20 text-center">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4 text-gray-400">
              <ShoppingBag size={24} />
            </div>
            <p className="text-gray-500">No products added yet.</p>
          </div>
        )}
      </div>
    </AdminLayout>
  );
};

export default ProductsManager;
