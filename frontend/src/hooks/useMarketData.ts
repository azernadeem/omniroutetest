import { useQuery, useQueryClient } from '@tanstack/react-query';
import { marketApi } from '@/lib/market';
import type { GlobalMarketData, CoinPrice, CoinDetail, OHLCVPoint, ProviderHealth, CoinsListResponse } from '@/lib/market';

export const MARKET_KEYS = {
  global: ['market', 'global'],
  coins: (page: number, perPage: number, search?: string) => ['market', 'coins', page, perPage, search],
  trending: ['market', 'trending'],
  gainers: ['market', 'gainers'],
  losers: ['market', 'losers'],
  volume: ['market', 'volume'],
  coinDetail: (symbol: string) => ['market', 'coin', symbol],
  coinHistory: (symbol: string, interval: string) => ['market', 'coin', symbol, 'history', interval],
  providersHealth: ['market', 'providers', 'health'],
};

export function useGlobalMarket() {
  return useQuery<GlobalMarketData>({
    queryKey: MARKET_KEYS.global,
    queryFn: marketApi.getGlobalMarket,
    refetchInterval: 30000,
    staleTime: 15000,
  });
}

export function useCoins(page: number = 1, perPage: number = 100, search?: string) {
  return useQuery<CoinsListResponse>({
    queryKey: MARKET_KEYS.coins(page, perPage, search),
    queryFn: () => marketApi.getCoins({ page, per_page: perPage, search }),
    refetchInterval: 60000,
    staleTime: 30000,
    enabled: !!search || page > 0,
  });
}

export function useTrending() {
  return useQuery<CoinPrice[]>({
    queryKey: MARKET_KEYS.trending,
    queryFn: marketApi.getTrending,
    refetchInterval: 60000,
    staleTime: 30000,
  });
}

export function useGainers() {
  return useQuery<CoinPrice[]>({
    queryKey: MARKET_KEYS.gainers,
    queryFn: marketApi.getGainers,
    refetchInterval: 60000,
    staleTime: 30000,
  });
}

export function useLosers() {
  return useQuery<CoinPrice[]>({
    queryKey: MARKET_KEYS.losers,
    queryFn: marketApi.getLosers,
    refetchInterval: 60000,
    staleTime: 30000,
  });
}

export function useCoinDetail(symbol: string) {
  return useQuery<CoinDetail>({
    queryKey: MARKET_KEYS.coinDetail(symbol),
    queryFn: () => marketApi.getCoinDetail(symbol),
    refetchInterval: 30000,
    staleTime: 15000,
    enabled: !!symbol,
  });
}

export function useCoinHistory(symbol: string, interval: string = '1h') {
  return useQuery<OHLCVPoint[]>({
    queryKey: MARKET_KEYS.coinHistory(symbol, interval),
    queryFn: () => marketApi.getCoinHistory(symbol, interval),
    refetchInterval: 60000,
    staleTime: 30000,
    enabled: !!symbol,
  });
}

export function useProvidersHealth() {
  return useQuery<ProviderHealth[]>({
    queryKey: MARKET_KEYS.providersHealth,
    queryFn: marketApi.getProvidersHealth,
    refetchInterval: 300000,
    staleTime: 120000,
  });
}