"use client";

import { ProCard } from "@ant-design/pro-components";

export default function SystemUser() {
  return (
    <ProCard
      title="用户管理"
      headerBordered
      style={{
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ lineHeight: "1.8", color: "#595959" }}>
        <p style={{ marginBottom: "16px", fontSize: "15px" }}>
          管理系统用户，包括用户创建、编辑、删除、权限分配等功能。
        </p>
        <p style={{ fontSize: "15px" }}>
          您可以在这里添加新用户、编辑用户信息、分配用户角色和权限。
        </p>
      </div>
    </ProCard>
  );
}

