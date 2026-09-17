"""add prediction created_at

Revision ID: 7f4ef2d4e356
Revises: 77f243fe6432
Create Date: 2026-09-17 00:00:00.000000

Adds intelligence_predictions.created_at, needed to tell whether a
prediction's horizon_days window has actually elapsed -- required by
PredictionFeedbackService.list_due_for_feedback() (see the
intelligence-pipeline-wiring-audit project doc's prediction feedback
loop section). Backfills existing rows with the current time via
server_default so this is a non-breaking additive change; the
server_default is left in place rather than dropped after backfill
since new rows written through PredictionRecord's Python-side
`default=` will always supply an explicit value anyway.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f4ef2d4e356'
down_revision: Union[str, Sequence[str], None] = '77f243fe6432'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'intelligence_predictions',
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('intelligence_predictions', 'created_at')
