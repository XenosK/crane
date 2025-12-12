/**
 * 数据源 API 服务
 */
import { get, post, put, del, ApiResponse } from '@/utils/api';

export interface DataSource {
  id?: number;
  name: string;
  type: 'presto' | 'hive' | 'doris' | 'mysql';
  host: string;
  port: number;
  database?: string;
  catalog?: string;
  schema?: string;
  username?: string;
  password?: string;
  config?: Record<string, any>;
  status?: string;
  last_test_at?: string;
  created_at?: string;
  updated_at?: string;
}

export interface DataSourceListParams {
  page?: number;
  page_size?: number;
  type?: string;
}

export interface DataSourceListResponse {
  items: DataSource[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

/**
 * 获取数据源列表
 */
export async function getDataSourceList(
  params?: DataSourceListParams
): Promise<ApiResponse<DataSourceListResponse>> {
  return get<DataSourceListResponse>('/api/datasource/list', params);
}

/**
 * 获取数据源详情
 */
export async function getDataSource(id: number): Promise<ApiResponse<DataSource>> {
  return get<DataSource>(`/api/datasource/${id}`);
}

/**
 * 根据类型获取数据源列表
 */
export async function getDataSourceByType(type: string): Promise<ApiResponse<DataSource[]>> {
  return get<DataSource[]>(`/api/datasource/type/${type}`);
}

/**
 * 创建数据源
 */
export async function createDataSource(data: Omit<DataSource, 'id' | 'created_at' | 'updated_at' | 'last_test_at'>): Promise<ApiResponse<DataSource>> {
  return post<DataSource>('/api/datasource/create', data);
}

/**
 * 更新数据源
 */
export async function updateDataSource(
  id: number,
  data: Partial<DataSource>
): Promise<ApiResponse<DataSource>> {
  return put<DataSource>(`/api/datasource/${id}`, data);
}

/**
 * 删除数据源
 */
export async function deleteDataSource(id: number): Promise<ApiResponse<void>> {
  return del<void>(`/api/datasource/${id}`);
}

/**
 * 测试数据源连接
 */
export async function testDataSourceConnection(id: number): Promise<ApiResponse<{ success: boolean; message: string }>> {
  return post<{ success: boolean; message: string }>(`/api/datasource/${id}/test`);
}

