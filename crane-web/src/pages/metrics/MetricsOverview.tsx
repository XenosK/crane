"use client";

import { ProCard } from "@ant-design/pro-components";
import { Statistic, Row, Col } from "antd";
import { BarChartOutlined, MonitorOutlined } from "@ant-design/icons";

export default function MetricsOverview() {
  return (
    <div>
      <ProCard
        title="指标概览"
        headerBordered
        style={{
          borderRadius: "12px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        }}
      >
        <Row gutter={[24, 24]}>
          <Col xs={24} sm={12} lg={6}>
            <ProCard
              bordered
              style={{
                borderRadius: "8px",
                background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                color: "#fff",
              }}
            >
              <Statistic
                title={<span style={{ color: "rgba(255,255,255,0.9)" }}>指标总数</span>}
                value={1234}
                styles={{ content: { color: "#fff", fontSize: "28px", fontWeight: 600 } }}
                prefix={<BarChartOutlined style={{ fontSize: "24px", opacity: 0.8 }} />}
              />
            </ProCard>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <ProCard
              bordered
              style={{
                borderRadius: "8px",
                background: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                color: "#fff",
              }}
            >
              <Statistic
                title={<span style={{ color: "rgba(255,255,255,0.9)" }}>活跃指标</span>}
                value={856}
                styles={{ content: { color: "#fff", fontSize: "28px", fontWeight: 600 } }}
                prefix={<BarChartOutlined style={{ fontSize: "24px", opacity: 0.8 }} />}
              />
            </ProCard>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <ProCard
              bordered
              style={{
                borderRadius: "8px",
                background: "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
                color: "#fff",
              }}
            >
              <Statistic
                title={<span style={{ color: "rgba(255,255,255,0.9)" }}>异常指标</span>}
                value={23}
                styles={{ content: { color: "#fff", fontSize: "28px", fontWeight: 600 } }}
                prefix={<MonitorOutlined style={{ fontSize: "24px", opacity: 0.8 }} />}
              />
            </ProCard>
          </Col>
          <Col xs={24} sm={12} lg={6}>
            <ProCard
              bordered
              style={{
                borderRadius: "8px",
                background: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
                color: "#fff",
              }}
            >
              <Statistic
                title={<span style={{ color: "rgba(255,255,255,0.9)" }}>今日新增</span>}
                value={12}
                styles={{ content: { color: "#fff", fontSize: "28px", fontWeight: 600 } }}
                prefix={<BarChartOutlined style={{ fontSize: "24px", opacity: 0.8 }} />}
              />
            </ProCard>
          </Col>
        </Row>
      </ProCard>
    </div>
  );
}

