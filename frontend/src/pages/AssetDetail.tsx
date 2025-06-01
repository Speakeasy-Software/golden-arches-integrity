import React from 'react';
import { useParams } from 'react-router-dom';

export default function AssetDetail() {
  const { id } = useParams<{ id: string }>();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Asset Detail</h1>
        <p className="text-gray-600 mt-1">
          Viewing details for asset ID: {id}
        </p>
      </div>
      
      <div className="card">
        <div className="card-content">
          <p className="text-gray-500 text-center py-8">
            Asset detail page coming soon...
          </p>
        </div>
      </div>
    </div>
  );
} 