import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Layout } from '../../components/layout';
import { Button, Card, Table, Modal, Spinner } from '../../components/ui';
import { usersApi } from '../../api';
import { useAuthStore } from '../../stores/authStore';
import type { User } from '../../types';

export function UsersListPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { user: currentUser } = useAuthStore();
  const isAdmin = currentUser?.role === 'admin';

  const [deleteModal, setDeleteModal] = useState<{ open: boolean; user: User | null }>({
    open: false,
    user: null,
  });

  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: () => usersApi.list(),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => usersApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      setDeleteModal({ open: false, user: null });
    },
  });

  const columns = [
    { key: 'name', header: 'Nome' },
    { key: 'email', header: 'Email' },
    {
      key: 'role',
      header: 'Perfil',
      render: (user: User) => (
        <span
          className={`px-2 py-1 rounded-full text-xs font-medium ${
            user.role === 'admin'
              ? 'bg-ctp-mauve/20 text-ctp-mauve'
              : 'bg-ctp-blue/20 text-ctp-blue'
          }`}
        >
          {user.role === 'admin' ? 'Admin' : 'Usuario'}
        </span>
      ),
    },
    {
      key: 'birth_date',
      header: 'Data de Nascimento',
      render: (user: User) =>
        user.birth_date
          ? new Date(user.birth_date + 'T00:00:00').toLocaleDateString('pt-BR')
          : '-',
    },
    {
      key: 'created_at',
      header: 'Criado em',
      render: (user: User) =>
        new Date(user.created_at).toLocaleDateString('pt-BR'),
    },
    ...(isAdmin
      ? [
          {
            key: 'actions',
            header: '',
            className: 'text-right',
            render: (user: User) => (
              <div className="flex justify-end gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/users/${user.id}/edit`);
                  }}
                >
                  Editar
                </Button>
                <Button
                  variant="danger"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    setDeleteModal({ open: true, user });
                  }}
                >
                  Excluir
                </Button>
              </div>
            ),
          },
        ]
      : []),
  ];

  if (isLoading) {
    return (
      <Layout title="Usuarios">
        <div className="flex items-center justify-center h-64">
          <Spinner size="lg" />
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout title="Usuarios">
        <div className="text-center text-ctp-red">
          Erro ao carregar usuarios
        </div>
      </Layout>
    );
  }

  return (
    <Layout
      title="Usuarios"
      subtitle={`${data?.total || 0} usuarios cadastrados`}
      actions={
        isAdmin && (
          <Button variant="primary" onClick={() => navigate('/users/new')}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                clipRule="evenodd"
              />
            </svg>
            Novo Usuario
          </Button>
        )
      }
    >
      <Card>
        <Table
          data={data?.users || []}
          columns={columns}
          keyExtractor={(user) => user.id}
          onRowClick={(user) => navigate(`/users/${user.id}`)}
          emptyMessage="Nenhum usuario cadastrado"
        />
      </Card>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, user: null })}
        title="Confirmar exclusao"
        footer={
          <>
            <Button
              variant="ghost"
              onClick={() => setDeleteModal({ open: false, user: null })}
            >
              Cancelar
            </Button>
            <Button
              variant="danger"
              isLoading={deleteMutation.isPending}
              onClick={() => {
                if (deleteModal.user) {
                  deleteMutation.mutate(deleteModal.user.id);
                }
              }}
            >
              Excluir
            </Button>
          </>
        }
      >
        <p className="text-ctp-text">
          Tem certeza que deseja excluir o usuario{' '}
          <strong>{deleteModal.user?.name}</strong>?
        </p>
        <p className="text-ctp-subtext0 text-sm mt-2">
          Esta acao nao pode ser desfeita.
        </p>
      </Modal>
    </Layout>
  );
}
