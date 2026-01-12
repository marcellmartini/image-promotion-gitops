import { NavLink } from 'react-router-dom';
import { useAuthStore } from '../../stores/authStore';

interface NavItem {
  path: string;
  label: string;
  icon: React.ReactNode;
  adminOnly?: boolean;
}

const navItems: NavItem[] = [
  {
    path: '/',
    label: 'Dashboard',
    adminOnly: true,
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" />
      </svg>
    ),
  },
  {
    path: '/users',
    label: 'Usuarios',
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
      </svg>
    ),
  },
];

export function Sidebar() {
  const { user } = useAuthStore();
  const isAdmin = user?.role === 'admin';

  const filteredItems = navItems.filter(
    (item) => !item.adminOnly || isAdmin
  );

  return (
    <aside className="w-64 bg-ctp-mantle border-r border-ctp-surface0 min-h-screen flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-ctp-surface0">
        <h1 className="text-xl font-bold text-ctp-text flex items-center gap-2">
          <span className="text-ctp-blue">@</span>
          Admin
        </h1>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-1">
          {filteredItems.map((item) => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-2.5 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-ctp-surface0 text-ctp-blue'
                      : 'text-ctp-subtext1 hover:bg-ctp-surface0 hover:text-ctp-text'
                  }`
                }
              >
                {item.icon}
                {item.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* User info */}
      <div className="p-4 border-t border-ctp-surface0">
        <div className="flex items-center gap-3 px-2">
          <div className="w-10 h-10 rounded-full bg-ctp-surface1 flex items-center justify-center text-ctp-blue font-medium">
            {user?.name?.charAt(0).toUpperCase() || '?'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-ctp-text truncate">
              {user?.name}
            </p>
            <p className="text-xs text-ctp-subtext0 truncate">
              {user?.email}
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}
