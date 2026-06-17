import { useEffect, useMemo, useState } from 'react';
import { CheckCircle2, Edit3, PauseCircle, Plus, RefreshCw, Search } from 'lucide-react';

import { StatusBadge } from '../components/StatusBadge.jsx';
import { createRecord, fetchRecords, updateRecord, updateRecordStatus } from '../services/api.js';

function formatValue(value, column, referenceOptions = {}) {
  if (value === null || value === undefined || value === '') {
    return '-';
  }
  if (column.type === 'reference') {
    const option = referenceOptions[column.referenceKey]?.find((item) => String(item.value) === String(value));
    return option?.label || value;
  }
  if (column.type === 'money') {
    return `¥${Number(value).toFixed(2)}`;
  }
  if (column.type === 'boolean') {
    return value ? '是' : '否';
  }
  if (column.type === 'status') {
    return <StatusBadge value={value} />;
  }
  return value;
}

function preparePayload(record, fields) {
  return fields.reduce((payload, field) => {
    const value = record[field.key];
    if (value === '' || value === undefined) {
      payload[field.key] = field.type === 'checkbox' ? false : null;
      return payload;
    }
    if (field.type === 'number') {
      payload[field.key] = Number(value);
      return payload;
    }
    if (field.type === 'reference') {
      payload[field.key] = Number(value);
      return payload;
    }
    if (field.type === 'checkbox') {
      payload[field.key] = Boolean(value);
      return payload;
    }
    payload[field.key] = value;
    return payload;
  }, {});
}

