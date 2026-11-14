"""initial

Revision ID: 2024_11_11_0000
Revises: 
Create Date: 2024-11-11 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2024_11_11_0000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'cryptocurrencies',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('symbol', sa.String(length=10), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('symbol')
    )
    op.create_index(op.f('ix_cryptocurrencies_symbol'), 'cryptocurrencies', ['symbol'], unique=True)

    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    op.create_table(
        'market_prices',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('crypto_id', sa.String(), nullable=False),
        sa.Column('price_usd', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('market_cap_usd', sa.Numeric(precision=20, scale=2), nullable=True),
        sa.Column('volume_24h_usd', sa.Numeric(precision=20, scale=2), nullable=True),
        sa.Column('change_1h', sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column('change_24h', sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column('change_7d', sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column('circulating_supply', sa.Numeric(precision=30, scale=8), nullable=True),
        sa.Column('total_supply', sa.Numeric(precision=30, scale=8), nullable=True),
        sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['crypto_id'], ['cryptocurrencies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_market_prices_crypto_id'), 'market_prices', ['crypto_id'], unique=False)

    op.create_table(
        'ohlcv',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('crypto_id', sa.String(), nullable=False),
        sa.Column('interval', sa.String(length=10), nullable=False),
        sa.Column('open_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('open_price', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('high_price', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('low_price', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('close_price', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('volume', sa.Numeric(precision=30, scale=8), nullable=False),
        sa.Column('close_time', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['crypto_id'], ['cryptocurrencies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ohlcv_crypto_id'), 'ohlcv', ['crypto_id'], unique=False)
    op.create_index(op.f('ix_ohlcv_interval'), 'ohlcv', ['interval'], unique=False)

    op.create_table(
        'portfolios',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('total_value_usd', sa.Numeric(precision=20, scale=2), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolios_user_id'), 'portfolios', ['user_id'], unique=False)

    op.create_table(
        'watchlists',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_watchlists_user_id'), 'watchlists', ['user_id'], unique=False)

    op.create_table(
        'alerts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('crypto_id', sa.String(), nullable=False),
        sa.Column('type', sa.Enum('price_above', 'price_below', 'percent_change', name='alerttype'), nullable=False),
        sa.Column('threshold_value', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('is_triggered', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('triggered_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alerts_user_id'), 'alerts', ['user_id'], unique=False)

    op.create_table(
        'notifications',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('type', sa.Enum('info', 'warning', 'error', 'success', 'alert', name='notificationtype'), nullable=False, server_default=sa.text("'info'::notificationtype")),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)

    op.create_table(
        'news_articles',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('url', sa.String(length=1000), nullable=False),
        sa.Column('source', sa.String(length=100), nullable=True),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('sentiment_score', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('is_processed', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_news_articles_published_at'), 'news_articles', ['published_at'], unique=False)

    op.create_table(
        'portfolio_transactions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('portfolio_id', sa.String(), nullable=False),
        sa.Column('crypto_id', sa.String(), nullable=False),
        sa.Column('type', sa.Enum('buy', 'sell', name='transactiontype'), nullable=False),
        sa.Column('amount', sa.Numeric(precision=30, scale=8), nullable=False),
        sa.Column('price_usd', sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column('total_usd', sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column('fee_usd', sa.Numeric(precision=20, scale=2), nullable=False, server_default=sa.text('0')),
        sa.Column('executed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolio_transactions_portfolio_id'), 'portfolio_transactions', ['portfolio_id'], unique=False)

    op.create_table(
        'user_preferences',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('theme', sa.String(length=20), nullable=False, server_default=sa.text("'dark'")),
        sa.Column('default_currency', sa.String(length=10), nullable=False, server_default=sa.text("'USD'")),
        sa.Column('email_notifications', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('push_notifications', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )


def downgrade() -> None:
    op.drop_table('user_preferences')
    op.drop_table('portfolio_transactions')
    op.drop_table('news_articles')
    op.drop_table('notifications')
    op.drop_table('alerts')
    op.drop_table('watchlists')
    op.drop_table('portfolios')
    op.drop_table('ohlcv')
    op.drop_table('market_prices')
    op.drop_table('users')
    op.drop_table('cryptocurrencies')