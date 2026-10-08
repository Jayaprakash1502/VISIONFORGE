import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { DashboardPage } from './pages/DashboardPage';
import { LiveMonitoringPage } from './pages/LiveMonitoringPage';
import { CamerasPage } from './pages/CamerasPage';
import { EventsPage } from './pages/EventsPage';
import { AlertsPage } from './pages/AlertsPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { SettingsPage } from './pages/SettingsPage';
import { EventDetailModal } from './components/EventDetailModal';
import { api } from './services/api';
import { Camera, SecurityEvent, SecurityAlert, VideoStatus } from './types';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [alerts, setAlerts] = useState<SecurityAlert[]>([]);
  const [videoStatus, setVideoStatus] = useState<VideoStatus>({
    status: 'ONLINE',
    is_processing: false,
    current_people_count: 0,
    active_alerts_count: 0,
    total_events_today: 0,
    camera_name: 'Camera 01 (Demo Feed)',
    location: 'Main Entrance Lobby',
  });
  const [selectedEvent, setSelectedEvent] = useState<SecurityEvent | null>(null);

  // Poll backend APIs for status, events, and alerts
  const fetchData = async () => {
    try {
      const [cData, eData, aData, vData] = await Promise.all([
        api.getCameras().catch(() => []),
        api.getEvents().catch(() => []),
        api.getAlerts().catch(() => []),
        api.getVideoStatus().catch(() => videoStatus),
      ]);
      setCameras(cData);
      setEvents(eData);
      setAlerts(aData);
      setVideoStatus(vData);
    } catch (err) {
      console.warn('API polling update warning:', err);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  // WebSocket for Instant Real-Time Alert Push
  useEffect(() => {
    let ws: WebSocket | null = null;
    try {
      ws = new WebSocket('ws://127.0.0.1:8000/ws/events');
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'alert.created' && data.alert) {
            setAlerts((prev) => [data.alert, ...prev]);
            if (data.event) {
              setEvents((prev) => [data.event, ...prev]);
            }
          }
        } catch (e) {
          console.error('WS parse error:', e);
        }
      };
    } catch (e) {
      console.warn('WebSocket connection failed, relying on polling fallback:', e);
    }
    return () => {
      if (ws) ws.close();
    };
  }, []);

  const handleStartVideo = async () => {
    await api.startVideo();
    fetchData();
  };

  const handleStopVideo = async () => {
    await api.stopVideo();
    fetchData();
  };

  const handleAcknowledgeAlert = async (id: string) => {
    await api.acknowledgeAlert(id);
    fetchData();
  };

  const handleResolveAlert = async (id: string) => {
    await api.resolveAlert(id);
    fetchData();
  };

  return (
    <div className="min-h-screen bg-soc-bg text-slate-100 flex flex-col font-sans">
      
      {/* Top Navbar Header */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isProcessing={videoStatus.is_processing}
        alertCount={alerts.filter((a) => a.status === 'NEW').length}
      />

      {/* Main Page Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6">
        {activeTab === 'dashboard' && (
          <DashboardPage
            videoStatus={videoStatus}
            events={events}
            alerts={alerts}
            activeCameraCount={cameras.length || 4}
            onStartVideo={handleStartVideo}
            onStopVideo={handleStopVideo}
            onAcknowledgeAlert={handleAcknowledgeAlert}
            onResolveAlert={handleResolveAlert}
            onSelectEvent={setSelectedEvent}
          />
        )}

        {activeTab === 'monitoring' && (
          <LiveMonitoringPage
            cameras={cameras}
            videoStatus={videoStatus}
            onStartVideo={handleStartVideo}
            onStopVideo={handleStopVideo}
          />
        )}

        {activeTab === 'cameras' && <CamerasPage cameras={cameras} onRefreshCameras={fetchData} />}

        {activeTab === 'events' && (
          <EventsPage events={events} onSelectEvent={setSelectedEvent} />
        )}

        {activeTab === 'alerts' && (
          <AlertsPage
            alerts={alerts}
            onAcknowledgeAlert={handleAcknowledgeAlert}
            onResolveAlert={handleResolveAlert}
          />
        )}

        {activeTab === 'analytics' && <AnalyticsPage events={events} />}

        {activeTab === 'settings' && <SettingsPage />}
      </main>

      {/* Event Details Modal */}
      <EventDetailModal event={selectedEvent} onClose={() => setSelectedEvent(null)} />

      {/* Footer */}
      <footer className="bg-slate-950 border-t border-slate-900 py-3 text-center text-xs text-slate-500">
        <p>VISIONFORGE Security Operations Center &copy; 2026. Making Existing Surveillance Systems Intelligent.</p>
      </footer>
    </div>
  );
};
