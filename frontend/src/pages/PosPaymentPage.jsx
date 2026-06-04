import { useEffect, useMemo, useState } from 'react';
import { Plus, Trash2 } from 'lucide-react';

import { createRecord, fetchRecords } from '../services/api.js';

const mealTypeOptions = [
  { label: '早餐', value: 'BREAKFAST' },
  { label: '午餐', value: 'LUNCH' },
  { label: '晚餐', value: 'DINNER' },
  { label: '其他', value: 'OTHER' },
];

const visitorPaymentOptions = [
  { label: '访客扫码', value: 'VISITOR_QR' },
  { label: '模拟支付宝', value: 'MOCK_ALIPAY' },
  { label: '模拟微信', value: 'MOCK_WECHAT' },
];

function money(value) {
  return `¥${Number(value || 0).toFixed(2)}`;
}

function statusText(value) {
  const labels = { PAID: '已支付', PENDING: '待支付', FAILED: '失败' };
  return labels[value] || value || '-';
}

export function PosPaymentPage({ mode }) {
  const isEmployee = mode === 'employee';
  const [employees, setEmployees] = useState([]);
  const [visitors, setVisitors] = useState([]);
  const [devices, setDevices] = useState([]);
  const [stalls, setStalls] = useState([]);
  const [dishes, setDishes] = useState([]);
  const [form, setForm] = useState({
    card_no: '',
    visitor_id: '',
    visitor_name: '',
    device_id: '',
    stall_id: '',
    meal_type: 'LUNCH',
    payment_method: 'VISITOR_QR',
  });
  const [items, setItems] = useState([{ dish_id: '', quantity: 1 }]);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    async function loadOptions() {
      setError('');
      try {
        const [employeeData, visitorData, deviceData, stallData, dishData] = await Promise.all([
          fetchRecords('/api/v1/employees', { page: 1, pageSize: 100 }),
          fetchRecords('/api/v1/visitors', { page: 1, pageSize: 100 }),
          fetchRecords('/api/v1/devices', { page: 1, pageSize: 100 }),
          fetchRecords('/api/v1/stalls', { page: 1, pageSize: 100 }),
          fetchRecords('/api/v1/dishes', { page: 1, pageSize: 100 }),
        ]);
        setEmployees(employeeData.items.filter((item) => item.status === 'ACTIVE' && item.card_no));
        setVisitors(visitorData.items.filter((item) => item.status === 'ACTIVE'));
        setDevices(deviceData.items.filter((item) => item.status === 'ONLINE'));
        setStalls(stallData.items.filter((item) => item.status === 'ACTIVE'));
        setDishes(dishData.items.filter((item) => item.status === 'ACTIVE' && item.is_available));
      } catch (err) {
        setError(err.message || '基础资料加载失败');
      }
    }
    loadOptions();
  }, []);

  const availableDishes = useMemo(
    () => dishes.filter((dish) => !form.stall_id || String(dish.stall_id) === String(form.stall_id)),
    [dishes, form.stall_id],
  );

  const totalAmount = useMemo(
    () =>
      items.reduce((total, item) => {
        const dish = dishes.find((candidate) => String(candidate.id) === String(item.dish_id));
        return total + Number(dish?.unit_price || 0) * Number(item.quantity || 0);
      }, 0),
    [dishes, items],
  );

  const updateForm = (key, value) => {
    setForm((current) => ({ ...current, [key]: value }));
    if (key === 'stall_id') {
      setItems([{ dish_id: '', quantity: 1 }]);
    }
  };

  const updateItem = (index, key, value) => {
    setItems((current) => current.map((item, itemIndex) => (itemIndex === index ? { ...item, [key]: value } : item)));
  };

  const removeItem = (index) => {
    setItems((current) => current.filter((_, itemIndex) => itemIndex !== index));
  };

  const submitPayment = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    setError('');
    setResult(null);
    try {
      const payloadItems = items.map((item) => ({
        dish_id: Number(item.dish_id),
        quantity: Number(item.quantity),
      }));
      const endpoint = isEmployee ? '/api/v1/pos/employee-card-payment' : '/api/v1/pos/visitor-qr-payment';
      const payload = isEmployee
        ? {
            card_no: form.card_no,
            device_id: Number(form.device_id),
            stall_id: Number(form.stall_id),
            meal_type: form.meal_type,
            items: payloadItems,
          }
        : {
            visitor_id: form.visitor_id ? Number(form.visitor_id) : null,
            visitor_name: form.visitor_name || null,
            device_id: Number(form.device_id),
            stall_id: Number(form.stall_id),
            meal_type: form.meal_type,
            payment_method: form.payment_method,
            items: payloadItems,
          };
      const response = await createRecord(endpoint, payload);
      setResult(response);
    } catch (err) {
      setError(err.message || '提交消费失败');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className="master-page">
      <div className="section-heading">
        <h2>{isEmployee ? '员工刷卡消费' : '访客扫码消费'}</h2>
        <p>{isEmployee ? '模拟员工使用餐卡在 POS 设备完成消费。' : '模拟访客扫码支付，默认 mock 支付成功。'}</p>
      </div>

      {error ? <div className="error-banner">{error}</div> : null}

      <form className="record-form" onSubmit={submitPayment}>
        <div className="form-grid">
          {isEmployee ? (
            <label className="form-field">
              <span>员工卡号</span>
              <select required value={form.card_no} onChange={(event) => updateForm('card_no', event.target.value)}>
                <option value="">{employees.length ? '请选择员工卡号' : '请先维护员工卡号'}</option>
                {employees.map((employee) => (
                  <option key={employee.id} value={employee.card_no}>
                    {employee.name} - {employee.card_no}
                  </option>
                ))}
              </select>
            </label>
          ) : (
            <>
              <label className="form-field">
                <span>已有访客</span>
                <select value={form.visitor_id} onChange={(event) => updateForm('visitor_id', event.target.value)}>
                  <option value="">不选择已有访客</option>
                  {visitors.map((visitor) => (
                    <option key={visitor.id} value={visitor.id}>
                      {visitor.name} - {visitor.company || '访客'}
                    </option>
                  ))}
                </select>
              </label>
              <label className="form-field">
                <span>临时访客姓名</span>
                <input value={form.visitor_name} onChange={(event) => updateForm('visitor_name', event.target.value)} />
              </label>
            </>
          )}

          <label className="form-field">
            <span>POS 设备</span>
            <select required value={form.device_id} onChange={(event) => updateForm('device_id', event.target.value)}>
              <option value="">{devices.length ? '请选择在线设备' : '暂无在线设备'}</option>
              {devices.map((device) => (
                <option key={device.id} value={device.id}>
                  {device.device_name}
                </option>
              ))}
            </select>
          </label>

          <label className="form-field">
            <span>档口</span>
            <select required value={form.stall_id} onChange={(event) => updateForm('stall_id', event.target.value)}>
              <option value="">{stalls.length ? '请选择档口' : '请先维护档口资料'}</option>
              {stalls.map((stall) => (
                <option key={stall.id} value={stall.id}>
                  {stall.name}
                </option>
              ))}
            </select>
          </label>

          <label className="form-field">
            <span>餐次</span>
            <select value={form.meal_type} onChange={(event) => updateForm('meal_type', event.target.value)}>
              {mealTypeOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>

          {!isEmployee ? (
            <label className="form-field">
              <span>支付方式</span>
              <select value={form.payment_method} onChange={(event) => updateForm('payment_method', event.target.value)}>
                {visitorPaymentOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>
          ) : null}
        </div>

        <div className="line-items">
          <div className="form-heading">
            <h3>菜品明细</h3>
            <button className="secondary-button" type="button" onClick={() => setItems([...items, { dish_id: '', quantity: 1 }])}>
              <Plus size={16} />
              添加菜品
            </button>
          </div>
          {items.map((item, index) => (
            <div className="line-item-row" key={`${index}-${item.dish_id}`}>
              <label className="form-field">
                <span>菜品</span>
                <select required value={item.dish_id} onChange={(event) => updateItem(index, 'dish_id', event.target.value)}>
                  <option value="">{availableDishes.length ? '请选择菜品' : '请先选择有可售菜品的档口'}</option>
                  {availableDishes.map((dish) => (
                    <option key={dish.id} value={dish.id}>
                      {dish.name} - {money(dish.unit_price)}
                    </option>
                  ))}
                </select>
              </label>
              <label className="form-field">
                <span>数量</span>
                <input
                  min="1"
                  required
                  type="number"
                  value={item.quantity}
                  onChange={(event) => updateItem(index, 'quantity', event.target.value)}
                />
              </label>
              <button className="icon-button line-remove" disabled={items.length === 1} type="button" onClick={() => removeItem(index)}>
                <Trash2 size={16} />
              </button>
            </div>
          ))}
        </div>

        <div className="payment-summary">
          <strong>预计金额：{money(totalAmount)}</strong>
          <button className="primary-button" disabled={submitting || totalAmount <= 0} type="submit">
            {submitting ? '提交中' : '提交消费'}
          </button>
        </div>
      </form>

      {result ? (
        <div className="result-panel">
          <h3>支付成功</h3>
          <p>订单号：{result.order.order_no}</p>
          <p>支付状态：{statusText(result.payment.payment_status)}</p>
          <p>应付金额：{money(result.order.payable_amount)}</p>
        </div>
      ) : null}
    </section>
  );
}
