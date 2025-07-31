import React, { useState } from 'react';

const ImageTest: React.FC = () => {
  const [imageStatus, setImageStatus] = useState<{[key: string]: string}>({});
  
  const testImages = [
    'https://m.media-amazon.com/images/I/81vF8pFhOGL._AC_SX679_.jpg',
    'https://m.media-amazon.com/images/I/71qJzK9mOFL._AC_SX679_.jpg',
    '/placeholder-deal.svg'
  ];
  
  const handleImageLoad = (url: string) => {
    setImageStatus(prev => ({ ...prev, [url]: 'loaded' }));
  };
  
  const handleImageError = (url: string) => {
    setImageStatus(prev => ({ ...prev, [url]: 'error' }));
  };
  
  return (
    <div className="p-4 bg-red-100 border border-red-300 rounded mb-4">
      <h3 className="font-bold mb-2">Image Loading Test</h3>
      {testImages.map((url, index) => (
        <div key={index} className="mb-2 flex items-center gap-2">
          <img 
            src={url}
            alt={`Test ${index}`}
            className="w-16 h-16 object-contain border"
            onLoad={() => handleImageLoad(url)}
            onError={() => handleImageError(url)}
          />
          <div className="text-sm">
            <div>Status: {imageStatus[url] || 'loading'}</div>
            <div className="text-xs text-gray-600">{url}</div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ImageTest;