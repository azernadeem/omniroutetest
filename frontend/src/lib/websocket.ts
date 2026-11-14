import { useState, useEffect } from 'react';

type WebSocketMessage =
  | { type: 'subscribed'; symbols: string[]; status: string }
  | { type: 'unsubscribed'; symbols: string[] }
  | { type: 'price_update'; symbol: string; price_usd: number; change_24h?: number; timestamp: number };

let ws: WebSocket | null = null;
let reconnectTimeout: ReturnType<typeof setTimeout> | null = null;
let subscribers: Set<(msg: WebSocketMessage) => void> = new Set();

const WS_URL = (import.meta as any).env.VITE_WS_URL || 'ws://localhost';

export function connectWebSocket() {
  if (ws && ws.readyState === WebSocket.OPEN) {
    return ws;
  }

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const url = `${protocol}//${window.location.host}/api/v1/ws/prices`;

  ws = new WebSocket(url);

  ws.onopen = () => {
    console.log('WebSocket connected');
    sendSubscribeMessage();
  };

  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data) as WebSocketMessage;
      subscribers.forEach((fn) => fn(msg));
    } catch (e) {
      console.error('Failed to parse WebSocket message:', e);
    }
  };

  ws.onclose = () => {
    console.log('WebSocket disconnected, reconnecting in 3s...');
    reconnectTimeout = setTimeout(() => {
      connectWebSocket();
    }, 3000);
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  return ws;
}

export function disconnectWebSocket() {
  if (reconnectTimeout) {
    clearTimeout(reconnectTimeout);
    reconnectTimeout = null;
  }
  if (ws) {
    ws.close();
    ws = null;
  }
}

export function subscribeToSymbols(symbols: string[]) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    sendSubscribeMessage(symbols);
  }
}

function sendSubscribeMessage(symbols: string[] = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP']) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      action: 'subscribe',
      symbols,
    }));
  }
}

export function useWebSocketPrices() {
  const [message, setMessage] = useState<WebSocketMessage | null>(null);

  useEffect(() => {
    connectWebSocket();
    return () => {
      disconnectWebSocket();
    };
  }, []);

  useEffect(() => {
    const handler = (msg: WebSocketMessage) => {
      setMessage(msg);
    };
    subscribers.add(handler);
    return () => {
      subscribers.delete(handler);
    };
  }, []);

  return message;
}

export function sendSocketMessage(msg: { action: string; symbols: string[] }) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(msg));
  }
}
