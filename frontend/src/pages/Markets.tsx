import { useState, useMemo } from 'react';
import { useCoins, useGainers, useLosers, useTrending } from '@/hooks/useMarketData';
import LoadingSpinner from '@/components/LoadingSpinner';
import { TrendingUp, TrendingDown, RefreshCw, Search, X } from 'lucide-react';

const formatNumber = (num: number | null | undefined): string => {
  if (num === null || num === undefined) return '—';
  if (num >= 1e9) return `$${(num / 1e9).toFixed(2)}B`;
  if (num >= 1e6) return `$${(num / 1e6).toFixed(2)}M`;
  if (num >= 1e3) return `$${(num / 1e3).toFixed(2)}K`;
  return `$${num.toFixed(2)}`;
};

const formatPercent = (num: number | null | undefined): string => {
  if (num === null || num === undefined) return '—';
  return `${num >= 0 ? '+' : ''}${num.toFixed(2)}%`;
};

const changeColor = (val: number | null | undefined): string => {
  if (val === null || val === undefined) return 'text-gray-400';
  return val >= 0 ? 'text-positive' : 'text-negative';
};

type SortKey = 'rank' | 'name' | 'price' | 'change24h' | 'volume';
type SortDirection = 'asc' | 'desc';

export default function Markets() {
  const [search, setSearch] = useState('');
  const [sortKey, setSortKey] = useState<SortKey>('rank');
  const [sortDir, setSortDir] = useState<SortDirection>('desc');
  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(20);

  const { data: coinsData, isLoading: coinsLoading, error: coinsError } = useCoins(page, perPage, search || undefined);
  const { data: trendingData, isLoading: trendingLoading } = useTrending();
  const { data: gainersData, isLoading: gainersLoading } = useGainers();
  const { data: losersData, isLoading: losersLoading } = useLosers();

  const coins = coinsData?.coins || [];
  const totalPages = Math.ceil((coinsData?.count || 0) / perPage);

  const sortedCoins = useMemo(() => {
    const sorted = [...coins];
    sorted.sort((a, b) => {
      let cmp = 0;
      switch (sortKey) {
        case 'rank':
          cmp = (a.symbol || '').localeCompare(b.symbol || '');
          break;
        case 'name':
          cmp = (a.name || '').localeCompare(b.name || '');
          break;
        case 'price':
          cmp = (a.price_usd ?? 0) - (b.price_usd ?? 0);
          break;
        case 'change24h':
          cmp = (a.change_24h ?? -9999) - (b.change_24h ?? -9999);
          break;
        case 'volume':
          cmp = (a.volume_24h_usd ?? 0) - (b.volume_24h_usd ?? 0);
          break;
      }
      return sortDir === 'asc' ? cmp : -cmp;
    });
    return sorted;
  }, [coins, sortKey, sortDir]);

  const toggleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir('asc');
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">Markets</h1>
          <p className="text-gray-400 text-sm">Search, filter, and sort cryptocurrency market data</p>
        </div>
        <div className="flex gap-2">
          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-white text-sm font-medium transition-colors">
            <RefreshCw className="w-4 h-4 inline mr-2" />
            Refresh
          </button>
        </div>
      </div>

      <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
        <form onSubmit={handleSearch} className="flex gap-2">
          <div className="flex-1 relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search coins..."
              className="w-full pl-9 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
            />
            {search && (
              <button
                type="button"
                onClick={() => setSearch('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
          <select
            value={perPage}
            onChange={(e) => { setPerPage(Number(e.target.value)); setPage(1); }}
            className="px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-sm text-white"
          >
            <option value={10}>10 per page</option>
            <option value={20}>20 per page</option>
            <option value={50}>50 per page</option>
          </select>
        </form>
      </div>

      {coinsLoading && (
        <div className="bg-gray-800 p-8 rounded-xl border border-gray-700 flex items-center justify-center">
          <LoadingSpinner />
        </div>
      )}

      {coinsError && (
        <div className="bg-gray-800 p-8 rounded-xl border border-gray-700 flex items-center justify-center text-red-400">
          Failed to load market data. Please try again.
        </div>
      )}

      {!coinsLoading && !coinsError && sortedCoins.length === 0 && (
        <div className="bg-gray-800 p-8 rounded-xl border border-gray-700 flex items-center justify-center text-gray-400">
          No coins found matching your criteria.
        </div>
      )}

      {!coinsLoading && !coinsError && sortedCoins.length > 0 && (
        <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-700/50">
                <tr>
                  {[
                    { key: 'rank', label: 'Rank', className: 'w-12' },
                    { key: 'name', label: 'Name', className: 'min-w-[140px]' },
                    { key: 'symbol', label: 'Symbol', className: 'min-w-[80px]' },
                    { key: 'price', label: 'Price', className: 'min-w-[120px]' },
                    { key: 'change1h', label: '1h', className: 'min-w-[80px]' },
                    { key: 'change24h', label: '24h', className: 'min-w-[90px]' },
                    { key: 'change7d', label: '7d', className: 'min-w-[90px]' },
                    { key: 'volume', label: 'Volume', className: 'min-w-[140px]' },
                    { key: 'marketcap', label: 'Market Cap', className: 'min-w-[140px]' },
                    { key: 'supply', label: 'Circ Supply', className: 'min-w-[100px]' },
                  ].map((col) => (
                    <th
                      key={col.key}
                      className="px-4 py-3 text-left text-xs font-semibold text-gray-400 uppercase cursor-pointer select-none"
                      onClick={() => toggleSort(col.key as SortKey)}
                      style={{ cursor: 'pointer' }}
                    >
                      <span className="flex items-center gap-1">
                        {col.label}
                        {sortKey === col.key && (
                          <span className="text-blue-400">
                            {sortDir === 'asc' ? '▲' : '▼'}
                          </span>
                        )}
                      </span>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {sortedCoins.slice((page - 1) * perPage, page * perPage).map((coin, idx) => (
                  <tr
                    key={coin.symbol}
                    className="border-b border-gray-700/50 hover:bg-gray-700/20 transition-colors"
                  >
                    <td className="px-4 py-3 text-sm text-gray-400">{(page - 1) * perPage + idx + 1}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 rounded-full bg-gray-600 flex items-center justify-center text-xs font-bold text-white">
                          {coin.symbol.substring(0, 1)}
                        </div>
                        <span className="text-sm font-medium text-gray-200">{coin.name}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-400">{coin.symbol}</td>
                    <td className="px-4 py-3 text-sm font-mono text-white">
                      {formatNumber(coin.price_usd)}
                    </td>
                    <td className={`px-4 py-3 text-sm ${changeColor(coin.change_1h)}`}>
                      {formatPercent(coin.change_1h)}
                    </td>
                    <td className={`px-4 py-3 text-sm font-medium ${changeColor(coin.change_24h)}`}>
                      {formatPercent(coin.change_24h)}
                    </td>
                    <td className={`px-4 py-3 text-sm ${changeColor(coin.change_7d)}`}>
                      {formatPercent(coin.change_7d)}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-400">{formatNumber(coin.volume_24h_usd)}</td>
                    <td className="px-4 py-3 text-sm text-gray-400">{formatNumber(coin.market_cap_usd)}</td>
                    <td className="px-4 py-3 text-sm text-gray-400">
                      {coin.circulating_supply?.toLocaleString() ?? '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {totalPages > 1 && (
            <div className="flex items-center justify-between px-4 py-3 bg-gray-700/30 border-t border-gray-700">
              <span className="text-sm text-gray-400">
                Page {page} of {totalPages}
              </span>
              <div className="flex gap-2">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 rounded disabled:opacity-50"
                >
                  Prev
                </button>
                <button
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                  className="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 rounded disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
