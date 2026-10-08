export type CameraStatus = 'ONLINE' | 'OFFLINE' | 'CONNECTING' | 'ERROR' | 'DISABLED' | 'PROCESSING';
export type CameraSourceType = 'LOCAL_VIDEO' | 'UPLOAD' | 'WEBCAM' | 'RTSP';
export type SeverityLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type EventType =
  | 'PERSON_DETECTED'
  | 'CROWD_DETECTED'
  | 'RESTRICTED_AREA_ENTRY'
  | 'LOITERING'
  | 'UNUSUAL_ACTIVITY'
  | 'CAMERA_OFFLINE'
  | 'CAMERA_RECOVERED'
  | 'SYSTEM_ERROR';
export type EventStatus = 'NEW' | 'ACKNOWLEDGED' | 'RESOLVED';

export interface Camera {
  id: string;
  name: string;
  location?: string;
  description?: string;
  source_type: CameraSourceType;
  source_url: string;
  status: CameraStatus;
  enabled: boolean;
  created_at: string;
  updated_at: string;
}

export interface SecurityEvent {
  id: string;
  event_type: EventType;
  camera_id: string;
  zone_id?: string;
  location?: string;
  timestamp: string;
  severity: SeverityLevel;
  description?: string;
  detection_data?: any;
  status: EventStatus;
  snapshot_path?: string;
  created_at: string;
}

export interface SecurityAlert {
  id: string;
  event_id: string;
  severity: SeverityLevel;
  title: string;
  message: string;
  status: EventStatus;
  created_at: string;
  acknowledged_at?: string;
  resolved_at?: string;
}

export interface VideoStatus {
  status: CameraStatus;
  is_processing: boolean;
  current_people_count: number;
  active_alerts_count: number;
  total_events_today: number;
  camera_name: string;
  location: string;
}

export interface AnalyticsData {
  total_events: number;
  total_alerts: number;
  active_alerts: number;
  current_people_count: number;
  type_breakdown: { name: string; count: number }[];
  trend_data: { day: string; events: number; people: number }[];
}

export interface SystemSettings {
  ai_confidence_threshold: number;
  inference_fps: number;
  crowd_threshold: number;
  loitering_threshold_seconds: number;
  event_cooldown_seconds: number;
}
