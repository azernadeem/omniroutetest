import { lazy } from 'react';
import { Route, Routes as RouterRoutes } from 'react-router-dom';

const Overview = lazy(() => import('@/pages/Overview'));
const Markets = lazy(() => import('@/pages/Markets'));
const CoinExplorer = lazy(() => import('@/pages/CoinExplorer'));
const Portfolio = lazy(() => import('@/pages/Portfolio'));
const Settings = lazy(() => import('@/pages/Settings'));

export default function AppRoutes() {
  return (
    <RouterRoutes>
      <Route path="overview" element={<Overview />} />
      <Route path="markets" element={<Markets />} />
      <Route path="coin-explorer" element={<CoinExplorer />} />
      <Route path="portfolio" element={<Portfolio />} />
      <Route path="settings" element={<Settings />} />
    </RouterRoutes>
  );
}