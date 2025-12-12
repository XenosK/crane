"use client";

import { ProCard } from "@ant-design/pro-components";

export default function MetricsDefinition() {
  return (
    <ProCard
      title="指标定义"
      headerBordered
      style={{
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ lineHeight: "1.8", color: "#595959" }}>
        <p style={{ marginBottom: "16px", fontSize: "15px" }}>
          管理和配置指标的定义，包括指标名称、类型、计算公式等。
        </p>
        <p style={{ fontSize: "15px" }}>
          您可以在这里创建、编辑和删除指标定义，设置指标的计算规则和展示方式。
        </p>
      </div>
    </ProCard>
  );
}

