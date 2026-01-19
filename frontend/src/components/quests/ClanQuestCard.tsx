import { ClanQuest } from '../../types';
import { Users, Crown, Clock, TrendingUp } from 'lucide-react';
import { Button } from '../ui/Button';
import { useState } from 'react';
interface ClanQuestCardProps {
  quest: ClanQuest;
  onContribute: (id: number, contribution: number) => void;
  currentUsername: string;
}
export function ClanQuestCard({ quest, onContribute, currentUsername }: ClanQuestCardProps) {
  const [contributionAmount, setContributionAmount] = useState(1);
  const [isContributing, setIsContributing] = useState(false);
  const progressPercentage = (quest.total_progress / quest.required_progress) * 100;
  const isEpic = quest.difficulty === 'epic';
  const userParticipation = quest.participants.find(p => p.username === currentUsername);
  const handleContribute = async () => {
    setIsContributing(true);
    await onContribute(quest.id, contributionAmount);
    setIsContributing(false);
  };
  const getDaysLeft = () => {
    const now = new Date();
    const expiresAt = new Date(quest.expires_at);
    const diffTime = expiresAt.getTime() - now.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };
  return (
    <div
      className={`bg-slate-950/40 rounded-lg border-2 p-6 transition-all ${
        quest.completed
          ? 'border-emerald-600/30 opacity-75'
          : isEpic
          ? 'border-purple-500/50 shadow-lg shadow-purple-500/20'
          : 'border-orange-500/50 shadow-lg shadow-orange-500/20'
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-4 mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <Crown className={`w-5 h-5 ${isEpic ? 'text-purple-400' : 'text-orange-400'}`} />
            <span className={`text-xs px-2 py-1 rounded ${
              isEpic ? 'bg-purple-900/30 text-purple-300' : 'bg-orange-900/30 text-orange-300'
            }`}>
              {isEpic ? 'Эпическое' : 'Легендарное'}
            </span>
          </div>
          <h3 className={`text-lg mb-2 ${quest.completed ? 'text-emerald-200 line-through' : 'text-amber-100'}`}>
            {quest.title}
          </h3>
          <p className="text-amber-200/60 text-sm">{quest.description}</p>
        </div>
        <div className="text-right flex-shrink-0">
          <div className={`text-2xl ${isEpic ? 'text-purple-300' : 'text-orange-300'}`}>
            +{quest.xp_reward}
          </div>
          <div className="text-xs text-amber-200/40">XP награда</div>
        </div>
      </div>
      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex justify-between text-sm text-amber-200/80 mb-2">
          <span>Прогресс</span>
          <span>{quest.total_progress} / {quest.required_progress}</span>
        </div>
        <div className="w-full h-4 bg-slate-950/50 rounded-full overflow-hidden border border-amber-600/30">
          <div
            className={`h-full transition-all duration-500 ${
              isEpic 
                ? 'bg-gradient-to-r from-purple-600 to-purple-400' 
                : 'bg-gradient-to-r from-orange-600 to-orange-400'
            }`}
            style={{ width: `${Math.min(progressPercentage, 100)}%` }}
          />
        </div>
      </div>
      {/* Participants */}
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-2">
          <Users className="w-4 h-4 text-amber-400" />
          <span className="text-sm text-amber-200/80">Участники ({quest.participants.length})</span>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {quest.participants.slice(0, 6).map((participant) => (
            <div
              key={participant.id}
              className={`flex items-center justify-between p-2 rounded bg-slate-800/50 border ${
                participant.username === currentUsername
                  ? 'border-amber-500/50'
                  : 'border-slate-700/50'
              }`}
            >
              <div>
                <p className="text-amber-200 text-sm">{participant.username}</p>
                <p className="text-amber-200/40 text-xs">Уровень {participant.level}</p>
              </div>
              <div className="text-right">
                <div className="text-amber-300 text-sm">+{participant.contribution}</div>
                <TrendingUp className="w-3 h-3 text-amber-400/60 ml-auto" />
              </div>
            </div>
          ))}
        </div>
        {quest.participants.length > 6 && (
          <p className="text-amber-200/40 text-xs text-center mt-2">
            +{quest.participants.length - 6} ещё участников
          </p>
        )}
      </div>
      {/* Time Left */}
      <div className="flex items-center gap-2 mb-4 p-3 bg-slate-800/50 rounded border border-amber-600/20">
        <Clock className="w-4 h-4 text-amber-400" />
        <span className="text-sm text-amber-200/80">
          Осталось дней: <span className="text-amber-300">{getDaysLeft()}</span>
        </span>
      </div>
      {/* Contribution Section */}
      {!quest.completed && (
        <div className="flex items-center gap-3">
          <input
            type="number"
            min="1"
            max="10"
            value={contributionAmount}
            onChange={(e) => setContributionAmount(Math.max(1, Math.min(10, parseInt(e.target.value) || 1)))}
            className="w-20 bg-slate-950/50 border border-amber-600/30 rounded px-3 py-2 text-amber-100 text-center focus:outline-none focus:border-amber-500"
          />
          <Button
            onClick={handleContribute}
            disabled={isContributing}
            className="flex-1"
          >
            {isContributing ? 'Отправка...' : 'Внести вклад'}
          </Button>
        </div>
      )}
      {/* User Contribution */}
      {userParticipation && (
        <div className="mt-3 p-2 bg-amber-900/20 rounded border border-amber-600/30">
          <p className="text-amber-200 text-sm">
            Ваш вклад: <span className="text-amber-300">+{userParticipation.contribution}</span>
          </p>
        </div>
      )}
    </div>
  );
}