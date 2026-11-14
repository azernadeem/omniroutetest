import { useGlobalMarket } from '@/hooks/useMarketData';
import LoadingSpinner from '@/components/LoadingSpinner';
import { AlertCircle } from 'lucide-react';

const formatLargeNumber = (num: number | null): string => {
  if (num === null || num === undefined) return '—';
  if (num >= 1e12) return `$${(num / 1e12).toFixed(2)}T`;
  if (num >= 1e9) return `$${(num / 1e9).toFixed(2)}B`;
  if (num >= 1e6) return `$${(num / 1e6).toFixed(2)}M`;
  return `$${num.toFixed(2)}`;
};

export default function Overview() {
  const { data, isLoading, error } = useGlobalMarket();

  if (isLoading) return <LoadingSpinner />;
  if (error || !data || !data.data_available) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-2 text-red-400">
          <AlertCircle className="w-4 h-4" />
          <h2 className="text-lg font-semibold">Data Unavailable</h2>
        </div>
        <p className="text-gray-400">Market data is temporarily unavailable. Please try again later.</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="bg-gray-800 p-4 rounded-xl border border-gray-700">
              <span className="text-sm text-gray-400">Stat {i + 1}</span>
              <span className="text-2xl font-bold text-gray-500">—</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  const marketCapChange = data.global_market_cap_change_24h;
  const marketCapPositive = marketCapChange !== null && marketCapChange >= 0;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-2xl font-bold">Market Overview</h1>
          <p className="text-gray-400 text-sm">Real-time cryptocurrency market data</p>
        </div>
        <div className="flex gap-2">
          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-white text-sm font-medium transition-colors">
            Refresh Data
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
          <div className="flex justify-between items-start mb-2">
            <span className="text-sm text-gray-400">Market Cap</span>
          </div>
          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-bold text-white">{formatLargeNumber(data.total_market_cap_usd)}</span>
            {marketCapChange !== null && (
              <span className={`text-xs font-medium ${marketCapPositive ? 'text-positive' : 'text-negative'}`}>
                {marketCapPositive ? '+' : ''}{marketCapChange.toFixed(2)}%
              </span>
            )}
          </div>
          <span className="text-xs text-gray-500 mt-1 block">Provider: {data.provider}</span>
        </div>
        <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
          <div className="flex justify-between items-start mb-2">
            <span className="text-sm text-gray-400">24h Volume</span>
          </div>
          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-bold text-white">{formatLargeNumber(data.total_volume_24h_usd)}</span>
          </div>
          <span className="text-xs text-gray-500 mt-1 block">Volume data live</span>
        </div>
        <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
          <div className="flex justify-between items-start mb-2">
            <span className="text-sm text-gray-400">BTC Dominance</span>
          </div>
          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-bold text-white">{data.btc_dominance?.toFixed(2) ?? '—'}%</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
          <div className="flex justify-between items-start mb-2">
            <span className="text-sm text-gray-400">ETH Dominance</span>
          </div>
          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-bold text-white">{data.eth_dominance?.toFixed(2) ?? '—'}%</span>
          </div>
        </div>
        <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
          <div className="flex justify-between items-start mb-2">
            <span className="text-sm text-gray-400">Total Coins</span>
          </div>
          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-bold text-white">{data.total_cryptocurrencies ?? '—'}</span>
          </div>
        </div>
        <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
          <div className="flex justify-between items-start mb-2">
            <span className="text-sm text-gray-400">Fear & Greed</span>
          </div>
          <div className="flex items-center gap-1">
            <span className="text-2xl font-bold text-white">{data.fear_and_greed?.value ?? '—'}</span>
            <span className="text-xs text-gray-400">{data.fear_and_greed?.classification ?? ''}</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-gray-800 p-6 rounded-xl border border-gray-700">
          <h3 className="text-lg font-semibold mb-4">Bitcoin Price Chart</h3>
          <LoadingSpinner />
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
          <h3 className="text-lg font-semibold mb-4">Ethereum Price Chart</h3>
          <LoadingSpinner />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
          <h3 className="text-lg font-semibold mb-4">Top Gainers</h3>
          <LoadingSpinner />
        </div>
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
          <h3 className="text-lg font-semibold mb-4">Top Losers</h3>
          <LoadingSpinner />
        </div>
      </div>
    </div>
  );
}
