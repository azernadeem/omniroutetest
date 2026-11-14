# OmniRoute Crypto Dashboard

A professional cryptocurrency intelligence dashboard inspired by TradingView, CoinMarketCap, and Binance.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Nginx     │────▶│  Frontend   │────▶│  Backend    │
│  (Port 80)  │     │  (Port 3000)│     │ (Port 8000) │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │  PostgreSQL     │
                                    │  (Port 5432)    │
                                    └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │  Redis          │
                                    │  (Port 6379)    │
                                    └─────────────────┘
```

## Technology Stack

**Frontend:** React, TypeScript, Vite, Tailwind CSS, Shadcn/UI, Lucide Icons, React Query, Zustand, Recharts

**Backend:** Python 3.12, FastAPI, SQLAlchemy, Pydantic, Alembic

**Infrastructure:** PostgreSQL, Redis, Docker, Docker Compose, Nginx

## Quick Start

### 1. Clone and configure

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 2. Run with Docker

```bash
docker compose up -d --build
```

### 3. Access the application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Nginx Proxy: http://localhost:80

### 4. Run database migrations

```bash
docker compose exec backend alembic upgrade head
```

## Project Structure

```
omniroutetest/
├── docker-compose.yml
├── nginx.conf
├── .env.example
├── README.md
├── frontend/          # React + TypeScript + Vite
├── backend/           # FastAPI + SQLAlchemy
└── ...
```

## Navigation Sections

1. Overview - Market cap, volume, dominance, fear & greed
2. Markets - Cryptocurrency listings
3. Coin Explorer - Individual coin details
4. Portfolio - Holdings management
5. Watchlists - Tracked coins
6. Technical Analysis - Charting
7. Market Analytics - Aggregated metrics
8. Correlation Analysis - Asset relationships
9. News & Sentiment - Market news
10. Alerts - Price notifications
11. AI Assistant - AI-powered insights
12. Settings - User preferences

## Development

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Database Models

- Users
- Cryptocurrencies
- Market Prices
- OHLCV (historical data)
- Portfolios
- Portfolio Transactions
- Watchlists
- Alerts
- Notifications
- News Articles
- User Preferences

## License

MIT