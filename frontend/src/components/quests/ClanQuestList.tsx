import { ClanQuest } from '../../types';
import { ClanQuestCard } from './ClanQuestCard';
import { Swords, CheckCircle2 } from 'lucide-react';
interface ClanQuestListProps {
  quests: ClanQuest[];
  onContribute: (id: number, contribution: number) => void;
  currentUsername: string;
}
export function ClanQuestList({ quests, onContribute, currentUsername }: ClanQuestListProps) {
  const activeQuests = quests.filter(q => !q.completed);
  const completedQuests = quests.filter(q => q.completed);
  return (
    <div className="space-y-6">
      {/* Active Clan Quests */}
      {activeQuests.length > 0 && (
        <div className="bg-slate-800/50 rounded-lg border-2 border-purple-600/30 p-6 backdrop-blur-sm">
          <h2 className="text-purple-300 mb-4 flex items-center gap-2">
            <Swords className="w-5 h-5" />
            Клановые задания ({activeQuests.length})
          </h2>
          <div className="space-y-4">
            {activeQuests.map((quest) => (
              <ClanQuestCard
                key={quest.id}
                quest={quest}
                onContribute={onContribute}
                currentUsername={currentUsername}
              />
            ))}
          </div>
        </div>
      )}
      {/* Completed Clan Quests */}
      {completedQuests.length > 0 && (
        <div className="bg-slate-800/30 rounded-lg border-2 border-emerald-600/20 p-6 backdrop-blur-sm">
          <h2 className="text-emerald-300 mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5" />
            Завершенные клановые задания ({completedQuests.length})
          </h2>
          <div className="space-y-4">
            {completedQuests.map((quest) => (
              <ClanQuestCard
                key={quest.id}
                quest={quest}
                onContribute={onContribute}
                currentUsername={currentUsername}
              />
            ))}
          </div>
        </div>
      )}
      {/* Empty State */}
      {quests.length === 0 && (
        <div className="bg-slate-800/30 rounded-lg border-2 border-purple-600/20 p-12 text-center backdrop-blur-sm">
          <Swords className="w-12 h-12 text-purple-400/40 mx-auto mb-4" />
          <p className="text-purple-200/60">Пока нет клановых заданий</p>
          <p className="text-purple-200/40 text-sm mt-2">Вступите в клан, чтобы участвовать в совместных заданиях</p>
        </div>
      )}
    </div>
  );
}