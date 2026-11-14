from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "OmniRoute Crypto Dashboard"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = "postgresql+psycopg2://omniroute:omniroute@postgres:5432/omniroute"
    REDIS_URL: str = "redis://redis:6379/0"
    
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    CORS_ORIGINS: list[str] = ["*"]

    # Market data provider configuration
    BINANCE_BASE_URL: str = "https://api.binance.com/api/v3"
    BINANCE_WS_URL: str = "wss://stream.binance.com:9443/ws"
    COINGECKO_BASE_URL: str = "https://api.coingecko.com/api/v3"
    COINGECKO_API_KEY: str = ""
    COINMARKETCAP_BASE_URL: str = "https://pro-api.coinmarketcap.com/v1"
    COINMARKETCAP_API_KEY: str = ""
    FEAR_GREED_BASE_URL: str = "https://api.alternative.me/fng"

    # Cache TTL in seconds
    CACHE_TTL_GLOBAL_MARKET: int = 300
    CACHE_TTL_COINS_LIST: int = 60
    CACHE_TTL_COIN_DETAIL: int = 300
    CACHE_TTL_FEAR_GREED: int = 300
    CACHE_TTL_PRICES: int = 15

    # Provider failover order
    PROVIDER_FAILOVER_ORDER: str = "binance,coingecko,coinmarketcap"
    
    class Config:
        env_file = ".env"

settings = Settings()