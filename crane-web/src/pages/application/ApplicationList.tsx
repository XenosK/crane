"use client";

import { ProCard } from "@ant-design/pro-components";

export default function ApplicationList() {
  return (
    <ProCard
      title="应用列表"
      headerBordered
      style={{
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ lineHeight: "1.8", color: "#595959" }}>
        <p style={{ marginBottom: "16px", fontSize: "15px" }}>
          查看和管理所有指标应用，包括应用状态、创建时间、负责人等信息。
        </p>
        <p style={{ fontSize: "15px" }}>
          您可以在这里查看所有已创建的指标应用，并进行编辑、删除等操作。
        </p>
      </div>
    </ProCard>
  );
}

