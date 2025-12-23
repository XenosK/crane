"use client";

import { useState, useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import AdminLayout from "@/components/AdminLayout";
import { useAuth } from "@/contexts/AuthContext";

// 指标平台页面
import MetricsOverview from "@/pages/metrics/MetricsOverview";
import MetricsDefinition from "@/pages/metrics/MetricsDefinition";
import MetricsMonitoring from "@/pages/metrics/MetricsMonitoring";
import MetricsReport from "@/pages/metrics/MetricsReport";

// 指标应用页面
import ApplicationList from "@/pages/application/ApplicationList";
import ApplicationCreate from "@/pages/application/ApplicationCreate";
import ApplicationConfig from "@/pages/application/ApplicationConfig";

// 语义建模页面
import SemanticModel from "@/pages/semantic/SemanticModel";

// 系统配置页面
import SystemUser from "@/pages/system/SystemUser";
import SystemRole from "@/pages/system/SystemRole";
import SystemPermission from "@/pages/system/SystemPermission";
import DataSourceList from "@/pages/system/datasource/DataSourceList";

export default function Dashboard() {
  const router = useRouter();
  const pathname = usePathname();
  const { isAuthenticated, loading } = useAuth();
  
  // 从路径中提取当前页面，避免初始状态闪烁
  const getCurrentPageFromPath = (path: string): string => {
    if (path === "/dashboard" || !path) {
      return "metrics/overview";
    }
    const pagePath = path.replace("/dashboard/", "").replace("/dashboard", "");
    return pagePath || "metrics/overview";
  };
  
  const [currentPage, setCurrentPage] = useState(() => getCurrentPageFromPath(pathname || ""));

  // 根据路径确定当前页面
  useEffect(() => {
    if (pathname) {
      if (pathname === "/dashboard") {
        // 访问 /dashboard 时重定向到默认页面
        router.replace("/dashboard/metrics/overview");
        setCurrentPage("metrics/overview");
      } else {
        // 从路径中提取页面标识
        const path = getCurrentPageFromPath(pathname);
        setCurrentPage(path);
      }
    }
  }, [pathname, router]);

  // 如果未登录，重定向到登录页
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      // 延迟一下，确保路由已经准备好
      const timer = setTimeout(() => {
        router.push("/login");
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [isAuthenticated, loading, router]);

  // 加载中显示空白或加载提示
  if (loading) {
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

  // 如果未登录，不渲染内容（等待重定向）
  if (!isAuthenticated) {
    return null;
  }

  const handleMenuChange = (menuKey: string) => {
    setCurrentPage(menuKey);
    router.push(`/dashboard/${menuKey}`);
  };

  const renderContent = () => {
    switch (currentPage) {
      // 指标平台
      case "metrics/overview":
        return <MetricsOverview />;
      case "metrics/definition":
        return <MetricsDefinition />;
      case "metrics/monitoring":
        return <MetricsMonitoring />;
      case "metrics/report":
        return <MetricsReport />;
      // 指标应用
      case "application/list":
        return <ApplicationList />;
      case "application/create":
        return <ApplicationCreate />;
      case "application/config":
        return <ApplicationConfig />;
      // 语义建模
      case "semantic/model":
        return <SemanticModel />;
      // 系统配置
      case "system/user":
        return <SystemUser />;
      case "system/role":
        return <SystemRole />;
      case "system/permission":
        return <SystemPermission />;
      case "system/datasource":
        return <DataSourceList />;
      default:
        return <MetricsOverview />;
    }
  };

  return (
    <AdminLayout onMenuChange={handleMenuChange} currentPage={currentPage}>
      {renderContent()}
    </AdminLayout>
  );
}

