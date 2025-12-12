"use client";

import { useState, useEffect } from "react";
import { Layout, Menu, MenuProps } from "antd";
import {
  DashboardOutlined,
  AppstoreOutlined,
  SettingOutlined,
  BarChartOutlined,
  MonitorOutlined,
  DatabaseOutlined,
  FileTextOutlined,
  UserOutlined,
  TeamOutlined,
  SafetyOutlined,
  CloudServerOutlined,
} from "@ant-design/icons";
import type { MenuItemType } from "antd/es/menu/hooks/useItems";

const { Header, Sider, Content } = Layout;

interface MenuItem {
  key: string;
  label: string;
  icon: React.ReactNode;
  children?: MenuItem[];
}

const menuConfig: MenuItem[] = [
  {
    key: "metrics",
    label: "指标平台",
    icon: <DashboardOutlined />,
    children: [
      {
        key: "metrics/overview",
        label: "指标概览",
        icon: <BarChartOutlined />,
      },
      {
        key: "metrics/definition",
        label: "指标定义",
        icon: <DatabaseOutlined />,
      },
      {
        key: "metrics/monitoring",
        label: "指标监控",
        icon: <MonitorOutlined />,
      },
      {
        key: "metrics/report",
        label: "指标报表",
        icon: <FileTextOutlined />,
      },
    ],
  },
  {
    key: "application",
    label: "指标应用",
    icon: <AppstoreOutlined />,
    children: [
      {
        key: "application/list",
        label: "应用列表",
        icon: <AppstoreOutlined />,
      },
      {
        key: "application/create",
        label: "创建应用",
        icon: <AppstoreOutlined />,
      },
      {
        key: "application/config",
        label: "应用配置",
        icon: <SettingOutlined />,
      },
    ],
  },
  {
    key: "system",
    label: "系统配置",
    icon: <SettingOutlined />,
    children: [
      {
        key: "system/user",
        label: "用户管理",
        icon: <UserOutlined />,
      },
      {
        key: "system/role",
        label: "角色管理",
        icon: <TeamOutlined />,
      },
      {
        key: "system/permission",
        label: "权限管理",
        icon: <SafetyOutlined />,
      },
      {
        key: "system/datasource",
        label: "数据源",
        icon: <CloudServerOutlined />,
      },
    ],
  },
];

function convertToMenuItems(items: MenuItem[]): MenuItemType[] {
  return items.map((item) => ({
    key: item.key,
    icon: item.icon,
    label: item.label,
    children: item.children ? convertToMenuItems(item.children) : undefined,
  }));
}

interface AdminLayoutProps {
  children?: React.ReactNode;
  onMenuChange?: (menuKey: string) => void;
  currentPage?: string;
}

export default function AdminLayout({ children, onMenuChange, currentPage }: AdminLayoutProps) {
  const [selectedTopMenu, setSelectedTopMenu] = useState<string>("metrics");
  const [selectedSubMenu, setSelectedSubMenu] = useState<string>("metrics/overview");

  const topMenuItems: MenuItemType[] = menuConfig.map((item) => ({
    key: item.key,
    icon: item.icon,
    label: item.label,
  }));

  const currentSubMenuItems = menuConfig.find(
    (item) => item.key === selectedTopMenu
  )?.children || [];

  const handleTopMenuClick: MenuProps["onClick"] = (e) => {
    const key = e.key as string;
    setSelectedTopMenu(key);
    // 自动选择该一级菜单下的第一个二级菜单
    const firstSubMenu = menuConfig
      .find((item) => item.key === key)
      ?.children?.[0]?.key;
    if (firstSubMenu) {
      setSelectedSubMenu(firstSubMenu);
      onMenuChange?.(firstSubMenu);
    }
  };

  const handleSubMenuClick: MenuProps["onClick"] = (e) => {
    const key = e.key as string;
    setSelectedSubMenu(key);
    onMenuChange?.(key);
  };

  // 同步外部传入的 currentPage
  useEffect(() => {
    if (currentPage) {
      const topMenu = menuConfig.find((item) =>
        item.children?.some((child) => child.key === currentPage)
      );
      if (topMenu) {
        setSelectedTopMenu(topMenu.key);
        setSelectedSubMenu(currentPage);
      }
    }
  }, [currentPage]);

  return (
    <Layout style={{ minHeight: "100vh", background: "#f0f2f5" }}>
      <Header
        style={{
          display: "flex",
          alignItems: "center",
          background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
          padding: "0 32px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
          position: "sticky",
          top: 0,
          zIndex: 100,
        }}
      >
        <div
          style={{
            color: "#fff",
            fontSize: "22px",
            fontWeight: 600,
            marginRight: "64px",
            display: "flex",
            alignItems: "center",
            letterSpacing: "0.5px",
          }}
        >
          <div
            style={{
              width: "32px",
              height: "32px",
              background: "rgba(255,255,255,0.2)",
              borderRadius: "8px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              marginRight: "12px",
              backdropFilter: "blur(10px)",
            }}
          >
            <DashboardOutlined style={{ fontSize: "18px", color: "#fff" }} />
          </div>
          Crane 管理系统
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[selectedTopMenu]}
          items={topMenuItems}
          onClick={handleTopMenuClick}
          style={{
            flex: 1,
            minWidth: 0,
            background: "transparent",
            borderBottom: "none",
            fontSize: "15px",
          }}
        />
      </Header>
      <Layout>
        <Sider
          width={240}
          style={{
            background: "#fff",
            boxShadow: "2px 0 8px rgba(0,0,0,0.06)",
            position: "sticky",
            top: 64,
            height: "calc(100vh - 64px)",
            overflow: "auto",
          }}
        >
          <div
            style={{
              padding: "24px",
              borderBottom: "1px solid #f0f0f0",
              background: "linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%)",
            }}
          >
            <div
              style={{
                fontSize: "13px",
                color: "#667eea",
                fontWeight: 600,
                textTransform: "uppercase",
                letterSpacing: "1.5px",
                display: "flex",
                alignItems: "center",
              }}
            >
              <div
                style={{
                  width: "4px",
                  height: "16px",
                  background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                  borderRadius: "2px",
                  marginRight: "12px",
                }}
              />
              {menuConfig.find((item) => item.key === selectedTopMenu)?.label}
            </div>
          </div>
          <Menu
            mode="inline"
            selectedKeys={[selectedSubMenu]}
            items={convertToMenuItems(currentSubMenuItems)}
            onClick={handleSubMenuClick}
            style={{
              height: "100%",
              borderRight: 0,
              padding: "12px 0",
            }}
            className="custom-sidebar-menu"
          />
        </Sider>
        <Layout style={{ padding: "24px", background: "#f0f2f5" }}>
          <Content
            style={{
              background: "#fff",
              padding: "32px",
              minHeight: 280,
              borderRadius: "12px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
            }}
          >
            {children}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
}

