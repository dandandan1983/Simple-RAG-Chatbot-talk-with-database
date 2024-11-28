// src/components/ui/card.jsx

import React from 'react';

export const Card = ({ className, children }) => {
  return (
    <div className={`bg-white shadow-md rounded-lg p-4 ${className}`}>
      {children}
    </div>
  );
};

export const CardHeader = ({ children }) => {
  return <div className="border-b pb-2 mb-4">{children}</div>;
};

export const CardContent = ({ children }) => {
  return <div className="flex-1">{children}</div>;
};

export const CardTitle = ({ children, className }) => {
  return <h2 className={`text-xl font-semibold ${className}`}>{children}</h2>;
};
