import { Quest } from '../../types';
import { CheckCircle2, Circle, Trash2, Sparkles, Flame, Skull, X } from 'lucide-react';
import { Button } from '../ui/Button';
import { useState } from 'react';
interface QuestCardProps {
  quest: Quest;
  onComplete: (id: number) => void;
  onDelete: (id: number) => void;
}
const difficultyConfig = {
  easy: {
    icon: Sparkles,
    color: 'text-green-400',
    bg: 'bg-green-900/20',
    border: 'border-green-600/40',
    label: 'Легкое',
  },
  medium: {
    icon: Flame,
    color: 'text-yellow-400',
    bg: 'bg-yellow-900/20',
    border: 'border-yellow-600/40',
    label: 'Среднее',
  },
  hard: {
    icon: Skull,
    color: 'text-red-400',
    bg: 'bg-red-900/20',
    border: 'border-red-600/40',
    label: 'Сложное',
  },
};
export function QuestCard({ quest, onComplete, onDelete }: QuestCardProps) {
  const config = difficultyConfig[quest.difficulty];
  const Icon = config.icon;
  const StatusIcon = quest.completed ? CheckCircle2 : Circle;

  // Timer state
  const [timerId, setTimerId] = useState<number | null>(null);
  const [timerActive, setTimerActive] = useState(false);
  const [processingTimer, setProcessingTimer] = useState(false);

  const startTimer = async () => {
    try {
      setProcessingTimer(true);
      const resp = await fetch('/api/activities/timers/start/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token') || ''}`,
        },
        body: JSON.stringify({ activity: quest.id }),
      });
      if (!resp.ok) throw new Error('Failed to start timer');
      const data = await resp.json();
      setTimerId(data.id);
      setTimerActive(true);
    } catch (err) {
      console.error('Start timer error', err);
    } finally {
      setProcessingTimer(false);
    }
  };

  const stopTimer = async () => {
    if (!timerId) return;
    try {
      setProcessingTimer(true);
      const resp = await fetch(`/api/activities/timers/${timerId}/stop/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token') || ''}`,
        },
      });
      if (!resp.ok) throw new Error('Failed to stop timer');
      const data = await resp.json();
      setTimerActive(false);
      setTimerId(null);
      // play simple feedback sound using AudioContext (short beep)
      try {
        const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gain = audioContext.createGain();
        oscillator.type = 'sine';
        oscillator.frequency.value = 880;
        gain.gain.setValueAtTime(0.02, audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.2);
        oscillator.connect(gain);
        gain.connect(audioContext.destination);
        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.2);
      } catch (e) {
        // ignore
      }
    } catch (err) {
      console.error('Stop timer error', err);
    } finally {
      setProcessingTimer(false);
    }
  };

  return (
    <div
      className={`group relative bg-slate-950/40 border-2 rounded-lg p-4 transition-all ${
        quest.completed
          ? 'border-emerald-600/30 opacity-75'
          : `${config.border} hover:border-opacity-70`
      }`}
    >
      <div className="flex items-start gap-3">
        {/* Status Icon */}
        <button
          onClick={() => !quest.completed && onComplete(quest.id)}
          className={`flex-shrink-0 mt-1 ${!quest.completed ? 'hover:scale-110' : ''} transition-transform`}
          disabled={quest.completed}
        >
          <StatusIcon
            className={`w-6 h-6 ${
              quest.completed ? 'text-emerald-400 fill-emerald-400' : config.color
            }`}
          />
        </button>
        {/* Quest Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2 mb-2">
            <h3
              className={`text-base ${
                quest.completed
                  ? 'line-through text-emerald-200/60'
                  : 'text-amber-100'
              }`}
            >
              {quest.title}
            </h3>
            <div
              className={`flex items-center gap-1 px-2 py-1 rounded-md ${config.bg} ${config.border} border flex-shrink-0`}
            >
              <Icon className={`w-3 h-3 ${config.color}`} />
              <span className={`text-xs ${config.color}`}>+{quest.xp_reward}</span>
            </div>
          </div>
          {quest.description && (
            <p className="text-sm text-amber-200/60 mb-2">{quest.description}</p>
          )}
          <div className="flex items-center gap-2 text-xs text-amber-200/40">
            <span className={config.color}>{config.label}</span>
            {quest.focus_area && (
              <>
                <span>•</span>
                <span>Фокус: {quest.focus_area}</span>
              </>
            )}
          </div>
        </div>
        {/* Controls */}
        <div className="flex flex-col gap-2 items-end">
          {/* Timer controls */}
          {!timerActive ? (
            <Button
              variant="secondary"
              size="sm"
              onClick={startTimer}
              disabled={processingTimer}
            >
              {processingTimer ? '...' : 'Start Session'}
            </Button>
          ) : (
            <Button
              variant="secondary"
              size="sm"
              onClick={stopTimer}
              disabled={processingTimer}
            >
              {processingTimer ? '...' : 'Stop'}
            </Button>
          )}

          {/* Delete Button (shown when completed) */}
          {quest.completed && (
            <button
              className="opacity-0 group-hover:opacity-100 transition-opacity p-2 hover:bg-slate-800/50 rounded mt-2"
              onClick={() => onDelete(quest.id)}
              title="Убрать из списка"
            >
              <X className="w-4 h-4 text-amber-400/60 hover:text-red-400" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}