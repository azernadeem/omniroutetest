import { Sun, Moon } from 'lucide-react';

export default function ThemeToggle({ darkMode, setDarkMode }: { darkMode: boolean; setDarkMode: (v: boolean) => void }) {
  return (
    <button
      onClick={() => setDarkMode(!darkMode)}
      className="p-2 rounded-lg text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
      aria-label="Toggle theme"
    >
      {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
    </button>
  );
}