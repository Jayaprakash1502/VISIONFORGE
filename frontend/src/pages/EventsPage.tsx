import React, { useState } from 'react';
import { SecurityEvent } from '../types';
import { History, Search, Eye } from 'lucide-react';

interface EventsPageProps {
  events: SecurityEvent[];
  onSelectEvent: (event: SecurityEvent) => void;
}

export const EventsPage: React.FC<EventsPageProps> = ({ events, onSelectEvent }) => {
  const [search, setSearch] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('');

  const filteredEvents = events.filter((e) => {
    const matchesSearch = !search || e.description?.toLowerCase().includes(search.toLowerCase()) || e.event_type.toLowerCase().includes(search.toLowerCase());
    const matchesSeverity = !severityFilter || e.severity === severityFilter;
    const matchesType = !typeFilter || e.event_type === typeFilter;
    return matchesSearch && matchesSeverity && matchesType;
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between bg-white border border-[#E2DFEC] p-4 rounded-xl shadow-sm">
        <div>
          <h1 className="text-base font-bold text-[#242331] flex items-center space-x-2">
            <History className="w-5 h-5 text-[#8B7FC7]" />
            <span>EVENT HISTORY & AUDIT TRAIL</span>
          </h1>
          <p className="text-xs text-[#AAA6BA]">Complete audit log of AI detections and rule breaches</p>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-white border border-[#E2DFEC] p-4 rounded-xl flex flex-wrap gap-4 items-center shadow-sm">
        <div className="flex-1 min-w-[240px] relative">
          <Search className="w-4 h-4 text-[#AAA6BA] absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search events by description or type..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-[#F7F6FB] border border-[#E2DFEC] rounded-lg pl-9 pr-3 py-1.5 text-xs text-[#242331]"
          />
        </div>

        <select
          value={severityFilter}
          onChange={(e) => setSeverityFilter(e.target.value)}
          className="bg-[#F7F6FB] border border-[#E2DFEC] rounded-lg px-3 py-1.5 text-xs text-[#242331]"
        >
          <option value="">All Severities</option>
          <option value="CRITICAL">CRITICAL</option>
          <option value="HIGH">HIGH</option>
          <option value="MEDIUM">MEDIUM</option>
          <option value="LOW">LOW</option>
        </select>

        <select
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
          className="bg-[#F7F6FB] border border-[#E2DFEC] rounded-lg px-3 py-1.5 text-xs text-[#242331]"
        >
          <option value="">All Event Types</option>
          <option value="RESTRICTED_AREA_ENTRY">RESTRICTED_AREA_ENTRY</option>
          <option value="CROWD_DETECTED">CROWD_DETECTED</option>
          <option value="LOITERING">LOITERING</option>
        </select>
      </div>

      {/* Events Table */}
      <div className="bg-white border border-[#E2DFEC] rounded-xl overflow-hidden shadow-sm">
        <table className="w-full text-left text-xs">
          <thead className="bg-[#F7F6FB] text-[#AAA6BA] border-b border-[#E2DFEC] uppercase text-[10px] tracking-wider">
            <tr>
              <th className="p-3.5">Time</th>
              <th className="p-3.5">Event Type</th>
              <th className="p-3.5">Location</th>
              <th className="p-3.5">Severity</th>
              <th className="p-3.5">Status</th>
              <th className="p-3.5 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#E2DFEC]">
            {filteredEvents.map((evt) => (
              <tr key={evt.id} className="hover:bg-[#F7F6FB] transition">
                <td className="p-3.5 text-[#AAA6BA] font-mono">{new Date(evt.timestamp).toLocaleString()}</td>
                <td className="p-3.5 font-bold text-[#242331]">{evt.event_type}</td>
                <td className="p-3.5 text-[#AAA6BA]">{evt.location || 'Main Lobby'}</td>
                <td className="p-3.5">
                  <span className="font-extrabold text-[10px] px-2 py-0.5 rounded bg-[#D87586]/10 text-[#D87586] border border-[#D87586]/20">
                    {evt.severity}
                  </span>
                </td>
                <td className="p-3.5">
                  <span className="font-bold text-[#5FBF9F]">{evt.status}</span>
                </td>
                <td className="p-3.5 text-right">
                  <button
                    onClick={() => onSelectEvent(evt)}
                    className="inline-flex items-center space-x-1 text-[#8B7FC7] hover:text-[#A99BE0] font-semibold"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    <span>Details</span>
                  </button>
                </td>
              </tr>
            ))}
            {filteredEvents.length === 0 && (
              <tr>
                <td colSpan={6} className="text-center py-12 text-[#AAA6BA]">
                  No security events match the current filter.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
