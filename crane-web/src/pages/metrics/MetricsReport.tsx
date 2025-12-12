"use client";

import { ProCard } from "@ant-design/pro-components";

export default function MetricsReport() {
  return (
    <ProCard
      title="指标报表"
      headerBordered
      style={{
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ lineHeight: "1.8", color: "#595959" }}>
        <p style={{ marginBottom: "16px", fontSize: "15px" }}>
          生成和查看指标报表，支持自定义报表模板和导出功能。
        </p>
        <p style={{ fontSize: "15px" }}>
          您可以创建自定义报表，选择需要展示的指标和时间范围，并导出为 Excel 或 PDF 格式。
        </p>
      </div>
    </ProCard>
  );
}

