import { useState } from 'react';
import { Sparkles, Target, Dumbbell, BookOpen, Heart, Briefcase, Home, Users } from 'lucide-react';
import { Button } from '../ui/Button';
import { FocusArea } from '../../types';
import { useCustomization } from '../../hooks/useCustomization';
interface FocusSelectorProps {
  currentFocus?: string;
  onSelectFocus: (focus: string) => void;
  loading?: boolean;
}
const FOCUS_AREAS: FocusArea[] = [
  {
    id: 'health',
    name: 'Здоровье',
    description: 'Физические упражнения, правильное питание, здоровые привычки',
    icon: 'heart',
  },
  {
    id: 'learning',
    name: 'Обучение',
    description: 'Изучение нового, чтение, развитие навыков',
    icon: 'book',
  },
  {
    id: 'work',
    name: 'Работа',
    description: 'Карьерные цели, проекты, продуктивность',
    icon: 'briefcase',
  },
  {
    id: 'personal',
    name: 'Личное развитие',
    description: 'Саморазвитие, медитация, хобби',
    icon: 'target',
  },
  {
    id: 'social',
    name: 'Социальная жизнь',
    description: 'Общение, встречи с друзьями, семья',
    icon: 'users',
  },
  {
    id: 'home',
    name: 'Домашние дела',
    description: 'Уборка, организация, благоустройство',
    icon: 'home',
  },
];
const ICON_MAP = {
  heart: Heart,
  book: BookOpen,
  briefcase: Briefcase,
  target: Target,
  users: Users,
  home: Home,
  dumbbell: Dumbbell,
};
export function FocusSelector({ currentFocus, onSelectFocus, loading }: FocusSelectorProps) {
  const [selectedFocus, setSelectedFocus] = useState<string>(currentFocus || '');
  const { settings } = useCustomization();
  const isLight = settings.theme === 'light';
  const handleGenerate = () => {
    if (selectedFocus) {
      onSelectFocus(selectedFocus);
    }
  };
  return (
    <div className={`rounded-lg border-2 p-6 shadow-xl backdrop-blur-sm ${
      isLight
        ? 'bg-white/90 border-purple-300'
        : 'bg-gradient-to-br from-slate-800/90 to-slate-900/90 border-purple-600/50'
    }`}>
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className={`w-5 h-5 ${isLight ? 'text-purple-600' : 'text-purple-400'}`} />
        <h2 className={isLight ? 'text-purple-800' : 'text-purple-300'}>
          Выберите направление развития
        </h2>
      </div>
      
      <p className={`text-sm mb-6 ${isLight ? 'text-purple-600' : 'text-purple-200/60'}`}>
        Приложение сгенерирует персональные задания на основе выбранного фокуса
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
        {FOCUS_AREAS.map((area) => {
          const IconComponent = ICON_MAP[area.icon as keyof typeof ICON_MAP] || Target;
          const isSelected = selectedFocus === area.id;
          
          return (
            <button
              key={area.id}
              onClick={() => setSelectedFocus(area.id)}
              className={`p-4 rounded-lg border-2 transition-all text-left ${
                isSelected
                  ? isLight
                    ? 'bg-purple-100 border-purple-500 shadow-lg'
                    : 'bg-purple-900/40 border-purple-500 shadow-lg shadow-purple-500/20'
                  : isLight
                  ? 'bg-white border-purple-200 hover:border-purple-400'
                  : 'bg-slate-950/30 border-purple-600/30 hover:border-purple-500/50'
              }`}
            >
              <div className="flex items-start gap-3">
                <IconComponent className={`w-5 h-5 flex-shrink-0 mt-0.5 ${
                  isSelected 
                    ? isLight ? 'text-purple-700' : 'text-purple-300'
                    : isLight ? 'text-purple-400' : 'text-purple-400/60'
                }`} />
                <div>
                  <h3 className={`mb-1 ${
                    isSelected 
                      ? isLight ? 'text-purple-900' : 'text-purple-200'
                      : isLight ? 'text-purple-700' : 'text-purple-300/80'
                  }`}>
                    {area.name}
                  </h3>
                  <p className={`text-xs ${
                    isSelected 
                      ? isLight ? 'text-purple-600' : 'text-purple-200/70'
                      : isLight ? 'text-purple-500' : 'text-purple-300/50'
                  }`}>
                    {area.description}
                  </p>
                </div>
              </div>
            </button>
          );
        })}
      </div>
      <Button
        onClick={handleGenerate}
        disabled={!selectedFocus || loading}
        className="w-full"
      >
        {loading ? 'Генерация заданий...' : 'Сгенерировать задания'}
      </Button>
      {currentFocus && (
        <p className={`text-center text-sm mt-3 ${
          isLight ? 'text-purple-500' : 'text-purple-200/40'
        }`}>
          Текущий фокус: {FOCUS_AREAS.find(a => a.id === currentFocus)?.name}
        </p>
      )}
    </div>
  );
}