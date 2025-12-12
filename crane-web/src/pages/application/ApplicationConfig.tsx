"use client";

import { ProCard } from "@ant-design/pro-components";

export default function ApplicationConfig() {
  return (
    <ProCard
      title="应用配置"
      headerBordered
      style={{
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ lineHeight: "1.8", color: "#595959" }}>
        <p style={{ marginBottom: "16px", fontSize: "15px" }}>
          配置指标应用的参数设置，包括数据源、计算规则、展示方式等。
        </p>
        <p style={{ fontSize: "15px" }}>
          您可以在这里配置应用的数据源连接、指标计算规则、数据展示格式等参数。
        </p>
      </div>
    </ProCard>
  );
}

