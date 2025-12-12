"use client";

import { Modal, Form, Input, InputNumber, Select, Switch, message } from "antd";
import { useEffect, useState } from "react";
import { createDataSource, DataSource } from "@/services/datasource";

interface DataSourceConfigModalProps {
  visible: boolean;
  dataSourceType: string | null;
  onClose: () => void;
  onSuccess?: () => void; // 保存成功后的回调
}

interface ConfigField {
  name: string;
  label: string;
  required: boolean;
  type: "input" | "number" | "select" | "switch" | "password";
  placeholder?: string;
  options?: { label: string; value: string }[];
  defaultValue?: any;
}

// 不同数据源的配置字段定义
const configFieldsMap: Record<string, ConfigField[]> = {
  presto: [
    { name: "name", label: "数据源名称", required: true, type: "input", placeholder: "请输入数据源名称" },
    { name: "host", label: "主机地址", required: true, type: "input", placeholder: "localhost" },
    { name: "port", label: "端口", required: true, type: "number", placeholder: "8080", defaultValue: 8080 },
    { name: "catalog", label: "Catalog", required: true, type: "input", placeholder: "hive" },
    { name: "schema", label: "Schema", required: false, type: "input", placeholder: "default" },
    { name: "username", label: "用户名", required: false, type: "input", placeholder: "请输入用户名" },
    { name: "password", label: "密码", required: false, type: "password", placeholder: "请输入密码" },
    { name: "ssl", label: "启用SSL", required: false, type: "switch", defaultValue: false },
  ],
  hive: [
    { name: "name", label: "数据源名称", required: true, type: "input", placeholder: "请输入数据源名称" },
    { name: "host", label: "主机地址", required: true, type: "input", placeholder: "localhost" },
    { name: "port", label: "端口", required: true, type: "number", placeholder: "10000", defaultValue: 10000 },
    { name: "database", label: "数据库", required: true, type: "input", placeholder: "default" },
    { name: "authType", label: "认证方式", required: false, type: "select", options: [
      { label: "无认证", value: "none" },
      { label: "用户名密码", value: "userpass" },
      { label: "Kerberos", value: "kerberos" },
    ], defaultValue: "none" },
    { name: "username", label: "用户名", required: false, type: "input", placeholder: "请输入用户名" },
    { name: "password", label: "密码", required: false, type: "password", placeholder: "请输入密码" },
    { name: "serviceDiscoveryMode", label: "服务发现模式", required: false, type: "select", options: [
      { label: "ZooKeeper", value: "zookeeper" },
      { label: "直连", value: "direct" },
    ], defaultValue: "direct" },
  ],
  doris: [
    { name: "name", label: "数据源名称", required: true, type: "input", placeholder: "请输入数据源名称" },
    { name: "host", label: "主机地址", required: true, type: "input", placeholder: "localhost" },
    { name: "port", label: "端口", required: true, type: "number", placeholder: "9030", defaultValue: 9030 },
    { name: "database", label: "数据库", required: true, type: "input", placeholder: "test_db" },
    { name: "username", label: "用户名", required: true, type: "input", placeholder: "root" },
    { name: "password", label: "密码", required: true, type: "password", placeholder: "请输入密码" },
    { name: "charset", label: "字符集", required: false, type: "select", options: [
      { label: "UTF-8", value: "utf8" },
      { label: "UTF-8MB4", value: "utf8mb4" },
      { label: "GBK", value: "gbk" },
    ], defaultValue: "utf8" },
    { name: "timeout", label: "连接超时(秒)", required: false, type: "number", placeholder: "30", defaultValue: 30 },
  ],
  mysql: [
    { name: "name", label: "数据源名称", required: true, type: "input", placeholder: "请输入数据源名称" },
    { name: "host", label: "主机地址", required: true, type: "input", placeholder: "localhost" },
    { name: "port", label: "端口", required: true, type: "number", placeholder: "3306", defaultValue: 3306 },
    { name: "database", label: "数据库", required: true, type: "input", placeholder: "test_db" },
    { name: "username", label: "用户名", required: true, type: "input", placeholder: "root" },
    { name: "password", label: "密码", required: true, type: "password", placeholder: "请输入密码" },
    { name: "charset", label: "字符集", required: false, type: "select", options: [
      { label: "UTF-8", value: "utf8" },
      { label: "UTF-8MB4", value: "utf8mb4" },
      { label: "GBK", value: "gbk" },
    ], defaultValue: "utf8mb4" },
    { name: "timeout", label: "连接超时(秒)", required: false, type: "number", placeholder: "30", defaultValue: 30 },
    { name: "ssl", label: "启用SSL", required: false, type: "switch", defaultValue: false },
  ],
};

const dataSourceNames: Record<string, string> = {
  presto: "Presto",
  hive: "Hive",
  doris: "Doris",
  mysql: "MySQL",
};

