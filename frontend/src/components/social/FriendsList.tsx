import { Friend } from '../../types';
import { Users, Circle } from 'lucide-react';
interface FriendsListProps {
  friends: Friend[];
}
export function FriendsList({ friends }: FriendsListProps) {
  const onlineFriends = friends.filter(f => f.is_online);
  const topFriends = [...friends].sort((a, b) => b.quests_completed_today - a.quests_completed_today).slice(0, 5);
  return (
    <div className="bg-gradient-to-br from-slate-800/90 to-slate-900/90 rounded-lg border-2 border-emerald-600/50 p-6 shadow-2xl backdrop-blur-sm">
      <div className="flex items-center gap-2 mb-4">
        <Users className="w-5 h-5 text-emerald-400" />
        <h2 className="text-emerald-300">Друзья</h2>
      </div>
      {/* Online Status */}
      <div className="mb-4 p-3 bg-emerald-900/20 rounded-lg border border-emerald-600/30">
        <p className="text-emerald-200/80 text-sm">
          Онлайн: <span className="text-emerald-300">{onlineFriends.length}</span> из {friends.length}
        </p>
      </div>
      {/* Top Friends Today */}
      <div className="space-y-2">
        <p className="text-emerald-200/60 text-sm mb-3">Активные сегодня:</p>
        {topFriends.map((friend) => (
          <div
            key={friend.id}
            className="flex items-center justify-between p-3 bg-slate-950/40 rounded-lg border border-emerald-600/20 hover:border-emerald-600/40 transition-colors"
          >
            <div className="flex items-center gap-2">
              <Circle
                className={`w-2 h-2 ${
                  friend.is_online ? 'fill-green-400 text-green-400' : 'fill-gray-500 text-gray-500'
                }`}
              />
              <div>
                <p className="text-emerald-200 text-sm">{friend.username}</p>
                <p className="text-emerald-200/40 text-xs">Уровень {friend.level}</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-emerald-300 text-sm">{friend.quests_completed_today}</p>
              <p className="text-emerald-200/40 text-xs">заданий</p>
            </div>
          </div>
        ))}
      </div>
      {friends.length === 0 && (
        <div className="text-center py-8">
          <p className="text-emerald-200/40 text-sm">Пока нет друзей</p>
        </div>
      )}
    </div>
  );
}