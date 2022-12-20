import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Innotter from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <Innotter />
  </React.StrictMode>
);
