"use client";

import { ProCard } from "@ant-design/pro-components";

export default function SystemRole() {
  return (
    <ProCard
      title="角色管理"
      headerBordered
      style={{
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ lineHeight: "1.8", color: "#595959" }}>
        <p style={{ marginBottom: "16px", fontSize: "15px" }}>
          管理系统角色，定义不同角色的权限范围，支持角色创建和编辑。
        </p>
        <p style={{ fontSize: "15px" }}>
          您可以创建不同的角色，并为每个角色分配相应的功能权限和数据权限。
        </p>
      </div>
    </ProCard>
  );
}

