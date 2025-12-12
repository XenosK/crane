"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { User, login as loginApi, getCurrentUser, logout as logoutApi } from "@/services/auth";
import { message } from "antd";

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // 从 localStorage 恢复登录状态
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem("token");
      const storedUser = localStorage.getItem("user");

      if (storedToken && storedUser) {
        // 先设置 token 和 user，避免闪烁
        setToken(storedToken);
        try {
          const parsedUser = JSON.parse(storedUser);
          setUser(parsedUser);
        } catch (e) {
          // 如果解析失败，清除存储
          clearAuth();
          return;
        }
        
        // 验证 token 是否有效
        await validateToken(storedToken);
      } else {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const validateToken = async (tokenToValidate: string) => {
    try {
      // 验证 token 是否有效
      const response = await getCurrentUser();
      if (response.code === 200 && response.data) {
        // 更新用户信息（可能已更新）
        setUser(response.data);
        // 更新 localStorage 中的用户信息
        localStorage.setItem("user", JSON.stringify(response.data));
        setLoading(false);
      } else {
        // Token 无效，清除登录状态
        clearAuth();
      }
    } catch (error: any) {
      // 如果是 401 错误，api.ts 已经处理了清除和重定向
      // 这里只需要清除本地状态
      if (error.message && error.message.includes('登录已过期')) {
        clearAuth();
      } else {
        // 其他错误，也清除登录状态
        clearAuth();
      }
    }
  };

  const clearAuth = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setLoading(false);
  };

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      const response = await loginApi({ username, password });
      if (response.code === 200 && response.data) {
        setToken(response.data.token);
        setUser(response.data.user);
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("user", JSON.stringify(response.data.user));
        message.success("登录成功");
        return true;
      } else {
        message.error(response.message || "登录失败");
        return false;
      }
    } catch (error: any) {
      message.error(error.message || "登录失败，请检查网络连接");
      return false;
    }
  };

  const logout = async () => {
    try {
      await logoutApi();
    } catch (error) {
      // 即使 API 调用失败，也清除本地状态
    } finally {
      clearAuth();
      message.success("已退出登录");
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        logout,
        isAuthenticated: !!user && !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

