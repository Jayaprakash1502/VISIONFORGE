import React from 'react';
import { SecurityAlert } from '../types';
import { Bell, CheckCircle2, ShieldAlert } from 'lucide-react';

interface AlertsPageProps {
  alerts: SecurityAlert[];
  onAcknowledgeAlert: (id: string) => void;
  onResolveAlert: (id: string) => void;
}

export const AlertsPage: React.FC<AlertsPageProps> = ({ alerts, onAcknowledgeAlert, onResolveAlert }) => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between bg-white border border-[#E2DFEC] p-4 rounded-xl shadow-sm">
        <div>
          <h1 className="text-base font-bold text-[#242331] flex items-center space-x-2">
            <Bell className="w-5 h-5 text-[#D87586]" />
            <span>OPERATOR ALERT MANAGEMENT COMMAND</span>
          </h1>
          <p className="text-xs text-[#AAA6BA]">Human-in-the-loop alert acknowledgment & incident resolution center</p>
        </div>
      </div>

      <div className="space-y-4">
        {alerts.map((alert) => (
          <div key={alert.id} className="bg-white border border-[#E2DFEC] p-5 rounded-xl shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center space-x-3">
                <ShieldAlert className="w-5 h-5 text-[#D87586]" />
                <h3 className="text-sm font-bold text-[#242331]">{alert.title}</h3>
                <span className="text-[10px] font-extrabold px-2.5 py-0.5 rounded bg-[#D87586]/10 text-[#D87586] border border-[#D87586]/20">
                  {alert.severity}
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-[#F7F6FB] text-[#242331] border border-[#E2DFEC]">
                  STATUS: {alert.status}
                </span>
              </div>
              <p className="text-xs text-[#242331]/80 pl-8 leading-relaxed">{alert.message}</p>
              <p className="text-[10px] font-mono text-[#AAA6BA] pl-8">Timestamp: {new Date(alert.created_at).toLocaleString()}</p>
            </div>

            <div className="flex items-center space-x-2 self-end md:self-center">
              {alert.status === 'NEW' && (
                <button
                  onClick={() => onAcknowledgeAlert(alert.id)}
                  className="px-4 py-2 bg-[#D6AE62]/10 hover:bg-[#D6AE62]/20 text-[#D6AE62] border border-[#D6AE62]/30 text-xs font-bold rounded-lg transition"
                >
                  ACKNOWLEDGE
                </button>
              )}
              {alert.status !== 'RESOLVED' && (
                <button
                  onClick={() => onResolveAlert(alert.id)}
                  className="px-4 py-2 bg-[#5FBF9F]/10 hover:bg-[#5FBF9F]/20 text-[#5FBF9F] border border-[#5FBF9F]/30 text-xs font-bold rounded-lg transition"
                >
                  RESOLVE INCIDENT
                </button>
              )}
            </div>
          </div>
        ))}

        {alerts.length === 0 && (
          <div className="bg-white border border-[#E2DFEC] p-12 rounded-xl text-center text-[#AAA6BA] shadow-sm">
            <CheckCircle2 className="w-12 h-12 mx-auto mb-3 text-[#5FBF9F]/60" />
            <h3 className="text-sm font-bold text-[#242331]">All Alerts Resolved</h3>
            <p className="text-xs text-[#AAA6BA] mt-1">There are no pending alerts requiring human operator action.</p>
          </div>
        )}
      </div>
    </div>
  );
};
