"use client";

import { useState, useEffect } from "react";
import { ProCard } from "@ant-design/pro-components";
import { Row, Col, Card, Typography, Table, Tag, Button, Space, message, Popconfirm } from "antd";
import {
  DatabaseOutlined,
  CloudServerOutlined,
  ThunderboltOutlined,
  HddOutlined,
  ReloadOutlined,
  DeleteOutlined,
} from "@ant-design/icons";
import DataSourceConfigModal from "./DataSourceConfigModal";
import { getDataSourceList, deleteDataSource, DataSource } from "@/services/datasource";

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
  const [dataSourceList, setDataSourceList] = useState<DataSource[]>([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });

  // 加载数据源列表
  const loadDataSourceList = async (page = 1, pageSize = 10) => {
    setLoading(true);
    try {
      const response = await getDataSourceList({ page, page_size: pageSize });
      if (response.code === 200 && response.data) {
        setDataSourceList(response.data.items || []);
        setPagination({
          current: response.data.page,
          pageSize: response.data.page_size,
          total: response.data.total,
        });
      }
    } catch (error: any) {
      console.error("加载数据源列表失败:", error);
      message.error(error.message || "加载数据源列表失败");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDataSourceList();
  }, []);

  const handleDataSourceClick = (type: string) => {
    setSelectedDataSource(type);
    setModalVisible(true);
  };

  const handleModalClose = () => {
    setModalVisible(false);
    setSelectedDataSource(null);
  };

  const handleSaveSuccess = () => {
    // 保存成功后刷新列表
    loadDataSourceList(pagination.current, pagination.pageSize);
  };

  const handleDelete = async (id: number) => {
    try {
      const response = await deleteDataSource(id);
      if (response.code === 200) {
        message.success("删除成功");
        loadDataSourceList(pagination.current, pagination.pageSize);
      } else {
        message.error(response.message || "删除失败");
      }
    } catch (error: any) {
      console.error("删除数据源失败:", error);
      message.error(error.message || "删除失败");
    }
  };

  const handleTableChange = (newPagination: any) => {
    loadDataSourceList(newPagination.current, newPagination.pageSize);
  };

  // 表格列定义
  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      width: 80,
    },
    {
      title: "名称",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "类型",
      dataIndex: "type",
      key: "type",
      render: (type: string) => {
        const typeMap: Record<string, { color: string; text: string }> = {
          presto: { color: "blue", text: "Presto" },
          hive: { color: "green", text: "Hive" },
          doris: { color: "orange", text: "Doris" },
          mysql: { color: "purple", text: "MySQL" },
        };
        const config = typeMap[type] || { color: "default", text: type };
        return <Tag color={config.color}>{config.text}</Tag>;
      },
    },
    {
      title: "主机",
      dataIndex: "host",
      key: "host",
    },
    {
      title: "端口",
      dataIndex: "port",
      key: "port",
    },
    {
      title: "数据库",
      dataIndex: "database",
      key: "database",
      render: (text: string) => text || "-",
    },
    {
      title: "状态",
      dataIndex: "status",
      key: "status",
      render: (status: string) => {
        const statusMap: Record<string, { color: string; text: string }> = {
          active: { color: "success", text: "活跃" },
          inactive: { color: "default", text: "未激活" },
          error: { color: "error", text: "错误" },
        };
        const config = statusMap[status] || { color: "default", text: status };
        return <Tag color={config.color}>{config.text}</Tag>;
      },
    },
    {
      title: "操作",
      key: "action",
      width: 120,
      render: (_: any, record: DataSource) => (
        <Space size="small">
          <Popconfirm
            title="确定要删除这个数据源吗？"
            onConfirm={() => handleDelete(record.id!)}
            okText="确定"
            cancelText="取消"
          >
            <Button
              type="link"
              danger
              size="small"
              icon={<DeleteOutlined />}
            >
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <ProCard
        title="数据源管理"
        headerBordered
        style={{
          borderRadius: "12px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        }}
        extra={
          <Button
            icon={<ReloadOutlined />}
            onClick={() => loadDataSourceList(pagination.current, pagination.pageSize)}
            loading={loading}
          >
            刷新
          </Button>
        }
      >
        <div style={{ marginBottom: "24px" }}>
          <Text type="secondary" style={{ fontSize: "14px" }}>
            选择数据源类型进行配置，支持 Presto、Hive、Doris、MySQL 等多种数据源。
          </Text>
        </div>
        <Row gutter={[24, 24]} style={{ marginBottom: "24px" }}>
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

        <div style={{ marginTop: "24px" }}>
          <Title level={5}>已配置的数据源</Title>
          <Table
            columns={columns}
            dataSource={dataSourceList}
            rowKey="id"
            loading={loading}
            pagination={{
              current: pagination.current,
              pageSize: pagination.pageSize,
              total: pagination.total,
              showSizeChanger: true,
              showTotal: (total) => `共 ${total} 条`,
            }}
            onChange={handleTableChange}
          />
        </div>
      </ProCard>

      <DataSourceConfigModal
        visible={modalVisible}
        dataSourceType={selectedDataSource}
        onClose={handleModalClose}
        onSuccess={handleSaveSuccess}
      />
    </div>
  );
}

