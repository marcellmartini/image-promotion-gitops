import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Layout } from '../../components/layout';
import { Button, Card, Input, Spinner } from '../../components/ui';
import { usersApi } from '../../api';
import type { UserRole } from '../../types';

export function UserFormPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEditing = !!id;

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    role: 'user' as UserRole,
    birth_date: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const { data: user, isLoading: isLoadingUser } = useQuery({
    queryKey: ['users', id],
    queryFn: () => usersApi.get(id!),
    enabled: isEditing,
  });

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name,
        email: user.email,
        password: '',
        role: user.role,
        birth_date: user.birth_date || '',
      });
    }
  }, [user]);

  const createMutation = useMutation({
    mutationFn: usersApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      navigate('/users');
    },
    onError: (error: { response?: { data?: { detail?: string } } }) => {
      const message = error?.response?.data?.detail || 'Erro ao criar usuario';
      setErrors({ submit: message });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: { name?: string; email?: string; birth_date?: string | null } }) =>
      usersApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      navigate('/users');
    },
    onError: (error: { response?: { data?: { detail?: string } } }) => {
      const message = error?.response?.data?.detail || 'Erro ao atualizar usuario';
      setErrors({ submit: message });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});

    // Basic validation
    const newErrors: Record<string, string> = {};
    if (!formData.name.trim()) newErrors.name = 'Nome e obrigatorio';
    if (!formData.email.trim()) newErrors.email = 'Email e obrigatorio';
    if (!isEditing && !formData.password) newErrors.password = 'Senha e obrigatoria';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    if (isEditing) {
      updateMutation.mutate({
        id: id!,
        data: {
          name: formData.name,
          email: formData.email,
          birth_date: formData.birth_date || null,
        },
      });
    } else {
      createMutation.mutate({
        name: formData.name,
        email: formData.email,
        password: formData.password,
        role: formData.role,
        birth_date: formData.birth_date || null,
      });
    }
  };

  const isSubmitting = createMutation.isPending || updateMutation.isPending;

  if (isEditing && isLoadingUser) {
    return (
      <Layout title="Carregando...">
        <div className="flex items-center justify-center h-64">
          <Spinner size="lg" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout
      title={isEditing ? 'Editar Usuario' : 'Novo Usuario'}
      subtitle={isEditing ? user?.email : 'Preencha os dados do novo usuario'}
    >
      <div className="max-w-lg">
        <Card>
          <form onSubmit={handleSubmit} className="space-y-6">
            {errors.submit && (
              <div className="p-3 rounded-lg bg-ctp-red/10 border border-ctp-red/20 text-ctp-red text-sm">
                {errors.submit}
              </div>
            )}

            <Input
              label="Nome"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              error={errors.name}
              placeholder="Nome completo"
            />

            <Input
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              error={errors.email}
              placeholder="email@exemplo.com"
            />

            <Input
              label="Data de Nascimento"
              type="date"
              value={formData.birth_date}
              onChange={(e) => setFormData({ ...formData, birth_date: e.target.value })}
              error={errors.birth_date}
            />

            {!isEditing && (
              <>
                <Input
                  label="Senha"
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  error={errors.password}
                  placeholder="••••••••"
                />

                <div>
                  <label className="block text-sm font-medium text-ctp-subtext1 mb-1">
                    Perfil
                  </label>
                  <select
                    value={formData.role}
                    onChange={(e) =>
                      setFormData({ ...formData, role: e.target.value as UserRole })
                    }
                    className="w-full px-4 py-2 rounded-lg border border-ctp-surface2
                      bg-ctp-surface0 text-ctp-text
                      focus:outline-none focus:ring-2 focus:ring-ctp-blue focus:border-transparent"
                  >
                    <option value="user">Usuario</option>
                    <option value="admin">Administrador</option>
                  </select>
                </div>
              </>
            )}

            <div className="flex gap-3 pt-4">
              <Button
                type="button"
                variant="ghost"
                onClick={() => navigate('/users')}
              >
                Cancelar
              </Button>
              <Button type="submit" variant="primary" isLoading={isSubmitting}>
                {isEditing ? 'Salvar Alteracoes' : 'Criar Usuario'}
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </Layout>
  );
}
