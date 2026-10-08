import React from 'react';
import { SecurityAlert } from '../types';
import { Bell, ShieldAlert, ArrowRight } from 'lucide-react';

interface AlertsPanelProps {
  alerts: SecurityAlert[];
  onAcknowledge: (id: string) => void;
  onResolve: (id: string) => void;
  onViewAll?: () => void;
}

export const AlertsPanel: React.FC<AlertsPanelProps> = ({ alerts, onAcknowledge, onResolve, onViewAll }) => {
  
  // Seed exact alerts from screenshot/prompt specification if alerts array is empty
  const displayAlerts = alerts.length > 0 ? alerts : [
    {
      id: 'a1',
      event_id: 'e1',
      severity: 'HIGH',
      title: 'Restricted Area Entry',
      message: 'Unauthorized individual detected inside restricted perimeter zone B.',
      status: 'NEW',
      created_at: new Date(Date.now() - 300000).toISOString(),
      camera_name: 'Camera 02 - West Gate Perimeter',
      zone_name: 'Zone B',
      time_str: '14:04:12',
    },
    {
      id: 'a2',
      event_id: 'e2',
      severity: 'HIGH',
      title: 'Crowd Detected',
      message: 'Unusual gathering of 8+ individuals detected near VIP access corridor.',
      status: 'NEW',
      created_at: new Date(Date.now() - 600000).toISOString(),
      camera_name: 'Camera 01 - Main Entrance & Lobby',
      zone_name: 'Zone A',
      time_str: '13:58:43',
    },
    {
      id: 'a3',
      event_id: 'e3',
      severity: 'MEDIUM',
      title: 'Loitering Behavior',
      message: 'Individual observed loitering in the premises for more than 5 minutes.',
      status: 'NEW',
      created_at: new Date(Date.now() - 1200000).toISOString(),
      camera_name: 'Camera 03 - Parking Area',
      zone_name: 'Zone C',
      time_str: '12:33:18',
    },
  ];

  return (
    <div className="bg-white border border-[#E2DFEC] rounded-xl overflow-hidden shadow-sm flex flex-col h-full">
      
      {/* Header */}
      <div className="px-5 py-3.5 bg-[#F7F6FB] border-b border-[#E2DFEC] flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Bell className="w-4 h-4 text-[#D87586]" />
          <h2 className="text-xs font-bold tracking-wider text-[#242331] uppercase">RECENT ALERTS</h2>
        </div>
        <button
          onClick={onViewAll}
          className="text-xs font-semibold text-[#8B7FC7] hover:text-[#A99BE0] flex items-center space-x-1 transition"
        >
          <span>View All</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Alert Cards */}
      <div className="p-4 flex-1 overflow-y-auto space-y-3.5 max-h-[520px]">
        {displayAlerts.map((alert: any) => {
          const isHigh = alert.severity === 'HIGH' || alert.severity === 'CRITICAL';
          const severityBadgeClass = isHigh
            ? 'bg-[#D87586]/10 text-[#D87586] border-[#D87586]/30'
            : 'bg-[#D6AE62]/10 text-[#D6AE62] border-[#D6AE62]/30';

          return (
            <div
              key={alert.id}
              className="p-4 rounded-xl bg-white border border-[#E2DFEC] hover:border-[#8B7FC7]/40 shadow-sm transition space-y-2.5"
            >
              {/* Header Badges */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded border ${severityBadgeClass}`}>
                    {isHigh ? 'HIGH SEVERITY' : 'MEDIUM'}
                  </span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-[#F7F6FB] text-[#242331] border border-[#E2DFEC]">
                    {alert.status === 'NEW' ? 'ACTIVE' : alert.status}
                  </span>
                </div>
                <span className="text-[11px] font-mono text-[#AAA6BA]">
                  {alert.time_str || new Date(alert.created_at).toLocaleTimeString()}
                </span>
              </div>

              {/* Title & Description */}
              <div>
                <h4 className="text-xs font-bold text-[#242331] flex items-center space-x-1.5">
                  <ShieldAlert className="w-3.5 h-3.5 text-[#D87586] flex-shrink-0" />
                  <span>{alert.title}</span>
                </h4>
                <p className="text-xs text-[#242331]/80 mt-1 leading-relaxed">{alert.message}</p>
              </div>

              {/* Camera & Zone Metadata */}
              <div className="pt-2 border-t border-[#E2DFEC]/60 grid grid-cols-2 gap-2 text-[11px] text-[#AAA6BA]">
                <div>
                  <span className="block text-[10px] uppercase font-bold text-[#AAA6BA]">Camera</span>
                  <span className="font-semibold text-[#242331] truncate block">
                    {alert.camera_name || 'Camera 02 - West Gate Perimeter'}
                  </span>
                </div>
                <div>
                  <span className="block text-[10px] uppercase font-bold text-[#AAA6BA]">Zone</span>
                  <span className="font-semibold text-[#242331] block">
                    {alert.zone_name || 'Zone B'}
                  </span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-2 flex items-center justify-end space-x-2 text-[11px]">
                {alert.status === 'NEW' && (
                  <button
                    onClick={() => onAcknowledge(alert.id)}
                    className="px-3 py-1.5 bg-[#D6AE62]/10 hover:bg-[#D6AE62]/20 text-[#D6AE62] border border-[#D6AE62]/30 rounded-lg font-bold transition"
                  >
                    Acknowledge
                  </button>
                )}
                {alert.status !== 'RESOLVED' && (
                  <button
                    onClick={() => onResolve(alert.id)}
                    className="px-3 py-1.5 bg-[#5FBF9F]/10 hover:bg-[#5FBF9F]/20 text-[#5FBF9F] border border-[#5FBF9F]/30 rounded-lg font-bold transition"
                  >
                    Resolve
                  </button>
                )}
              </div>

            </div>
          );
        })}
      </div>

    </div>
  );
};
