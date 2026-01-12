import { forwardRef } from 'react';
import type { InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = '', id, ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s/g, '-');

    return (
      <div className="w-full">
        {label && (
          <label htmlFor={inputId} className="block text-sm font-medium text-ctp-subtext1 mb-1">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={`
            w-full px-4 py-2 rounded-lg border
            bg-ctp-surface0 text-ctp-text placeholder-ctp-overlay0
            focus:outline-none focus:ring-2 focus:border-transparent
            transition-all duration-200
            ${error
              ? 'border-ctp-red focus:ring-ctp-red'
              : 'border-ctp-surface2 focus:ring-ctp-blue'
            }
            ${className}
          `}
          {...props}
        />
        {error && (
          <p className="mt-1 text-sm text-ctp-red">{error}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
