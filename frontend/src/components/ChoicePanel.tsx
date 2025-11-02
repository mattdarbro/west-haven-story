import { useState } from 'react';
import { Choice } from '../types/story';

interface ChoicePanelProps {
  choices: Choice[];
  onChoiceSelect: (choice: Choice) => void;
  disabled?: boolean;
  className?: string;
}

export function ChoicePanel({ 
  choices, 
  onChoiceSelect, 
  disabled = false,
  className = '' 
}: ChoicePanelProps) {
  const [hoveredChoice, setHoveredChoice] = useState<number | null>(null);

  if (choices.length === 0) {
    return null;
  }

  return (
    <div className={`space-y-3 ${className}`}>
      <div className="text-center mb-4">
        <h3 className="text-sm font-fantasy text-primary-300 mb-1">
          Choose Your Path
        </h3>
        <div className="w-16 h-px bg-gradient-to-r from-transparent via-primary-500 to-transparent mx-auto"></div>
      </div>
      
      <div className="space-y-3">
        {choices.map((choice, index) => (
          <div key={choice.id} className="relative">
            <button
              onClick={() => !disabled && onChoiceSelect(choice)}
              disabled={disabled}
              onMouseEnter={() => setHoveredChoice(choice.id)}
              onMouseLeave={() => setHoveredChoice(null)}
              className={`
                w-full p-4 text-left rounded-lg border transition-all duration-300
                ${disabled 
                  ? 'bg-dark-800/50 border-dark-600 text-dark-500 cursor-not-allowed' 
                  : 'bg-dark-800/80 border-primary-500/30 text-dark-100 hover:border-primary-400/50 hover:bg-dark-700/80 hover:shadow-lg hover:shadow-primary-500/10'
                }
                ${hoveredChoice === choice.id && !disabled 
                  ? 'transform scale-[1.02] shadow-lg shadow-primary-500/20' 
                  : ''
                }
                ${disabled ? '' : 'hover:animate-glow'}
              `}
            >
              <div className="flex items-start gap-3">
                {/* Choice number */}
                <div className={`
                  flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-semibold
                  ${disabled 
                    ? 'bg-dark-600 text-dark-400' 
                    : 'bg-primary-600 text-white'
                  }
                `}>
                  {index + 1}
                </div>
                
                {/* Choice text */}
                <div className="flex-1">
                  <p className="text-base font-medium leading-relaxed">
                    {choice.text}
                  </p>
                  
                  {/* Consequence hint */}
                  {choice.consequence_hint && (
                    <p className={`
                      text-sm mt-2 transition-opacity duration-200
                      ${hoveredChoice === choice.id && !disabled 
                        ? 'opacity-100 text-accent-300' 
                        : 'opacity-60 text-dark-400'
                      }
                    `}>
                      {choice.consequence_hint}
                    </p>
                  )}
                </div>
                
                {/* Arrow indicator */}
                {!disabled && (
                  <div className={`
                    flex-shrink-0 transition-transform duration-200
                    ${hoveredChoice === choice.id ? 'translate-x-1' : ''}
                  `}>
                    <svg 
                      className="w-4 h-4 text-primary-400" 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path 
                        strokeLinecap="round" 
                        strokeLinejoin="round" 
                        strokeWidth={2} 
                        d="M9 5l7 7-7 7" 
                      />
                    </svg>
                  </div>
                )}
              </div>
            </button>
          </div>
        ))}
      </div>
      
      {disabled && (
        <div className="text-center mt-4">
          <p className="text-sm text-dark-500">
            No credits remaining. Please start a new story.
          </p>
        </div>
      )}
    </div>
  );
}
