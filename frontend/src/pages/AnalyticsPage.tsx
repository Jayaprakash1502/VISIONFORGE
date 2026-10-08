import React, { useEffect, useState } from 'react';
import { SecurityEvent, AnalyticsData } from '../types';
import { BarChart2, TrendingUp, PieChart as PieIcon } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import { api } from '../services/api';

interface AnalyticsPageProps {
  events: SecurityEvent[];
}

export const AnalyticsPage: React.FC<AnalyticsPageProps> = ({ events }) => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);

  useEffect(() => {
    api.getAnalytics().then(setAnalytics).catch((err) => console.warn('Analytics fetch error:', err));
  }, [events]);

  const trendData = analytics?.trend_data || [
    { day: 'Mon', events: 4, people: 12 },
    { day: 'Tue', events: 8, people: 25 },
    { day: 'Wed', events: 3, people: 15 },
    { day: 'Thu', events: 9, people: 30 },
    { day: 'Fri', events: 6, people: 18 },
    { day: 'Sat', events: 11, people: 42 },
    { day: 'Sun', events: events.length || 18, people: 12 },
  ];

  const typeData = analytics?.type_breakdown?.length ? analytics.type_breakdown : [
    { name: 'RESTRICTED_AREA_ENTRY', count: events.filter(e => e.event_type === 'RESTRICTED_AREA_ENTRY').length || 10 },
    { name: 'CROWD_DETECTED', count: events.filter(e => e.event_type === 'CROWD_DETECTED').length || 5 },
    { name: 'LOITERING', count: events.filter(e => e.event_type === 'LOITERING').length || 3 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between bg-white border border-[#E2DFEC] p-4 rounded-xl shadow-sm">
        <div>
          <h1 className="text-base font-bold text-[#242331] flex items-center space-x-2">
            <BarChart2 className="w-5 h-5 text-[#8B7FC7]" />
            <span>SECURITY ANALYTICS & INSIGHTS</span>
          </h1>
          <p className="text-xs text-[#AAA6BA]">Time-series metrics and event distribution breakdown</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Events & People Trend Chart */}
        <div className="bg-white border border-[#E2DFEC] p-5 rounded-xl shadow-sm space-y-4">
          <h3 className="text-xs font-bold text-[#242331] uppercase tracking-wider flex items-center space-x-2">
            <TrendingUp className="w-4 h-4 text-[#8B7FC7]" />
            <span>Weekly Event & People Count Trend</span>
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <XAxis dataKey="day" stroke="#AAA6BA" fontSize={11} />
                <YAxis stroke="#AAA6BA" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2DFEC', color: '#242331', fontSize: '12px' }} />
                <Line type="monotone" dataKey="events" stroke="#D87586" strokeWidth={2} name="Events Triggered" />
                <Line type="monotone" dataKey="people" stroke="#8B7FC7" strokeWidth={2} name="Max People Observed" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Events by Type Bar Chart */}
        <div className="bg-white border border-[#E2DFEC] p-5 rounded-xl shadow-sm space-y-4">
          <h3 className="text-xs font-bold text-[#242331] uppercase tracking-wider flex items-center space-x-2">
            <PieIcon className="w-4 h-4 text-[#D6AE62]" />
            <span>Events Distribution by Category</span>
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={typeData}>
                <XAxis dataKey="name" stroke="#AAA6BA" fontSize={10} />
                <YAxis stroke="#AAA6BA" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2DFEC', color: '#242331', fontSize: '12px' }} />
                <Bar dataKey="count" fill="#8B7FC7" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>
    </div>
  );
};
