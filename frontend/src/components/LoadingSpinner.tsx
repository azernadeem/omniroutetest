export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center h-64 text-gray-400">
      <div className="w-8 h-8 border-4 border-gray-700 border-t-positive rounded-full animate-spin mb-2" />
      <span className="text-sm">Loading market data...</span>
    </div>
  );
}