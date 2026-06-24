"""empty message

Revision ID: 1f701ff706bf
Revises: 61f1a527eba7
Create Date: 2026-06-24 14:00:25.537670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f701ff706bf'
down_revision = '61f1a527eba7'
branch_labels = None
depends_on = None


def upgrade():
    # Создаём последовательность, если её ещё нет
    op.execute("CREATE SEQUENCE IF NOT EXISTS reading_progress_id_seq")
    
    # Устанавливаем DEFAULT для колонки id (используем nextval)
    op.execute("ALTER TABLE reading_progress ALTER COLUMN id SET DEFAULT nextval('reading_progress_id_seq')")
    
    # Привязываем последовательность к колонке (для каскадного удаления)
    op.execute("ALTER SEQUENCE reading_progress_id_seq OWNED BY reading_progress.id")
    
    # Устанавливаем текущее значение последовательности на максимальный существующий id
    # Это защитит от конфликтов, если в таблице уже есть записи
    op.execute("SELECT setval('reading_progress_id_seq', COALESCE((SELECT MAX(id) FROM reading_progress), 1))")


def downgrade():
    # Откат: убираем DEFAULT
    op.execute("ALTER TABLE reading_progress ALTER COLUMN id DROP DEFAULT")
    # Удаляем последовательность
    op.execute("DROP SEQUENCE IF EXISTS reading_progress_id_seq")
