import { apiClient } from './api';

export interface GlobalMarketData {
  total_market_cap_usd: number | null;
  total_volume_24h_usd: number | null;
  btc_dominance: number | null;
  eth_dominance: number | null;
  stablecoin_market_cap_usd: number | null;
  total_cryptocurrencies: number | null;
  global_market_cap_change_24h: number | null;
  active_cryptocurrencies: number | null;
  fear_and_greed: {
    value: number | null;
    classification: string | null;
  } | null;
  provider: string;
  data_available: boolean;
}

export interface CoinPrice {
  symbol: string;
  name: string;
  price_usd: number;
  market_cap_usd: number | null;
  volume_24h_usd: number | null;
  change_1h: number | null;
  change_24h: number | null;
  change_7d: number | null;
  circulating_supply: number | null;
  total_supply: number | null;
  max_supply: number | null;
  provider: string;
  last_updated: string | null;
}

export interface CoinsListResponse {
  coins: CoinPrice[];
  page: number;
  per_page: number;
  count: number;
}

export interface CoinDetail {
  symbol: string;
  name: string;
  description: string | null;
  price_usd: number | null;
  market_cap_usd: number | null;
  fully_diluted_valuation: number | null;
  volume_24h_usd: number | null;
  circulating_supply: number | null;
  total_supply: number | null;
  max_supply: number | null;
  all_time_high: number | null;
  all_time_low: number | null;
  provider: string;
  last_updated: string | null;
  data_available: boolean;
}

export interface OHLCVPoint {
  open_time: string;
  open_price: number;
  high_price: number;
  low_price: number;
  close_price: number;
  volume: number;
  close_time: string;
}

export interface ProviderHealth {
  provider: string;
  status: string;
  avg_response_time_ms: number | null;
  error: string | null;
}

const BASE = '/api/v1';

export const marketApi = {
  getGlobalMarket: async (): Promise<GlobalMarketData> => {
    const res = await apiClient.get(`${BASE}/market/overview`);
    return res.data;
  },
  getCoins: async (params?: {
    page?: number;
    per_page?: number;
    search?: string;
  }): Promise<CoinsListResponse> => {
    const res = await apiClient.get(`${BASE}/market/coins`, { params });
    return res.data;
  },
  getTrending: async (): Promise<CoinPrice[]> => {
    const res = await apiClient.get(`${BASE}/market/trending`);
    return res.data;
  },
  getGainers: async (): Promise<CoinPrice[]> => {
    const res = await apiClient.get(`${BASE}/market/gainers`);
    return res.data;
  },
  getLosers: async (): Promise<CoinPrice[]> => {
    const res = await apiClient.get(`${BASE}/market/losers`);
    return res.data;
  },
  getHighVolume: async (): Promise<CoinPrice[]> => {
    const res = await apiClient.get(`${BASE}/market/volume`);
    return res.data;
  },
  getCoinDetail: async (symbol: string): Promise<CoinDetail> => {
    const res = await apiClient.get(`${BASE}/coins/${symbol}`);
    return res.data;
  },
  getCoinHistory: async (symbol: string, interval: string, limit?: number): Promise<OHLCVPoint[]> => {
    const res = await apiClient.get(`${BASE}/coins/${symbol}/history`, {
      params: { interval, limit },
    });
    return res.data;
  },
  getProvidersHealth: async (): Promise<ProviderHealth[]> => {
    const res = await apiClient.get(`${BASE}/providers/health`);
    return res.data;
  },
};