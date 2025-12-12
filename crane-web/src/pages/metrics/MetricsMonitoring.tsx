"use client";

import { ProCard } from "@ant-design/pro-components";

export default function MetricsMonitoring() {
  return (
    <ProCard
      title="指标监控"
      headerBordered
      style={{
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ lineHeight: "1.8", color: "#595959" }}>
        <p style={{ marginBottom: "16px", fontSize: "15px" }}>
          实时监控指标的状态和变化，查看指标趋势图和告警信息。
        </p>
        <p style={{ fontSize: "15px" }}>
          系统会实时更新指标数据，并在指标异常时发送告警通知。
        </p>
      </div>
    </ProCard>
  );
}

