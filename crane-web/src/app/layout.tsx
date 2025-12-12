import type { Metadata } from "next";
import { ConfigProvider } from "antd";
import zhCN from "antd/locale/zh_CN";
import "./globals.css";

export const metadata: Metadata = {
  title: "Crane 后台管理系统",
  description: "指标平台管理系统",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>
        <ConfigProvider
          locale={zhCN}
          theme={{
            token: {
              colorPrimary: "#667eea",
              borderRadius: 8,
              colorBgContainer: "#ffffff",
              colorBgElevated: "#ffffff",
            },
            components: {
              Menu: {
                itemSelectedBg: "rgba(102, 126, 234, 0.1)",
                itemHoverBg: "rgba(102, 126, 234, 0.06)",
                itemActiveBg: "rgba(102, 126, 234, 0.1)",
                subMenuItemBg: "transparent",
              },
              Card: {
                borderRadiusLG: 12,
                paddingLG: 24,
              },
            },
          }}
        >
          {children}
        </ConfigProvider>
      </body>
    </html>
  );
}
