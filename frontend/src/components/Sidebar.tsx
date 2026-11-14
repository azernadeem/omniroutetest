import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Activity,
  Wallet,
  List,
  BarChart2,
  GitMerge,
  Mail,
  AlertTriangle,
  Bot,
  Settings,
  TrendingUp,
  TrendingDown,
  Menu,
  Search
} from 'lucide-react';

const navItems = [
  { name: 'Overview', path: '/overview', icon: LayoutDashboard },
  { name: 'Markets', path: '/markets', icon: Activity },
  { name: 'Coin Explorer', path: '/coin-explorer', icon: Search },
  { name: 'Portfolio', path: '/portfolio', icon: Wallet },
  { name: 'Watchlists', path: '/watchlists', icon: List },
  { name: 'Technical Analysis', path: '/technical-analysis', icon: Activity },
  { name: 'Market Analytics', path: '/market-analytics', icon: BarChart2 },
  { name: 'Correlation Analysis', path: '/correlation', icon: GitMerge },
  { name: 'News & Sentiment', path: '/news', icon: Mail },
  { name: 'Alerts', path: '/alerts', icon: AlertTriangle },
  { name: 'AI Assistant', path: '/ai-assistant', icon: Bot },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-gray-800 border-r border-gray-700 flex flex-col h-screen shrink-0">
      <div className="p-4 flex items-center gap-2 border-b border-gray-700">
        <div className="w-8 h-8 bg-gradient-to-br from-positive to-negative rounded-lg flex items-center justify-center">
          <TrendingUp className="w-5 h-5 text-white" />
        </div>
        <span className="font-bold text-xl tracking-tight">OmniRoute</span>
      </div>
      <nav className="flex-1 overflow-y-auto p-2 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                }`
              }
            >
              <Icon className="w-5 h-5" />
              {item.name}
            </NavLink>
          );
        })}
      </nav>
      <div className="p-4 border-t border-gray-700">
        <button className="w-full flex items-center gap-3 px-3 py-2 rounded-md text-gray-300 hover:bg-gray-700 hover:text-white transition-colors">
          <Menu className="w-5 h-5" />
          Collapse
        </button>
      </div>
    </aside>
  );
}