"use client";

import { useState } from "react";
import { ProCard } from "@ant-design/pro-components";
import { Row, Col, Card, Typography } from "antd";
import {
  DatabaseOutlined,
  CloudServerOutlined,
  ThunderboltOutlined,
  HddOutlined,
} from "@ant-design/icons";
import DataSourceConfigModal from "./DataSourceConfigModal";

const { Title, Text } = Typography;

interface DataSourceType {
  key: string;
  name: string;
  icon: React.ReactNode;
  color: string;
  gradient: string;
}

const dataSourceTypes: DataSourceType[] = [
  {
    key: "presto",
    name: "Presto",
    icon: <ThunderboltOutlined style={{ fontSize: "48px" }} />,
    color: "#1890ff",
    gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
  },
  {
    key: "hive",
    name: "Hive",
    icon: <DatabaseOutlined style={{ fontSize: "48px" }} />,
    color: "#52c41a",
    gradient: "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
  },
  {
    key: "doris",
    name: "Doris",
    icon: <CloudServerOutlined style={{ fontSize: "48px" }} />,
    color: "#fa8c16",
    gradient: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
  },
  {
    key: "mysql",
    name: "MySQL",
    icon: <HddOutlined style={{ fontSize: "48px" }} />,
    color: "#722ed1",
    gradient: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
  },
];

export default function DataSourceList() {
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedDataSource, setSelectedDataSource] = useState<string | null>(null);

  const handleDataSourceClick = (type: string) => {
    setSelectedDataSource(type);
    setModalVisible(true);
  };

  const handleModalClose = () => {
    setModalVisible(false);
    setSelectedDataSource(null);
  };

  return (
    <div>
      <ProCard
        title="数据源管理"
        headerBordered
        style={{
          borderRadius: "12px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        }}
      >
        <div style={{ marginBottom: "24px" }}>
          <Text type="secondary" style={{ fontSize: "14px" }}>
            选择数据源类型进行配置，支持 Presto、Hive、Doris、MySQL 等多种数据源。
          </Text>
        </div>
        <Row gutter={[24, 24]}>
          {dataSourceTypes.map((source) => (
            <Col xs={24} sm={12} lg={6} key={source.key}>
              <Card
                hoverable
                onClick={() => handleDataSourceClick(source.key)}
                style={{
                  borderRadius: "12px",
                  cursor: "pointer",
                  transition: "all 0.3s ease",
                  border: "1px solid #f0f0f0",
                  height: "100%",
                }}
                styles={{
                  body: {
                    padding: "32px 24px",
                    textAlign: "center",
                    background: source.gradient,
                    borderRadius: "12px",
                  },
                }}
                className="datasource-card"
              >
                <div style={{ color: "#fff", marginBottom: "16px" }}>
                  {source.icon}
                </div>
                <Title
                  level={4}
                  style={{
                    color: "#fff",
                    margin: 0,
                    fontWeight: 600,
                    fontSize: "20px",
                  }}
                >
                  {source.name}
                </Title>
              </Card>
            </Col>
          ))}
        </Row>
      </ProCard>

      <DataSourceConfigModal
        visible={modalVisible}
        dataSourceType={selectedDataSource}
        onClose={handleModalClose}
      />
    </div>
  );
}

