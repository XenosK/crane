"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import AdminLayout from "@/components/AdminLayout";
import Login from "@/pages/auth/Login";
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

// 系统配置页面
import SystemUser from "@/pages/system/SystemUser";
import SystemRole from "@/pages/system/SystemRole";
import SystemPermission from "@/pages/system/SystemPermission";
import DataSourceList from "@/pages/system/datasource/DataSourceList";

export default function Home() {
  const [currentPage, setCurrentPage] = useState("metrics/overview");
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  // 如果未登录，显示登录页面
  if (!loading && !isAuthenticated) {
    return <Login />;
  }

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
    <AdminLayout onMenuChange={setCurrentPage} currentPage={currentPage}>
      {renderContent()}
    </AdminLayout>
  );
}