export default function DataSourceConfigModal({
  visible,
  dataSourceType,
  onClose,
  onSuccess,
}: DataSourceConfigModalProps) {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  // Hooks 必须在组件顶层调用，不能在条件判断之后
  const authType = Form.useWatch("authType", form);

  useEffect(() => {
    if (visible && dataSourceType) {
      form.resetFields();
    }
  }, [visible, dataSourceType, form]);

  /**
   * 根据数据源类型构建 config 对象
   */
  const buildConfig = (type: string | null, values: any): Record<string, any> => {
    const config: Record<string, any> = {};
    
    if (type === 'presto') {
      if (values.ssl !== undefined) {
        config.ssl = values.ssl;
      }
    } else if (type === 'hive') {
      if (values.authType) {
        config.authType = values.authType;
      }
      if (values.serviceDiscoveryMode) {
        config.serviceDiscoveryMode = values.serviceDiscoveryMode;
      }
    } else if (type === 'doris' || type === 'mysql') {
      if (values.charset) {
        config.charset = values.charset;
      }
      if (values.timeout !== undefined) {
        config.timeout = values.timeout;
      }
      if (type === 'mysql' && values.ssl !== undefined) {
        config.ssl = values.ssl;
      }
    }
    
    return config;
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      // 构建提交数据，确保类型正确
      const submitData: Omit<DataSource, 'id' | 'created_at' | 'updated_at' | 'last_test_at'> = {
        name: values.name,
        type: dataSourceType as 'presto' | 'hive' | 'doris' | 'mysql',
        host: values.host,
        port: Number(values.port),
        database: values.database,
        catalog: values.catalog,
        schema: values.schema,
        username: values.username,
        password: values.password,
        // 根据不同类型构建 config 对象
        config: buildConfig(dataSourceType, values),
      };

      // 调用 API 创建数据源
      const response = await createDataSource(submitData);
      
      if (response.code === 200) {
        message.success(`${dataSourceNames[dataSourceType || ""]} 数据源配置成功`);
        form.resetFields();
        onClose();
        // 触发成功回调，用于刷新列表
        if (onSuccess) {
          onSuccess();
        }
      } else {
        message.error(response.message || '保存失败');
      }
    } catch (error: any) {
      console.error("保存数据源失败:", error);
      message.error(error.message || '保存失败，请检查网络连接');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    form.resetFields();
    onClose();
  };

  if (!dataSourceType) {
    return null;
  }

  const configFields = configFieldsMap[dataSourceType] || [];

  const renderFormField = (field: ConfigField) => {
    // Hive 数据源：根据认证方式显示/隐藏用户名密码
    if (dataSourceType === "hive") {
      if (field.name === "username" || field.name === "password") {
        if (authType !== "userpass") {
          return null;
        }
      }
    }
    
    // 动态调整必填规则
    let rules = [];
    if (field.required) {
      if (dataSourceType === "hive" && (field.name === "username" || field.name === "password")) {
        // Hive 的用户名密码只有在选择用户名密码认证时才必填
        rules = authType === "userpass" 
          ? [{ required: true, message: `请输入${field.label}` }]
          : [];
      } else {
        rules = [{ required: true, message: `请输入${field.label}` }];
      }
    }

    switch (field.type) {
      case "input":
        return (
          <Form.Item
            key={field.name}
            name={field.name}
            label={field.label}
            rules={rules}
          >
            <Input placeholder={field.placeholder} />
          </Form.Item>
        );
      case "password":
        return (
          <Form.Item
            key={field.name}
            name={field.name}
            label={field.label}
            rules={rules}
          >
            <Input.Password placeholder={field.placeholder} />
          </Form.Item>
        );
      case "number":
        return (
          <Form.Item
            key={field.name}
            name={field.name}
            label={field.label}
            rules={rules}
          >
            <InputNumber
              placeholder={field.placeholder}
              style={{ width: "100%" }}
              min={1}
              max={65535}
            />
          </Form.Item>
        );
      case "select":
        return (
          <Form.Item
            key={field.name}
            name={field.name}
            label={field.label}
            rules={rules}
            initialValue={field.defaultValue}
          >
            <Select placeholder={`请选择${field.label}`} options={field.options} />
          </Form.Item>
        );
      case "switch":
        return (
          <Form.Item
            key={field.name}
            name={field.name}
            label={field.label}
            valuePropName="checked"
            initialValue={field.defaultValue}
          >
            <Switch />
          </Form.Item>
        );
      default:
        return null;
    }
  };

  return (
    <Modal
      title={`配置 ${dataSourceNames[dataSourceType]} 数据源`}
      open={visible}
      onOk={handleSubmit}
      onCancel={handleCancel}
      width={600}
      okText="保存"
      cancelText="取消"
      confirmLoading={loading}
      destroyOnClose
    >
      <Form
        form={form}
        layout="vertical"
        style={{ marginTop: "24px" }}
        initialValues={configFields.reduce((acc, field) => {
          if (field.defaultValue !== undefined) {
            acc[field.name] = field.defaultValue;
          }
          return acc;
        }, {} as Record<string, any>)}
      >
        {configFields
          .map((field) => renderFormField(field))
          .filter((field) => field !== null)}
      </Form>
    </Modal>
  );
}

