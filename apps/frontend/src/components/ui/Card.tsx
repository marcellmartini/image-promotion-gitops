import type { ReactNode } from 'react';

interface CardProps {
  title?: string;
  subtitle?: string;
  children: ReactNode;
  className?: string;
  actions?: ReactNode;
}

export function Card({ title, subtitle, children, className = '', actions }: CardProps) {
  return (
    <div className={`bg-ctp-surface0 rounded-xl border border-ctp-surface1 ${className}`}>
      {(title || actions) && (
        <div className="flex items-center justify-between px-6 py-4 border-b border-ctp-surface1">
          <div>
            {title && (
              <h3 className="text-lg font-semibold text-ctp-text">{title}</h3>
            )}
            {subtitle && (
              <p className="text-sm text-ctp-subtext0 mt-0.5">{subtitle}</p>
            )}
          </div>
          {actions && (
            <div className="flex items-center gap-2">{actions}</div>
          )}
        </div>
      )}
      <div className="p-6">{children}</div>
    </div>
  );
}
