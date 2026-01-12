import { useAuthStore } from '../../stores/authStore';
import { Button } from '../ui';

interface HeaderProps {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
}

export function Header({ title, subtitle, actions }: HeaderProps) {
  const { logout } = useAuthStore();

  return (
    <header className="bg-ctp-mantle border-b border-ctp-surface0 px-8 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-ctp-text">{title}</h1>
          {subtitle && (
            <p className="text-sm text-ctp-subtext0 mt-1">{subtitle}</p>
          )}
        </div>
        <div className="flex items-center gap-4">
          {actions}
          <Button variant="ghost" onClick={logout}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                clipRule="evenodd"
              />
            </svg>
            Sair
          </Button>
        </div>
      </div>
    </header>
  );
}
