export type UserRole = 'admin' | 'user';

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  created_at: string;
  updated_at: string | null;
}

export interface UserCreate {
  name: string;
  email: string;
  password: string;
  role?: UserRole;
}

export interface UserUpdate {
  name?: string;
  email?: string;
}

export interface UserListResponse {
  users: User[];
  total: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

export interface Stats {
  total_users: number;
  users_today: number;
  users_this_week: number;
  users_this_month: number;
  recent_users: User[];
  growth_data: { date: string; count: number }[];
}

export interface ApiError {
  detail: string;
}
