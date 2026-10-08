import React from 'react';
import { LayoutDashboard, Eye, Camera, History, Bell, BarChart2, Settings, Server, Cpu, Activity } from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  alertCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, alertCount }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'monitoring', label: 'Live Monitoring', icon: Eye },
    { id: 'cameras', label: 'Cameras', icon: Camera },
    { id: 'events', label: 'Events', icon: History },
    { id: 'alerts', label: 'Alerts', icon: Bell, badge: alertCount },
    { id: 'analytics', label: 'Analytics', icon: BarChart2 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-white border-r border-[#E2DFEC] flex flex-col justify-between h-[calc(100vh-61px)] sticky top-[61px] p-4 flex-shrink-0">
      
      {/* Navigation Items */}
      <div className="space-y-1">
        <p className="px-3 text-[10px] font-extrabold text-[#4F4C5F] uppercase tracking-wider mb-2">Main Menu</p>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                isActive
                  ? 'bg-[#8B7FC7] text-white shadow-sm shadow-[#8B7FC7]/20'
                  : 'text-[#242331] hover:text-[#8B7FC7] hover:bg-[#F7F6FB]'
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-[#8B7FC7]'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge !== undefined && item.badge > 0 && (
                <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full ${
                  isActive ? 'bg-white text-[#D87586]' : 'bg-[#D87586] text-white'
                }`}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Bottom Compact SOC Node Status Area */}
      <div className="bg-[#F7F6FB] border border-[#E2DFEC] rounded-xl p-3.5 space-y-2 text-[11px]">
        <div className="flex items-center justify-between text-[#4F4C5F]">
          <span className="flex items-center space-x-1.5 font-medium">
            <Server className="w-3.5 h-3.5 text-[#8B7FC7]" />
            <span>SOC Node:</span>
          </span>
          <span className="font-mono font-bold text-[#242331]">US-EAST-V1</span>
        </div>

        <div className="flex items-center justify-between text-[#4F4C5F]">
          <span className="flex items-center space-x-1.5 font-medium">
            <Cpu className="w-3.5 h-3.5 text-[#8B7FC7]" />
            <span>Engine:</span>
          </span>
          <span className="font-mono font-bold text-[#242331]">VisionForge v2.4</span>
        </div>

        <div className="flex items-center justify-between text-[#4F4C5F]">
          <span className="flex items-center space-x-1.5 font-medium">
            <Activity className="w-3.5 h-3.5 text-[#5FBF9F]" />
            <span>Latency:</span>
          </span>
          <span className="font-mono font-bold text-[#5FBF9F]">12ms</span>
        </div>
      </div>

    </aside>
  );
};
