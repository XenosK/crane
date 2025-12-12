/**
 * 认证 API 服务
 */
import { post, get, ApiResponse } from '@/utils/api';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: {
    id: number;
    username: string;
    email?: string;
    real_name?: string;
    phone?: string;
    status: string;
    roles?: any[];
  };
}

export interface User {
  id: number;
  username: string;
  email?: string;
  real_name?: string;
  phone?: string;
  status: string;
  roles?: any[];
}

/**
 * 用户登录
 */
export async function login(data: LoginRequest): Promise<ApiResponse<LoginResponse>> {
  return post<LoginResponse>('/api/auth/login', data);
}

/**
 * 获取当前用户信息
 */
export async function getCurrentUser(): Promise<ApiResponse<User>> {
  return get<User>('/api/auth/me');
}

/**
 * 用户登出
 */
export async function logout(): Promise<ApiResponse<void>> {
  return post<void>('/api/auth/logout');
}

