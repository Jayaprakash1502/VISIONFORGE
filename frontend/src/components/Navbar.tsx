import React from 'react';
import { Shield, LayoutDashboard, Eye, Camera, History, Bell, BarChart2, Settings } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  alertCount: number;
  isProcessing?: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab, alertCount, isProcessing }) => {
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
    <header className="bg-white border-b border-[#E2DFEC] sticky top-0 z-50 px-6 py-3.5 shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand */}
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
          <div className="bg-[#8B7FC7]/10 p-2.5 rounded-xl border border-[#8B7FC7]/20">
            <Shield className="w-6 h-6 text-[#8B7FC7]" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg tracking-wider text-[#242331]">VISIONFORGE</span>
              <span className="bg-[#8B7FC7]/10 text-[#8B7FC7] text-[10px] font-bold px-2 py-0.5 rounded border border-[#8B7FC7]/30">
                SOC v1.0
              </span>
            </div>
            <p className="text-xs text-[#4F4C5F] font-medium">AI Based Intelligent Video Analytics Platform</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center space-x-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-[#8B7FC7] text-white shadow-md shadow-[#8B7FC7]/20'
                    : 'text-[#242331] hover:text-[#8B7FC7] hover:bg-[#F7F6FB]'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-[#8B7FC7]'}`} />
                <span>{item.label}</span>
                {item.badge !== undefined && item.badge > 0 && (
                  <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded-full ${
                    isActive ? 'bg-white text-[#D87586]' : 'bg-[#D87586] text-white'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Header Right Tag */}
        <div className="flex items-center">
          <span className="bg-[#8B7FC7]/10 text-[#8B7FC7] text-xs font-semibold px-3 py-1 rounded-md border border-[#8B7FC7]/20 font-mono">
            DEMO MODE
          </span>
        </div>

      </div>
    </header>
  );
};
