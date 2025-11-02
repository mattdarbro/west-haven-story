import React from 'react';

interface ErrorStateProps {
  error: string;
  onRetry?: () => void;
  onReset?: () => void;
}

export function ErrorState({ error, onRetry, onReset }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] p-8">
      {/* Error icon */}
      <div className="mb-6">
        <div className="w-16 h-16 rounded-full bg-red-900/20 border-2 border-red-500/30 flex items-center justify-center">
          <svg 
            className="w-8 h-8 text-red-400" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" 
            />
          </svg>
        </div>
      </div>
      
      {/* Error message */}
      <div className="text-center mb-6">
        <h3 className="text-lg font-fantasy text-red-300 mb-2">
          The Story Stumbles
        </h3>
        <p className="text-sm text-dark-400 mb-4 max-w-md">
          {error}
        </p>
      </div>
      
      {/* Action buttons */}
      <div className="flex gap-3">
        {onRetry && (
          <button
            onClick={onRetry}
            className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors duration-200 font-medium"
          >
            Try Again
          </button>
        )}
        {onReset && (
          <button
            onClick={onReset}
            className="px-4 py-2 bg-dark-700 hover:bg-dark-600 text-dark-200 rounded-lg transition-colors duration-200 font-medium"
          >
            Start Over
          </button>
        )}
      </div>
    </div>
  );
}
