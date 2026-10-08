import React from 'react';
import { KPICards } from '../components/KPICards';
import { VideoPlayer } from '../components/VideoPlayer';
import { AlertsPanel } from '../components/AlertsPanel';
import { SecurityEvent, SecurityAlert, VideoStatus } from '../types';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Shield, Eye, AlertTriangle } from 'lucide-react';

interface DashboardPageProps {
  videoStatus: VideoStatus;
  events: SecurityEvent[];
  alerts: SecurityAlert[];
  activeCameraCount?: number;
  onStartVideo: () => void;
  onStopVideo: () => void;
  onAcknowledgeAlert: (id: string) => void;
  onResolveAlert: (id: string) => void;
  onSelectEvent: (event: SecurityEvent) => void;
}

const mockChartData = [
  { time: '10:00', count: 1 },
  { time: '10:05', count: 2 },
  { time: '10:10', count: 5 },
  { time: '10:15', count: 3 },
  { time: '10:20', count: 6 },
  { time: '10:25', count: 4 },
];

const pieColors = ['#D87586', '#D6AE62', '#8B7FC7'];

export const DashboardPage: React.FC<DashboardPageProps> = ({
  videoStatus,
  events,
  alerts,
  activeCameraCount = 4,
  onStartVideo,
  onStopVideo,
  onAcknowledgeAlert,
  onResolveAlert,
  onSelectEvent,
}) => {
  const pieData = [
    { name: 'High / Critical', value: events.filter(e => e.severity === 'HIGH' || e.severity === 'CRITICAL').length || 2 },
    { name: 'Medium', value: events.filter(e => e.severity === 'MEDIUM').length || 1 },
    { name: 'Low', value: events.filter(e => e.severity === 'LOW').length || 1 },
  ];

  return (
    <div className="space-y-6">
      
      {/* Top KPI Cards */}
      <KPICards
        activeCameras={activeCameraCount}
        activeAlerts={alerts.filter(a => a.status === 'NEW').length}
        currentPeople={videoStatus.current_people_count}
        eventsToday={events.length}
      />

      {/* Main Monitoring & Alerts Split View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 min-h-[460px]">
          <VideoPlayer
            isProcessing={videoStatus.is_processing}
            onStart={onStartVideo}
            onStop={onStopVideo}
            peopleCount={videoStatus.current_people_count}
            cameraName={videoStatus.camera_name || 'Camera 01 (Demo Feed)'}
            location={videoStatus.location || 'Main Entrance Lobby'}
          />
        </div>
        <div className="min-h-[460px]">
          <AlertsPanel
            alerts={alerts.filter(a => a.status !== 'RESOLVED')}
            onAcknowledge={onAcknowledgeAlert}
            onResolve={onResolveAlert}
          />
        </div>
      </div>

      {/* Analytics Charts & Recent Events Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Timeline Chart */}
        <div className="bg-white border border-[#E2DFEC] p-5 rounded-xl shadow-sm">
          <h3 className="text-xs font-bold text-[#242331] tracking-wider mb-3 uppercase flex items-center space-x-2">
            <Eye className="w-4 h-4 text-[#8B7FC7]" />
            <span>People Count Trend Over Time</span>
          </h3>
          <div className="h-44">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockChartData}>
                <defs>
                  <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8B7FC7" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#8B7FC7" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="time" stroke="#AAA6BA" fontSize={10} />
                <YAxis stroke="#AAA6BA" fontSize={10} />
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2DFEC', color: '#242331', fontSize: '12px' }} />
                <Area type="monotone" dataKey="count" stroke="#8B7FC7" fillOpacity={1} fill="url(#colorCount)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Severity Distribution Pie Chart */}
        <div className="bg-white border border-[#E2DFEC] p-5 rounded-xl shadow-sm flex flex-col justify-between">
          <h3 className="text-xs font-bold text-[#242331] tracking-wider mb-2 uppercase flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-[#D6AE62]" />
            <span>Severity Breakdown</span>
          </h3>
          <div className="h-44 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={40} outerRadius={65} paddingAngle={5} dataKey="value">
                  {pieData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2DFEC', color: '#242331', fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Events List Preview */}
        <div className="bg-white border border-[#E2DFEC] p-5 rounded-xl shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-bold text-[#242331] tracking-wider mb-3 uppercase flex items-center space-x-2">
              <Shield className="w-4 h-4 text-[#8B7FC7]" />
              <span>Recent Security Triggers</span>
            </h3>
            <div className="space-y-2">
              {events.slice(0, 4).map((event) => (
                <div
                  key={event.id}
                  onClick={() => onSelectEvent(event)}
                  className="p-2.5 rounded-lg bg-[#F7F6FB] border border-[#E2DFEC] hover:border-[#8B7FC7]/40 cursor-pointer flex items-center justify-between transition text-xs"
                >
                  <div>
                    <span className="font-bold text-[#242331] block">{event.event_type}</span>
                    <span className="text-[10px] text-[#AAA6BA]">{new Date(event.timestamp).toLocaleTimeString()}</span>
                  </div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-[#D87586]/10 text-[#D87586] border border-[#D87586]/20">
                    {event.severity}
                  </span>
                </div>
              ))}
              {events.length === 0 && (
                <p className="text-xs text-[#AAA6BA] text-center py-6">No recent events logged yet.</p>
              )}
            </div>
          </div>
        </div>

      </div>

    </div>
  );
};
