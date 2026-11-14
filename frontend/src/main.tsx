import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from '@/App';
import Overview from '@/pages/Overview';
import Markets from '@/pages/Markets';
import CoinExplorer from '@/pages/CoinExplorer';
import Portfolio from '@/pages/Portfolio';
import Settings from '@/pages/Settings';
import '@/index.css';

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App>
          <Routes>
            <Route index element={<Overview />} />
            <Route path="overview" element={<Overview />} />
            <Route path="markets" element={<Markets />} />
            <Route path="coin-explorer" element={<CoinExplorer />} />
            <Route path="portfolio" element={<Portfolio />} />
            <Route path="settings" element={<Settings />} />
          </Routes>
        </App>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
);