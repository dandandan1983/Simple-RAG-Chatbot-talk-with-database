// src/components/ui/alert.jsx

import React from 'react';

export const Alert = ({ children, className }) => {
  return (
    <div className={`bg-yellow-100 text-yellow-800 border-l-4 border-yellow-500 p-4 ${className}`}>
      {children}
    </div>
  );
};

export const AlertDescription = ({ children }) => {
  return <div className="mt-2">{children}</div>;
};
