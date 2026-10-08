import React, { useEffect, useState } from 'react';
import { Settings, Save, Check, Cpu, Server, Activity, Database } from 'lucide-react';
import { api } from '../services/api';

export const SettingsPage: React.FC = () => {
  const [crowdThreshold, setCrowdThreshold] = useState(8);
  const [loiteringSeconds, setLoiteringSeconds] = useState(20);
  const [confidence, setConfidence] = useState(0.45);
  const [cooldown, setCooldown] = useState(10);
  const [saved, setSaved] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api.getSettings().then((s) => {
      if (s) {
        if (s.crowd_threshold) setCrowdThreshold(s.crowd_threshold);
        if (s.loitering_threshold_seconds) setLoiteringSeconds(s.loitering_threshold_seconds);
        if (s.ai_confidence_threshold) setConfidence(s.ai_confidence_threshold);
        if (s.event_cooldown_seconds) setCooldown(s.event_cooldown_seconds);
      }
    }).catch((e) => console.warn('Failed to load settings from backend:', e));
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      await api.updateSettings({
        crowd_threshold: crowdThreshold,
        loitering_threshold_seconds: loiteringSeconds,
        ai_confidence_threshold: confidence,
        event_cooldown_seconds: cooldown,
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error('Failed to update settings:', err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex items-center justify-between bg-white border border-[#E2DFEC] p-4 rounded-xl shadow-sm">
        <div>
          <h1 className="text-base font-bold text-[#242331] flex items-center space-x-2">
            <Settings className="w-5 h-5 text-[#8B7FC7]" />
            <span>SYSTEM STATUS & RULE CONFIGURATION</span>
          </h1>
          <p className="text-xs text-[#AAA6BA]">Engine health, active detection algorithms, and threshold parameters</p>
        </div>
      </div>

      {/* System Status Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 bg-white border border-[#E2DFEC] rounded-xl shadow-sm space-y-1">
          <div className="flex items-center space-x-2 text-[#AAA6BA] text-xs">
            <Server className="w-4 h-4 text-[#8B7FC7]" />
            <span>API Backend</span>
          </div>
          <p className="text-sm font-bold text-[#5FBF9F]">Connected</p>
          <p className="text-[10px] text-[#AAA6BA] font-mono">http://127.0.0.1:8000</p>
        </div>

        <div className="p-4 bg-white border border-[#E2DFEC] rounded-xl shadow-sm space-y-1">
          <div className="flex items-center space-x-2 text-[#AAA6BA] text-xs">
            <Activity className="w-4 h-4 text-[#8B7FC7]" />
            <span>WebSocket Stream</span>
          </div>
          <p className="text-sm font-bold text-[#5FBF9F]">Connected</p>
          <p className="text-[10px] text-[#AAA6BA] font-mono">/ws/events</p>
        </div>

        <div className="p-4 bg-white border border-[#E2DFEC] rounded-xl shadow-sm space-y-1">
          <div className="flex items-center space-x-2 text-[#AAA6BA] text-xs">
            <Cpu className="w-4 h-4 text-[#8B7FC7]" />
            <span>AI Engine</span>
          </div>
          <p className="text-sm font-bold text-[#242331]">YOLOv8n / OpenCV</p>
          <p className="text-[10px] text-[#AAA6BA]">Active Fallback Ready</p>
        </div>

        <div className="p-4 bg-white border border-[#E2DFEC] rounded-xl shadow-sm space-y-1">
          <div className="flex items-center space-x-2 text-[#AAA6BA] text-xs">
            <Database className="w-4 h-4 text-[#8B7FC7]" />
            <span>Event Store</span>
          </div>
          <p className="text-sm font-bold text-[#242331]">Memory Store Fallback</p>
          <p className="text-[10px] text-[#AAA6BA]">PostgreSQL Offline</p>
        </div>
      </div>

      {/* Threshold Configuration Panel */}
      <div className="bg-white border border-[#E2DFEC] p-6 rounded-xl space-y-6 shadow-sm text-xs">
        
        {/* Crowd Threshold */}
        <div className="space-y-2">
          <div className="flex justify-between font-bold text-[#242331]">
            <label>Crowd Density Threshold (People Count)</label>
            <span className="text-[#8B7FC7] font-mono">{crowdThreshold} Persons</span>
          </div>
          <input
            type="range"
            min="2"
            max="30"
            value={crowdThreshold}
            onChange={(e) => setCrowdThreshold(Number(e.target.value))}
            className="w-full accent-[#8B7FC7]"
          />
          <p className="text-[#AAA6BA]">Triggers a CROWD_DETECTED event when person count exceeds this number.</p>
        </div>

        {/* Loitering Threshold */}
        <div className="space-y-2 pt-4 border-t border-[#E2DFEC]">
          <div className="flex justify-between font-bold text-[#242331]">
            <label>Loitering Duration Threshold (Seconds)</label>
            <span className="text-[#D6AE62] font-mono">{loiteringSeconds} Seconds</span>
          </div>
          <input
            type="range"
            min="5"
            max="60"
            value={loiteringSeconds}
            onChange={(e) => setLoiteringSeconds(Number(e.target.value))}
            className="w-full accent-[#D6AE62]"
          />
          <p className="text-[#AAA6BA]">Triggers a LOITERING event when a person remains inside a monitored region past this duration.</p>
        </div>

        {/* Confidence Threshold */}
        <div className="space-y-2 pt-4 border-t border-[#E2DFEC]">
          <div className="flex justify-between font-bold text-[#242331]">
            <label>YOLO AI Detection Confidence Threshold</label>
            <span className="text-[#5FBF9F] font-mono">{Math.round(confidence * 100)}%</span>
          </div>
          <input
            type="range"
            min="0.20"
            max="0.90"
            step="0.05"
            value={confidence}
            onChange={(e) => setConfidence(Number(e.target.value))}
            className="w-full accent-[#5FBF9F]"
          />
          <p className="text-[#AAA6BA]">Minimum confidence score required for YOLO person detection bounding boxes.</p>
        </div>

        {/* Event Cooldown */}
        <div className="space-y-2 pt-4 border-t border-[#E2DFEC]">
          <div className="flex justify-between font-bold text-[#242331]">
            <label>Event Cooldown / Debounce (Seconds)</label>
            <span className="text-[#8B7FC7] font-mono">{cooldown} Seconds</span>
          </div>
          <input
            type="range"
            min="3"
            max="60"
            value={cooldown}
            onChange={(e) => setCooldown(Number(e.target.value))}
            className="w-full accent-[#8B7FC7]"
          />
          <p className="text-[#AAA6BA]">Minimum delay between duplicate alerts for the same camera zone.</p>
        </div>

        {/* Action Button */}
        <div className="pt-4 border-t border-[#E2DFEC] flex items-center justify-between">
          {saved ? (
            <span className="text-[#5FBF9F] font-bold flex items-center space-x-1">
              <Check className="w-4 h-4" />
              <span>Settings Saved Successfully!</span>
            </span>
          ) : (
            <span className="text-[#AAA6BA]">Changes apply dynamically to AI engine</span>
          )}
          <button
            onClick={handleSave}
            disabled={saving}
            className="flex items-center space-x-2 bg-[#8B7FC7] hover:bg-[#A99BE0] text-white px-5 py-2 rounded-lg text-xs font-semibold shadow-sm transition disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            <span>{saving ? 'Saving...' : 'Save Settings'}</span>
          </button>
        </div>

      </div>
    </div>
  );
};