function RecordForm({ config, editingRecord, onCancel, onSubmit, referenceErrors, referenceOptions, submitting }) {
  const [record, setRecord] = useState(() => ({ ...config.emptyRecord, ...editingRecord }));

  useEffect(() => {
    setRecord({ ...config.emptyRecord, ...editingRecord });
  }, [config, editingRecord]);

  const updateField = (key, value) => {
    setRecord((current) => ({ ...current, [key]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(preparePayload(record, config.fields));
  };

  return (
    <form className="record-form" onSubmit={handleSubmit}>
      <div className="form-heading">
        <h3>{editingRecord?.id ? '编辑资料' : '新增资料'}</h3>
        <button className="text-button" onClick={onCancel} type="button">
          取消
        </button>
      </div>
      <div className="form-grid">
        {config.fields.map((field) => {
          const value = record[field.key] ?? '';
          if (field.type === 'textarea') {
            return (
              <label className="form-field wide" key={field.key}>
                <span>{field.label}</span>
                <textarea value={value} onChange={(event) => updateField(field.key, event.target.value)} />
              </label>
            );
          }
          if (field.type === 'select') {
            return (
              <label className="form-field" key={field.key}>
                <span>{field.label}</span>
                <select value={value} onChange={(event) => updateField(field.key, event.target.value)}>
                  {field.options.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </label>
            );
          }
          if (field.type === 'reference') {
            const reference = field.reference;
            const options = referenceOptions[reference.referenceKey] || [];
            const referenceError = referenceErrors[reference.referenceKey];
            const isDisabled = Boolean(referenceError) || options.length === 0;

            return (
              <label className="form-field" key={field.key}>
                <span>{field.label}</span>
                <select
                  disabled={isDisabled}
                  required={field.required}
                  value={value === null ? '' : String(value)}
                  onChange={(event) => updateField(field.key, event.target.value)}
                >
                  <option value="">
                    {referenceError || (options.length === 0 ? reference.emptyMessage : reference.placeholder)}
                  </option>
                  {options.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </label>
            );
          }
          if (field.type === 'checkbox') {
            return (
              <label className="form-field checkbox-field" key={field.key}>
                <input
                  checked={Boolean(record[field.key])}
                  type="checkbox"
                  onChange={(event) => updateField(field.key, event.target.checked)}
                />
                <span>{field.label}</span>
              </label>
            );
          }
          return (
            <label className="form-field" key={field.key}>
              <span>{field.label}</span>
              <input
                min={field.type === 'number' ? '0' : undefined}
                required={field.required}
                step={field.step}
                type={field.type || 'text'}
                value={value}
                onChange={(event) => updateField(field.key, event.target.value)}
              />
            </label>
          );
        })}
      </div>
      <div className="form-actions">
        <button className="primary-button" disabled={submitting} type="submit">
          {submitting ? '保存中' : '保存'}
        </button>
      </div>
    </form>
  );
}

export function MasterDataPage({ config }) {
  const [keyword, setKeyword] = useState('');
  const [status, setStatus] = useState('');
  const [page, setPage] = useState(1);
  const [data, setData] = useState({ items: [], total: 0, page: 1, page_size: 20 });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [editingRecord, setEditingRecord] = useState(null);
  const [referenceErrors, setReferenceErrors] = useState({});
  const [referenceOptions, setReferenceOptions] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const totalPages = useMemo(() => Math.max(1, Math.ceil(data.total / data.page_size)), [data]);
  const referenceFields = useMemo(
    () => config.fields.filter((field) => field.type === 'reference' && field.reference),
    [config],
  );

  const loadData = async (targetPage = page, nextFilters = { keyword, status }) => {
    setLoading(true);
    setError('');
    try {
      const result = await fetchRecords(config.endpoint, {
        keyword: nextFilters.keyword,
        status: nextFilters.status,
        page: targetPage,
        pageSize: 20,
      });
      setData(result);
    } catch (err) {
      setError(err.message || '加载失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [config.endpoint, page]);

  useEffect(() => {
    const loadReferenceOptions = async () => {
      const uniqueReferences = referenceFields.reduce((references, field) => {
        references.set(field.reference.referenceKey, field.reference);
        return references;
      }, new Map());

      if (uniqueReferences.size === 0) {
        setReferenceOptions({});
        setReferenceErrors({});
        return;
      }

      const nextOptions = {};
      const nextErrors = {};

      await Promise.all(
        Array.from(uniqueReferences.values()).map(async (reference) => {
          try {
            const result = await fetchRecords(reference.endpoint, { page: 1, pageSize: 100 });
            nextOptions[reference.referenceKey] = result.items.map((item) => ({
              value: item[reference.valueKey],
              label: item[reference.labelKey],
            }));
          } catch (err) {
            nextOptions[reference.referenceKey] = [];
            nextErrors[reference.referenceKey] = reference.errorMessage;
          }
        }),
      );

      setReferenceOptions(nextOptions);
      setReferenceErrors(nextErrors);
    };

    loadReferenceOptions();
  }, [referenceFields]);

  const handleSearch = (event) => {
    event.preventDefault();
    setPage(1);
    loadData(1);
  };

  const resetSearch = () => {
    const nextFilters = { keyword: '', status: '' };
    setKeyword('');
    setStatus('');
    setPage(1);
    loadData(1, nextFilters);
  };

  const handleSubmit = async (payload) => {
    setSubmitting(true);
    setError('');
    try {
      if (editingRecord?.id) {
        await updateRecord(config.endpoint, editingRecord.id, payload);
      } else {
        await createRecord(config.endpoint, payload);
      }
      setEditingRecord(null);
      await loadData();
    } catch (err) {
      setError(err.message || '保存失败');
    } finally {
      setSubmitting(false);
    }
  };

  const handleStatusToggle = async (record) => {
    const inactiveValue = config.statusOptions.some((option) => option.value === 'INACTIVE') ? 'INACTIVE' : 'OFFLINE';
    const activeValue = config.statusOptions.some((option) => option.value === 'ACTIVE') ? 'ACTIVE' : 'ONLINE';
    const nextStatus = record.status === activeValue ? inactiveValue : activeValue;
    try {
      await updateRecordStatus(config.endpoint, record.id, nextStatus);
      await loadData();
    } catch (err) {
      setError(err.message || '状态更新失败');
    }
  };

  return (
    <section className="master-page">
      <div className="page-header">
        <div>
          <h1>{config.title}</h1>
          <p>{config.description}</p>
        </div>
      </div>

      <div className="toolbar filter-bar">
        <form className="search-form" onSubmit={handleSearch}>
          <div className="search-box">
            <Search size={17} />
            <input
              placeholder="输入关键字搜索"
              value={keyword}
              onChange={(event) => setKeyword(event.target.value)}
            />
          </div>
          <select value={status} onChange={(event) => setStatus(event.target.value)}>
            <option value="">全部状态</option>
            {config.statusOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <button className="primary-button" type="submit">
            查询
          </button>
          <button className="secondary-button" type="button" onClick={resetSearch}>
            重置
          </button>
        </form>
        <div className="toolbar-actions">
          <button className="icon-button" title="刷新" type="button" onClick={loadData}>
            <RefreshCw size={17} />
          </button>
          <button className="primary-button" type="button" onClick={() => setEditingRecord({})}>
            <Plus size={17} />
            新增
          </button>
        </div>
      </div>

      {error ? <div className="error-banner">{error}</div> : null}

      {editingRecord ? (
        <RecordForm
          config={config}
          editingRecord={editingRecord}
          referenceErrors={referenceErrors}
          referenceOptions={referenceOptions}
          submitting={submitting}
          onCancel={() => setEditingRecord(null)}
          onSubmit={handleSubmit}
        />
      ) : null}

      <div className="table-panel">
        <table>
          <thead>
            <tr>
              {config.columns.map((column) => (
                <th key={column.key}>{column.label}</th>
              ))}
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((record) => (
              <tr key={record.id}>
                {config.columns.map((column) => (
                  <td key={column.key}>{formatValue(record[column.key], column, referenceOptions)}</td>
                ))}
                <td>
                  <div className="row-actions">
                    <button className="icon-button" title="编辑" type="button" onClick={() => setEditingRecord(record)}>
                      <Edit3 size={16} />
                    </button>
                    <button className="icon-button" title="启用或停用" type="button" onClick={() => handleStatusToggle(record)}>
                      {record.status === 'ACTIVE' || record.status === 'ONLINE' ? (
                        <PauseCircle size={16} />
                      ) : (
                        <CheckCircle2 size={16} />
                      )}
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {!loading && data.items.length === 0 ? (
              <tr>
                <td className="empty-cell" colSpan={config.columns.length + 1}>
                  暂无数据
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>

      <div className="pagination">
        <span>
          共 {data.total} 条，第 {page} / {totalPages} 页
        </span>
        <div>
          <button className="secondary-button" disabled={page <= 1} type="button" onClick={() => setPage(page - 1)}>
            上一页
          </button>
          <button
            className="secondary-button"
            disabled={page >= totalPages}
            type="button"
            onClick={() => setPage(page + 1)}
          >
            下一页
          </button>
        </div>
      </div>
    </section>
  );
}
