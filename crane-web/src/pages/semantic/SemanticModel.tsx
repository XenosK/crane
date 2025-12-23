"use client";

import { ProCard } from "@ant-design/pro-components";

export default function SemanticModel() {
  return (
    <ProCard
      title="语义模型"
      headerBordered
      style={{
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ lineHeight: "1.8", color: "#595959" }}>
        <p style={{ marginBottom: "16px", fontSize: "15px" }}>
          语义建模功能正在开发中...
        </p>
        <p style={{ fontSize: "15px" }}>
          您可以在这里管理和配置语义模型，包括实体、关系、属性等语义元素的定义和管理。
        </p>
      </div>
    </ProCard>
  );
}

