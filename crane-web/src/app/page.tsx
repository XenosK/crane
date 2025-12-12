"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";

export default function Home() {
  const router = useRouter();
  const { isAuthenticated, loading } = useAuth();

  useEffect(() => {
    if (!loading) {
      // 延迟一下，确保路由已经准备好
      const timer = setTimeout(() => {
        if (isAuthenticated) {
          // 已登录，重定向到仪表板
          router.push("/dashboard/metrics/overview");
        } else {
          // 未登录，重定向到登录页
          router.push("/login");
        }
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [isAuthenticated, loading, router]);

  // 加载中显示空白
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div>加载中...</div>
    </div>
  );
}
