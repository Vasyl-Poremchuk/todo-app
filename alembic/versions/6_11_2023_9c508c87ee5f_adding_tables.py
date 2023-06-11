"""
adding tables

Revision ID: 9c508c87ee5f
Revises: 
Create Date: 2023-06-11 15:23:39.297823
"""
from alembic import op
import sqlalchemy as sa


revision = "9c508c87ee5f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    The function upgrades all changes from a specific revision.
    """
    op.create_table(
        "address",
        sa.Column("address_id", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(length=30), nullable=False),
        sa.Column("state", sa.String(length=30), nullable=False),
        sa.Column("country", sa.String(length=30), nullable=False),
        sa.Column("postal_code", sa.String(length=5), nullable=True),
        sa.PrimaryKeyConstraint("address_id"),
    )
    op.create_index(
        op.f("ix_address_address_id"), "address", ["address_id"], unique=False
    )
    op.create_table(
        "user",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("username", sa.String(length=30), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column(
            "role", sa.Enum("admin", "user", name="role"), nullable=False
        ),
        sa.Column("first_name", sa.String(length=30), nullable=True),
        sa.Column("last_name", sa.String(length=30), nullable=True),
        sa.Column("phone_number", sa.String(length=15), nullable=True),
        sa.Column("address_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["address_id"], ["address.address_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_user_id"), "user", ["user_id"], unique=False)
    op.create_table(
        "todo",
        sa.Column("todo_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=30), nullable=False),
        sa.Column("description", sa.String(length=200), nullable=False),
        sa.Column(
            "priority",
            sa.Enum("one", "two", "three", "four", "five", name="priority"),
            nullable=False,
        ),
        sa.Column("complete", sa.Boolean(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["user.user_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("todo_id"),
    )
    op.create_index(op.f("ix_todo_title"), "todo", ["title"], unique=False)
    op.create_index(op.f("ix_todo_todo_id"), "todo", ["todo_id"], unique=False)


def downgrade() -> None:
    """
    The function downgrades all changes from a specific revision.
    """
    op.drop_index(op.f("ix_todo_todo_id"), table_name="todo")
    op.drop_index(op.f("ix_todo_title"), table_name="todo")
    op.drop_table("todo")
    op.drop_index(op.f("ix_user_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_address_address_id"), table_name="address")
    op.drop_table("address")
