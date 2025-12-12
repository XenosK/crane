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
    const storedToken = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      // 验证 token 是否有效
      validateToken(storedToken);
    } else {
      setLoading(false);
    }
  }, []);

  const validateToken = async (tokenToValidate: string) => {
    try {
      // 设置 token 到请求头（需要在 api.ts 中处理）
      const response = await getCurrentUser();
      if (response.code === 200 && response.data) {
        setUser(response.data);
        setLoading(false);
      } else {
        // Token 无效，清除登录状态
        clearAuth();
      }
    } catch (error) {
      // Token 无效，清除登录状态
      clearAuth();
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

