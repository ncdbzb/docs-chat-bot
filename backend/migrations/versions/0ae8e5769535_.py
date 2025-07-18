from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0ae8e5769535'
down_revision: Union[str, None] = 'd9c3736fb6d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# объявляем enum отдельно
admin_request_status_enum = postgresql.ENUM(
    'pending', 'approved', 'rejected', name='adminrequeststatus'
)

def upgrade() -> None:

    op.create_table(
        'admin_requests',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('status', admin_request_status_enum, nullable=False),
        sa.Column('info', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('admin_requests')
    # Удаляем enum явно
    admin_request_status_enum.drop(op.get_bind())
