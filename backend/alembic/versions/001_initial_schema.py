"""Initial schema with all models

Revision ID: 001_initial
Revises: 
Create Date: 2024-12-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('organizations',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.Column('tier', sa.String(length=50), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('max_documents', sa.Integer(), nullable=True),
    sa.Column('max_storage_mb', sa.Integer(), nullable=True),
    sa.Column('max_users', sa.Integer(), nullable=True),
    sa.Column('current_documents', sa.Integer(), nullable=True),
    sa.Column('current_storage_mb', sa.Integer(), nullable=True),
    sa.Column('current_users', sa.Integer(), nullable=True),
    sa.Column('org_settings', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organizations_name'), 'organizations', ['name'], unique=False)
    op.create_index(op.f('ix_organizations_slug'), 'organizations', ['slug'], unique=True)
    
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=True),
    sa.Column('organization_id', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('ADMIN', 'MEMBER', 'VIEWER', name='userrole'), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    op.create_table('documents',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('organization_id', sa.String(), nullable=False),
    sa.Column('uploaded_by', sa.String(), nullable=True),
    sa.Column('filename', sa.String(length=500), nullable=False),
    sa.Column('file_type', sa.String(length=50), nullable=True),
    sa.Column('file_size', sa.Integer(), nullable=True),
    sa.Column('s3_key', sa.String(length=1000), nullable=True),
    sa.Column('status', sa.Enum('UPLOADING', 'PROCESSING', 'COMPLETED', 'FAILED', name='documentstatus'), nullable=True),
    sa.Column('num_chunks', sa.Integer(), nullable=True),
    sa.Column('num_pages', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=500), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('tags', sa.JSON(), nullable=True),
    sa.Column('doc_metadata', sa.JSON(), nullable=True),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_created_at'), 'documents', ['created_at'], unique=False)
    op.create_index(op.f('ix_documents_organization_id'), 'documents', ['organization_id'], unique=False)
    op.create_index(op.f('ix_documents_status'), 'documents', ['status'], unique=False)
    
    op.create_table('conversations',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('organization_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(length=500), nullable=True),
    sa.Column('is_archived', sa.Boolean(), nullable=True),
    sa.Column('conv_metadata', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversations_created_at'), 'conversations', ['created_at'], unique=False)
    op.create_index(op.f('ix_conversations_organization_id'), 'conversations', ['organization_id'], unique=False)
    op.create_index(op.f('ix_conversations_user_id'), 'conversations', ['user_id'], unique=False)
    
    op.create_table('usage_metrics',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('organization_id', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('api_calls', sa.Integer(), nullable=True),
    sa.Column('documents_uploaded', sa.Integer(), nullable=True),
    sa.Column('embeddings_created', sa.Integer(), nullable=True),
    sa.Column('chat_messages', sa.Integer(), nullable=True),
    sa.Column('prompt_tokens', sa.Integer(), nullable=True),
    sa.Column('completion_tokens', sa.Integer(), nullable=True),
    sa.Column('total_tokens', sa.Integer(), nullable=True),
    sa.Column('embedding_cost', sa.Float(), nullable=True),
    sa.Column('llm_cost', sa.Float(), nullable=True),
    sa.Column('storage_cost', sa.Float(), nullable=True),
    sa.Column('total_cost', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usage_metrics_date'), 'usage_metrics', ['date'], unique=False)
    op.create_index(op.f('ix_usage_metrics_organization_id'), 'usage_metrics', ['organization_id'], unique=False)
    
    op.create_table('document_chunks',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('document_id', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('chunk_index', sa.Integer(), nullable=False),
    sa.Column('vector_id', sa.String(length=100), nullable=True),
    sa.Column('page_number', sa.Integer(), nullable=True),
    sa.Column('start_char', sa.Integer(), nullable=True),
    sa.Column('end_char', sa.Integer(), nullable=True),
    sa.Column('chunk_metadata', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_document_chunks_document_id'), 'document_chunks', ['document_id'], unique=False)
    
    op.create_table('messages',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('conversation_id', sa.String(), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('sources', sa.JSON(), nullable=True),
    sa.Column('msg_metadata', sa.JSON(), nullable=True),
    sa.Column('tokens_used', sa.Integer(), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_conversation_id'), 'messages', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_messages_created_at'), 'messages', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_messages_created_at'), table_name='messages')
    op.drop_index(op.f('ix_messages_conversation_id'), table_name='messages')
    op.drop_table('messages')
    op.drop_index(op.f('ix_document_chunks_document_id'), table_name='document_chunks')
    op.drop_table('document_chunks')
    op.drop_index(op.f('ix_usage_metrics_organization_id'), table_name='usage_metrics')
    op.drop_index(op.f('ix_usage_metrics_date'), table_name='usage_metrics')
    op.drop_table('usage_metrics')
    op.drop_index(op.f('ix_conversations_user_id'), table_name='conversations')
    op.drop_index(op.f('ix_conversations_organization_id'), table_name='conversations')
    op.drop_index(op.f('ix_conversations_created_at'), table_name='conversations')
    op.drop_table('conversations')
    op.drop_index(op.f('ix_documents_status'), table_name='documents')
    op.drop_index(op.f('ix_documents_organization_id'), table_name='documents')
    op.drop_index(op.f('ix_documents_created_at'), table_name='documents')
    op.drop_table('documents')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_organizations_slug'), table_name='organizations')
    op.drop_index(op.f('ix_organizations_name'), table_name='organizations')
    op.drop_table('organizations')


