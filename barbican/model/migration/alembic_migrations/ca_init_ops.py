# Copyright 2015 OpenStack Foundation
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

# Initial operations for agent management extension
# This module only manages the 'agents' table. Binding tables are created
# in the modules for relevant resources


from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'certificate_authorities',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('deleted', sa.Boolean(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('plugin_name', sa.String(length=255), nullable=False),
        sa.Column('plugin_ca_id', sa.Text(), nullable=False),
        sa.Column('expiration', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'project_certificate_authorities',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('deleted', sa.Boolean(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('ca_id', sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(['ca_id'], ['certificate_authorities.id'],),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'],),
        sa.PrimaryKeyConstraint('id', 'project_id', 'ca_id'),
        sa.UniqueConstraint('project_id',
                            'ca_id',
                            name='_project_certificate_authority_uc')
    )

    op.create_table(
        'certificate_authority_metadata',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('deleted', sa.Boolean(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('key', sa.String(length=255), nullable=False),
        sa.Column('value', sa.String(length=255), nullable=False),
        sa.Column('ca_id', sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(['ca_id'], ['certificate_authorities.id'],),
        sa.PrimaryKeyConstraint('id', 'key', 'ca_id'),
        sa.UniqueConstraint('ca_id', 'key',
                            name='_certificate_authority_metadatum_uc')
    )

    op.create_table(
        'preferred_certificate_authorities',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('deleted', sa.Boolean(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('ca_id', sa.String(length=36), nullable=True),
        sa.ForeignKeyConstraint(['ca_id'], ['certificate_authorities.id'],),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'],),
        sa.PrimaryKeyConstraint('id', 'project_id'),
        sa.UniqueConstraint('project_id')
    )
