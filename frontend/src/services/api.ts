import axios from 'axios';
import { Camera, SecurityEvent, SecurityAlert, VideoStatus, AnalyticsData, SystemSettings } from '../types';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
const API_BASE = `${BASE_URL}/api`;

export const api = {
  getHealth: async () => {
    const res = await axios.get(`${API_BASE}/health`);
    return res.data;
  },
  getCameras: async (): Promise<Camera[]> => {
    const res = await axios.get(`${API_BASE}/cameras`);
    return res.data;
  },
  createCamera: async (camera: Partial<Camera>): Promise<Camera> => {
    const res = await axios.post(`${API_BASE}/cameras`, camera);
    return res.data;
  },
  getEvents: async (params?: { event_type?: string; severity?: string; status?: string; search?: string }): Promise<SecurityEvent[]> => {
    const res = await axios.get(`${API_BASE}/events`, { params });
    return res.data;
  },
  getAlerts: async (params?: { status?: string; severity?: string }): Promise<SecurityAlert[]> => {
    const res = await axios.get(`${API_BASE}/alerts`, { params });
    return res.data;
  },
  acknowledgeAlert: async (id: string): Promise<SecurityAlert> => {
    const res = await axios.post(`${API_BASE}/alerts/${id}/acknowledge`);
    return res.data;
  },
  resolveAlert: async (id: string): Promise<SecurityAlert> => {
    const res = await axios.post(`${API_BASE}/alerts/${id}/resolve`);
    return res.data;
  },
  startVideo: async () => {
    const res = await axios.post(`${API_BASE}/video/start`);
    return res.data;
  },
  stopVideo: async () => {
    const res = await axios.post(`${API_BASE}/video/stop`);
    return res.data;
  },
  getVideoStatus: async (): Promise<VideoStatus> => {
    const res = await axios.get(`${API_BASE}/video/status`);
    return res.data;
  },
  getSettings: async (): Promise<SystemSettings> => {
    const res = await axios.get(`${API_BASE}/settings`);
    return res.data;
  },
  updateSettings: async (settings: Partial<SystemSettings>): Promise<SystemSettings> => {
    const res = await axios.put(`${API_BASE}/settings`, settings);
    return res.data;
  },
  getAnalytics: async (): Promise<AnalyticsData> => {
    const res = await axios.get(`${API_BASE}/analytics`);
    return res.data;
  }
};
