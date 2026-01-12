import { useQuery } from '@tanstack/react-query';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { Layout } from '../../components/layout';
import { Card, Spinner, Table } from '../../components/ui';
import { statsApi } from '../../api';
import type { User } from '../../types';

function StatCard({
  title,
  value,
  color,
}: {
  title: string;
  value: number;
  color: string;
}) {
  return (
    <div className="bg-ctp-surface0 rounded-xl border border-ctp-surface1 p-6">
      <p className="text-sm text-ctp-subtext0">{title}</p>
      <p className={`text-3xl font-bold mt-2 ${color}`}>{value}</p>
    </div>
  );
}

export function DashboardPage() {
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['stats'],
    queryFn: statsApi.get,
  });

  const recentUsersColumns = [
    { key: 'name', header: 'Nome' },
    { key: 'email', header: 'Email' },
    {
      key: 'created_at',
      header: 'Criado em',
      render: (user: User) =>
        new Date(user.created_at).toLocaleDateString('pt-BR'),
    },
  ];

  if (isLoading) {
    return (
      <Layout title="Dashboard">
        <div className="flex items-center justify-center h-64">
          <Spinner size="lg" />
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout title="Dashboard">
        <div className="text-center text-ctp-red">
          Erro ao carregar estatisticas
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Dashboard" subtitle="Visao geral do sistema">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total de Usuarios"
          value={stats?.total_users || 0}
          color="text-ctp-blue"
        />
        <StatCard
          title="Novos Hoje"
          value={stats?.users_today || 0}
          color="text-ctp-green"
        />
        <StatCard
          title="Esta Semana"
          value={stats?.users_this_week || 0}
          color="text-ctp-peach"
        />
        <StatCard
          title="Este Mes"
          value={stats?.users_this_month || 0}
          color="text-ctp-mauve"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Growth Chart */}
        <Card title="Crescimento de Usuarios" subtitle="Ultimos 30 dias">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.growth_data || []}>
                <defs>
                  <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#89b4fa" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#89b4fa" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#45475a" />
                <XAxis
                  dataKey="date"
                  stroke="#a6adc8"
                  fontSize={12}
                  tickFormatter={(value) =>
                    new Date(value).toLocaleDateString('pt-BR', {
                      day: '2-digit',
                      month: '2-digit',
                    })
                  }
                />
                <YAxis stroke="#a6adc8" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#313244',
                    border: '1px solid #45475a',
                    borderRadius: '8px',
                    color: '#cdd6f4',
                  }}
                  labelFormatter={(value) =>
                    new Date(value).toLocaleDateString('pt-BR')
                  }
                />
                <Area
                  type="monotone"
                  dataKey="count"
                  stroke="#89b4fa"
                  fillOpacity={1}
                  fill="url(#colorCount)"
                  name="Usuarios"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Recent Users */}
        <Card title="Usuarios Recentes" subtitle="Ultimos cadastros">
          <Table
            data={stats?.recent_users || []}
            columns={recentUsersColumns}
            keyExtractor={(user) => user.id}
            emptyMessage="Nenhum usuario cadastrado"
          />
        </Card>
      </div>
    </Layout>
  );
}
