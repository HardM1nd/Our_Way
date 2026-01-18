import { User } from '../../types';
import { Sparkles, Trophy } from 'lucide-react';
import { useCustomization } from '../../hooks/useCustomization';
interface CharacterProfileProps {
  user: User;
  questsCompletedToday: number;
}
export function CharacterProfile({ user, questsCompletedToday }: CharacterProfileProps) {
  const { settings } = useCustomization();
  const isLight = settings.theme === 'light';
  const xpPercentage = (user.xp / user.xp_to_next_level) * 100;
  return (
    <div className={`rounded-lg border-2 p-6 shadow-2xl backdrop-blur-sm ${
      isLight
        ? 'bg-white/90 border-purple-300'
        : 'bg-gradient-to-br from-slate-800/90 to-slate-900/90 border-purple-600/50'
    }`}>
      {/* Character Name */}
      <div className="text-center mb-6">
        <h2 className={isLight ? 'text-amber-800' : 'text-amber-300'}>
          {user.username}
        </h2>
        <p className={isLight ? 'text-amber-600' : 'text-amber-200/60'}>
          Авантюрист {user.level} уровня
        </p>
      </div>
      {/* XP Bar */}
      <div className="mb-6">
        <div className={`flex justify-between text-sm mb-2 ${
          isLight ? 'text-amber-700' : 'text-amber-200/80'
        }`}>
          <span>Опыт</span>
          <span>{user.xp} / {user.xp_to_next_level} XP</span>
        </div>
        <div className={`w-full h-3 rounded-full overflow-hidden border ${
          isLight
            ? 'bg-amber-100 border-amber-300'
            : 'bg-slate-950/50 border-amber-600/30'
        }`}>
          <div
            className="h-full bg-gradient-to-r from-amber-600 to-amber-400 transition-all duration-500 rounded-full"
            style={{ width: `${xpPercentage}%` }}
          />
        </div>
      </div>
      {/* Stats */}
      <div className="space-y-3">
        <div className={`flex items-center justify-between p-3 rounded-lg border ${
          isLight
            ? 'bg-amber-50 border-amber-200'
            : 'bg-amber-900/20 border-amber-600/30'
        }`}>
          <div className="flex items-center gap-2">
            <Sparkles className={`w-4 h-4 ${isLight ? 'text-amber-600' : 'text-amber-400'}`} />
            <span className={`text-sm ${isLight ? 'text-amber-900' : 'text-amber-200'}`}>
              Заданий сегодня
            </span>
          </div>
          <span className={isLight ? 'text-amber-900' : 'text-amber-100'}>
            {questsCompletedToday}
          </span>
        </div>
        <div className={`flex items-center justify-between p-3 rounded-lg border ${
          isLight
            ? 'bg-purple-50 border-purple-200'
            : 'bg-purple-900/20 border-purple-600/30'
        }`}>
          <div className="flex items-center gap-2">
            <Trophy className={`w-4 h-4 ${isLight ? 'text-purple-600' : 'text-purple-400'}`} />
            <span className={`text-sm ${isLight ? 'text-purple-900' : 'text-purple-200'}`}>
              Всего заданий
            </span>
          </div>
          <span className={isLight ? 'text-purple-900' : 'text-purple-100'}>
            {user.total_quests_completed}
          </span>
        </div>
      </div>
    </div>
  );
}