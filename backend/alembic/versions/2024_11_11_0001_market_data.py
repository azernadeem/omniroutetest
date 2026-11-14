"""market data

Revision ID: 2024_11_11_0001
Revises: 2024_11_11_0000
Create Date: 2024-11-11 01:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2024_11_11_0001'
down_revision = '2024_11_11_0000'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'global_market',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('total_market_cap_usd', sa.Numeric(precision=20, scale=2), nullable=True),
        sa.Column('total_volume_24h_usd', sa.Numeric(precision=20, scale=2), nullable=True),
        sa.Column('btc_dominance', sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column('eth_dominance', sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column('stablecoin_market_cap_usd', sa.Numeric(precision=20, scale=2), nullable=True),
        sa.Column('total_cryptocurrencies', sa.Integer(), nullable=True),
        sa.Column('global_market_cap_change_24h', sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column('active_cryptocurrencies', sa.Integer(), nullable=True),
        sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'fear_greed_index',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Integer(), nullable=False),
        sa.Column('value_classification', sa.String(length=50), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fear_greed_index_timestamp'), 'fear_greed_index', ['timestamp'], unique=False)

    op.create_table(
        'provider_health',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('provider_name', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('last_success', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_error', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_error_message', sa.String(length=500), nullable=True),
        sa.Column('rate_limit_remaining', sa.Integer(), nullable=True),
        sa.Column('rate_limit_reset', sa.DateTime(timezone=True), nullable=True),
        sa.Column('avg_response_time_ms', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_health_provider_name'), 'provider_health', ['provider_name'], unique=False)


def downgrade() -> None:
    op.drop_table('provider_health')
    op.drop_table('fear_greed_index')
    op.drop_table('global_market')