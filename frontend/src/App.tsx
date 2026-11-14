import { useEffect, useState, PropsWithChildren } from 'react';
import { useLocation, Navigate } from 'react-router-dom';
import Sidebar from '@/components/Sidebar';
import ThemeToggle from '@/components/ThemeToggle';

const App = ({ children }: PropsWithChildren) => {
  const [darkMode, setDarkMode] = useState(true);
  const location = useLocation();

  useEffect(() => {
    const stored = localStorage.getItem('theme');
    if (stored) setDarkMode(stored === 'dark');
  }, []);

  useEffect(() => {
    const root = window.document.documentElement;
    if (darkMode) {
      root.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      root.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  if (location.pathname === '/') {
    return <Navigate to="/overview" replace />;
  }

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="flex justify-end p-4 bg-gray-800/50 border-b border-gray-700">
          <ThemeToggle darkMode={darkMode} setDarkMode={setDarkMode} />
        </header>
        <main className="flex-1 overflow-y-auto p-4">
          {children}
        </main>
      </div>
    </div>
  );
};

export default App;