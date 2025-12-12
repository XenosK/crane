"use client";

import { ProCard } from "@ant-design/pro-components";

export default function SystemPermission() {
  return (
    <ProCard
      title="权限管理"
      headerBordered
      style={{
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ lineHeight: "1.8", color: "#595959" }}>
        <p style={{ marginBottom: "16px", fontSize: "15px" }}>
          配置系统权限，管理功能权限和数据权限的分配。
        </p>
        <p style={{ fontSize: "15px" }}>
          您可以在这里配置系统的所有权限点，包括菜单权限、操作权限和数据权限等。
        </p>
      </div>
    </ProCard>
  );
}

