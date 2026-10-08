import React from 'react';
import { Camera, Bell, Users, Activity } from 'lucide-react';

interface KPICardsProps {
  activeCameras: number;
  activeAlerts: number;
  currentPeople: number;
  eventsToday: number;
}

export const KPICards: React.FC<KPICardsProps> = ({
  activeCameras,
  activeAlerts,
  currentPeople,
  eventsToday,
}) => {
  const cards = [
    {
      title: 'ACTIVE CAMERAS',
      value: activeCameras !== undefined ? activeCameras : 4,
      subtitle: `100% Operational (${activeCameras || 4} total)`,
      icon: Camera,
      badgeColor: 'text-[#5FBF9F]',
      iconColor: 'text-[#8B7FC7]',
    },
    {
      title: 'PEOPLE DETECTED',
      value: currentPeople !== undefined ? currentPeople : 13,
      subtitle: 'Across all 4 active zones',
      icon: Users,
      badgeColor: 'text-[#242331]',
      iconColor: 'text-[#8B7FC7]',
    },
    {
      title: 'ACTIVE ALERTS',
      value: activeAlerts !== undefined ? activeAlerts : 3,
      subtitle: activeAlerts > 0 ? 'Requires Operator Action' : 'All Incidents Resolved',
      icon: Bell,
      badgeColor: activeAlerts > 0 ? 'text-[#D87586]' : 'text-[#5FBF9F]',
      iconColor: activeAlerts > 0 ? 'text-[#D87586]' : 'text-[#5FBF9F]',
    },
    {
      title: 'EVENTS TODAY',
      value: eventsToday !== undefined ? eventsToday : 18,
      subtitle: 'Logged in audit trail',
      icon: Activity,
      badgeColor: 'text-[#242331]',
      iconColor: 'text-[#8B7FC7]',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className="p-4 bg-white border border-[#E2DFEC] rounded-xl shadow-sm flex items-center justify-between"
          >
            <div>
              <p className="text-[10px] font-extrabold tracking-wider text-[#4F4C5F] uppercase">{card.title}</p>
              <h3 className={`text-2xl font-extrabold mt-0.5 ${card.badgeColor}`}>{card.value}</h3>
              <p className="text-[11px] text-[#6B687A] font-medium mt-0.5">{card.subtitle}</p>
            </div>
            <div className="p-3 rounded-xl bg-[#F7F6FB] border border-[#E2DFEC]">
              <Icon className={`w-5 h-5 ${card.iconColor}`} />
            </div>
          </div>
        );
      })}
    </div>
  );
};
