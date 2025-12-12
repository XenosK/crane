"use client";

import { ProCard } from "@ant-design/pro-components";

export default function ApplicationCreate() {
  return (
    <ProCard
      title="创建应用"
      headerBordered
      style={{
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ lineHeight: "1.8", color: "#595959" }}>
        <p style={{ marginBottom: "16px", fontSize: "15px" }}>
          创建新的指标应用，配置应用基本信息、关联指标等。
        </p>
        <p style={{ fontSize: "15px" }}>
          填写应用名称、描述、关联的指标等信息，即可创建新的指标应用。
        </p>
      </div>
    </ProCard>
  );
}

