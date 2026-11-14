export default function CoinExplorer() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Coin Explorer</h1>
      <p className="text-gray-400">Explore individual cryptocurrencies and their metrics</p>
      <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
        <div className="flex items-center justify-center h-64 text-gray-500">
          Coin explorer loading...
        </div>
      </div>
    </div>
  );
}