import { useNavigate, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Layout } from '../../components/layout';
import { Button, Card, Spinner } from '../../components/ui';
import { usersApi } from '../../api';
import { useAuthStore } from '../../stores/authStore';

export function UserDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user: currentUser } = useAuthStore();
  const isAdmin = currentUser?.role === 'admin';

  const { data: user, isLoading, error } = useQuery({
    queryKey: ['users', id],
    queryFn: () => usersApi.get(id!),
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <Layout title="Usuario">
        <div className="flex items-center justify-center h-64">
          <Spinner size="lg" />
        </div>
      </Layout>
    );
  }

  if (error || !user) {
    return (
      <Layout title="Usuario">
        <div className="text-center">
          <p className="text-ctp-red mb-4">Usuario nao encontrado</p>
          <Button variant="secondary" onClick={() => navigate('/users')}>
            Voltar para lista
          </Button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout
      title={user.name}
      subtitle={user.email}
      actions={
        isAdmin && (
          <Button variant="primary" onClick={() => navigate(`/users/${id}/edit`)}>
            Editar Usuario
          </Button>
        )
      }
    >
      <div className="max-w-2xl">
        <Card>
          <dl className="space-y-6">
            <div>
              <dt className="text-sm text-ctp-subtext0">Nome</dt>
              <dd className="text-lg text-ctp-text mt-1">{user.name}</dd>
            </div>
            <div>
              <dt className="text-sm text-ctp-subtext0">Email</dt>
              <dd className="text-lg text-ctp-text mt-1">{user.email}</dd>
            </div>
            <div>
              <dt className="text-sm text-ctp-subtext0">Perfil</dt>
              <dd className="mt-1">
                <span
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    user.role === 'admin'
                      ? 'bg-ctp-mauve/20 text-ctp-mauve'
                      : 'bg-ctp-blue/20 text-ctp-blue'
                  }`}
                >
                  {user.role === 'admin' ? 'Administrador' : 'Usuario'}
                </span>
              </dd>
            </div>
            <div>
              <dt className="text-sm text-ctp-subtext0">Data de Nascimento</dt>
              <dd className="text-lg text-ctp-text mt-1">
                {user.birth_date
                  ? new Date(user.birth_date + 'T00:00:00').toLocaleDateString('pt-BR', {
                      day: '2-digit',
                      month: 'long',
                      year: 'numeric',
                    })
                  : 'Nao informada'}
              </dd>
            </div>
            <div>
              <dt className="text-sm text-ctp-subtext0">Criado em</dt>
              <dd className="text-lg text-ctp-text mt-1">
                {new Date(user.created_at).toLocaleDateString('pt-BR', {
                  day: '2-digit',
                  month: 'long',
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </dd>
            </div>
            {user.updated_at && (
              <div>
                <dt className="text-sm text-ctp-subtext0">Atualizado em</dt>
                <dd className="text-lg text-ctp-text mt-1">
                  {new Date(user.updated_at).toLocaleDateString('pt-BR', {
                    day: '2-digit',
                    month: 'long',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </dd>
              </div>
            )}
          </dl>
        </Card>

        <div className="mt-6">
          <Button variant="ghost" onClick={() => navigate('/users')}>
            &larr; Voltar para lista
          </Button>
        </div>
      </div>
    </Layout>
  );
}
