import React, { Component } from "react";
import { createRoot } from 'react-dom/client';
import './i18n';
import App from './App';

// append app to dom
const root = createRoot(document.getElementById('root'));
root.render(
  <App />
);
