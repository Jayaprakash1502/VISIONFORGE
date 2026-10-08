"""Initial Version 1 Schema Migration

Revision ID: 001_initial_v1_schema
Revises: 
Create Date: 2026-10-08 13:16:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_v1_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create Enums
    camera_source_enum = postgresql.ENUM('LOCAL_VIDEO', 'UPLOAD', 'WEBCAM', 'RTSP', name='camera_source_type_enum', create_type=False)
    camera_source_enum.create(op.get_bind(), checkfirst=True)

    camera_status_enum = postgresql.ENUM('ONLINE', 'OFFLINE', 'CONNECTING', 'ERROR', 'DISABLED', name='camera_status_enum', create_type=False)
    camera_status_enum.create(op.get_bind(), checkfirst=True)

    zone_type_enum = postgresql.ENUM('RESTRICTED', name='zone_type_enum', create_type=False)
    zone_type_enum.create(op.get_bind(), checkfirst=True)

    severity_level_enum = postgresql.ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='severity_level_enum', create_type=False)
    severity_level_enum.create(op.get_bind(), checkfirst=True)

    event_type_enum = postgresql.ENUM('PERSON_DETECTED', 'CROWD_DETECTED', 'RESTRICTED_AREA_ENTRY', 'LOITERING', 'UNUSUAL_ACTIVITY', 'CAMERA_OFFLINE', 'CAMERA_RECOVERED', 'SYSTEM_ERROR', name='event_type_enum', create_type=False)
    event_type_enum.create(op.get_bind(), checkfirst=True)

    event_status_enum = postgresql.ENUM('NEW', 'ACKNOWLEDGED', 'RESOLVED', name='event_status_enum', create_type=False)
    event_status_enum.create(op.get_bind(), checkfirst=True)

    # 2. Table: cameras
    op.create_table(
        'cameras',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('location', sa.String(length=200), nullable=True),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('source_type', sa.Enum('LOCAL_VIDEO', 'UPLOAD', 'WEBCAM', 'RTSP', name='camera_source_type_enum'), nullable=False),
        sa.Column('source_url', sa.String(length=500), nullable=False),
        sa.Column('status', sa.Enum('ONLINE', 'OFFLINE', 'CONNECTING', 'ERROR', 'DISABLED', name='camera_status_enum'), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('length(name) > 0', name='ck_cameras_name_not_empty'),
        sa.CheckConstraint('length(source_url) > 0', name='ck_cameras_source_url_not_empty')
    )

    # 3. Table: zones
    op.create_table(
        'zones',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('camera_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('zone_type', sa.Enum('RESTRICTED', name='zone_type_enum'), nullable=False),
        sa.Column('polygon_coordinates', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('applicable_object_class', sa.String(length=50), nullable=False, server_default='person'),
        sa.Column('severity', sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='severity_level_enum'), nullable=False),
        sa.Column('cooldown_seconds', sa.Integer(), nullable=False, server_default='10'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['camera_id'], ['cameras.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('cooldown_seconds >= 0', name='ck_zones_cooldown_positive'),
        sa.CheckConstraint('length(name) > 0', name='ck_zones_name_not_empty')
    )
    op.create_index('idx_zones_camera_id', 'zones', ['camera_id'], unique=False)

    # 4. Table: events
    op.create_table(
        'events',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('event_type', sa.Enum('PERSON_DETECTED', 'CROWD_DETECTED', 'RESTRICTED_AREA_ENTRY', 'LOITERING', 'UNUSUAL_ACTIVITY', 'CAMERA_OFFLINE', 'CAMERA_RECOVERED', 'SYSTEM_ERROR', name='event_type_enum'), nullable=False),
        sa.Column('camera_id', sa.UUID(), nullable=False),
        sa.Column('zone_id', sa.UUID(), nullable=True),
        sa.Column('location', sa.String(length=200), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('severity', sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='severity_level_enum'), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('detection_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.Enum('NEW', 'ACKNOWLEDGED', 'RESOLVED', name='event_status_enum'), nullable=False),
        sa.Column('snapshot_path', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['camera_id'], ['cameras.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['zone_id'], ['zones.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_events_timestamp', 'events', ['timestamp'], unique=False)
    op.create_index('idx_events_camera_id', 'events', ['camera_id'], unique=False)
    op.create_index('idx_events_event_type', 'events', ['event_type'], unique=False)
    op.create_index('idx_events_severity', 'events', ['severity'], unique=False)
    op.create_index('idx_events_status', 'events', ['status'], unique=False)

    # 5. Table: detections
    op.create_table(
        'detections',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('camera_id', sa.UUID(), nullable=False),
        sa.Column('event_id', sa.UUID(), nullable=True),
        sa.Column('object_class', sa.String(length=50), nullable=False, server_default='person'),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('bbox_x', sa.Float(), nullable=False),
        sa.Column('bbox_y', sa.Float(), nullable=False),
        sa.Column('bbox_width', sa.Float(), nullable=False),
        sa.Column('bbox_height', sa.Float(), nullable=False),
        sa.Column('tracking_id', sa.Integer(), nullable=True),
        sa.Column('frame_timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['camera_id'], ['cameras.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('confidence >= 0.0 AND confidence <= 1.0', name='ck_detections_confidence_range'),
        sa.CheckConstraint('bbox_width >= 0.0 AND bbox_height >= 0.0', name='ck_detections_bbox_positive')
    )
    op.create_index('idx_detections_camera_id', 'detections', ['camera_id'], unique=False)
    op.create_index('idx_detections_frame_timestamp', 'detections', ['frame_timestamp'], unique=False)
    op.create_index('idx_detections_object_class', 'detections', ['object_class'], unique=False)

    # 6. Table: alerts
    op.create_table(
        'alerts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('event_id', sa.UUID(), nullable=False),
        sa.Column('severity', sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='severity_level_enum'), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('message', sa.String(length=500), nullable=False),
        sa.Column('status', sa.Enum('NEW', 'ACKNOWLEDGED', 'RESOLVED', name='event_status_enum'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('acknowledged_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_alerts_event_id', 'alerts', ['event_id'], unique=False)
    op.create_index('idx_alerts_status', 'alerts', ['status'], unique=False)
    op.create_index('idx_alerts_created_at', 'alerts', ['created_at'], unique=False)

    # 7. Table: system_settings
    op.create_table(
        'system_settings',
        sa.Column('key', sa.String(length=100), nullable=False),
        sa.Column('value', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('description', sa.String(length=250), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('key')
    )


def downgrade() -> None:
    op.drop_table('system_settings')
    op.drop_index('idx_alerts_created_at', table_name='alerts')
    op.drop_index('idx_alerts_status', table_name='alerts')
    op.drop_index('idx_alerts_event_id', table_name='alerts')
    op.drop_table('alerts')
    op.drop_index('idx_detections_object_class', table_name='detections')
    op.drop_index('idx_detections_frame_timestamp', table_name='detections')
    op.drop_index('idx_detections_camera_id', table_name='detections')
    op.drop_table('detections')
    op.drop_index('idx_events_status', table_name='events')
    op.drop_index('idx_events_severity', table_name='events')
    op.drop_index('idx_events_event_type', table_name='events')
    op.drop_index('idx_events_camera_id', table_name='events')
    op.drop_index('idx_events_timestamp', table_name='events')
    op.drop_table('events')
    op.drop_index('idx_zones_camera_id', table_name='zones')
    op.drop_table('zones')
    op.drop_table('cameras')

    op.execute("DROP TYPE IF EXISTS event_status_enum")
    op.execute("DROP TYPE IF EXISTS event_type_enum")
    op.execute("DROP TYPE IF EXISTS severity_level_enum")
    op.execute("DROP TYPE IF EXISTS zone_type_enum")
    op.execute("DROP TYPE IF EXISTS camera_status_enum")
    op.execute("DROP TYPE IF EXISTS camera_source_type_enum")
