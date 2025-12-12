/**
 * API 配置和请求工具
 */

// API 基础 URL，可以通过环境变量配置
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000';

export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data?: T;
}

/**
 * 通用 API 请求函数
 */
async function request<T = any>(
  url: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const fullUrl = `${API_BASE_URL}${url}`;
  
  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json',
  };

  // 从 localStorage 获取 token
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(fullUrl, config);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || `HTTP error! status: ${response.status}`);
    }
    
    return data;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('网络请求失败');
  }
}

/**
 * GET 请求
 */
export async function get<T = any>(url: string, params?: Record<string, any>): Promise<ApiResponse<T>> {
  let fullUrl = url;
  if (params) {
    const searchParams = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== null) {
        searchParams.append(key, String(params[key]));
      }
    });
    const queryString = searchParams.toString();
    if (queryString) {
      fullUrl += `?${queryString}`;
    }
  }
  return request<T>(fullUrl, { method: 'GET' });
}

/**
 * POST 请求
 */
export async function post<T = any>(url: string, data?: any): Promise<ApiResponse<T>> {
  return request<T>(url, {
    method: 'POST',
    body: data ? JSON.stringify(data) : undefined,
  });
}

/**
 * PUT 请求
 */
export async function put<T = any>(url: string, data?: any): Promise<ApiResponse<T>> {
  return request<T>(url, {
    method: 'PUT',
    body: data ? JSON.stringify(data) : undefined,
  });
}

/**
 * DELETE 请求
 */
export async function del<T = any>(url: string): Promise<ApiResponse<T>> {
  return request<T>(url, { method: 'DELETE' });
}

export default {
  get,
  post,
  put,
  delete: del,
};

