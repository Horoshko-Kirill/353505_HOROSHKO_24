import React, { Component } from "react";
import { getOrders, createOrder, updateOrder, deleteOrder } from "../api/orders";
import { getCakes } from "../api/cakes";
import "./css/OrderManager.css";

class OrderManager extends Component {
  state = { orders: [], cakes: [], form: { customerName: "", cakeId: "", address: "", deliveryDate: "", status: "pending" }, editingOrderId: null };

  componentDidMount() {
    this.loadOrders();
    this.loadCakes();
  }

  loadOrders = async () => {
    try { const { data } = await getOrders(); this.setState({ orders: data }); } 
    catch (err) { console.error("Ошибка загрузки заказов:", err.response?.data || err.message); }
  };

  loadCakes = async () => {
    try { const { data } = await getCakes(); this.setState({ cakes: data }); } 
    catch (err) { console.error("Ошибка загрузки тортов:", err.response?.data || err.message); }
  };

  handleInputChange = (e) => {
    const { name, value } = e.target;
    this.setState({ form: { ...this.state.form, [name]: value } });
  };

  handleSubmit = async (e) => {
    e.preventDefault();
    const { form, editingOrderId } = this.state;
    if (!form.customerName || !form.cakeId || !form.address || !form.deliveryDate) return alert("Заполните все поля!");
    try {
      if (editingOrderId) await updateOrder(editingOrderId, form);
      else await createOrder(form);
      this.setState({ form: { customerName: "", cakeId: "", address: "", deliveryDate: "", status: "pending" }, editingOrderId: null });
      this.loadOrders();
    } catch (err) {
      console.error("Ошибка создания/обновления заказа:", err.response?.data || err.message);
    }
  };

  handleEdit = (order) => {
    this.setState({
      editingOrderId: order._id,
      form: {
        customerName: order.customerName,
        cakeId: order.cakeId?._id || "",
        address: order.address,
        deliveryDate: order.deliveryDate?.slice(0, 16) || "",
        status: order.status
      }
    });
  };

  handleDelete = async (id) => { try { await deleteOrder(id); this.loadOrders(); } catch (err) { console.error(err); } };
  handleStatusChange = async (id, status) => { try { await updateOrder(id, { status }); this.loadOrders(); } catch (err) { console.error(err); } };

  render() {
    const { orders, cakes, form, editingOrderId } = this.state;

    return (
      <div>
        <h2>Управление заказами</h2>

        <form onSubmit={this.handleSubmit}>
          <input name="customerName" placeholder="Имя клиента" value={form.customerName} onChange={this.handleInputChange} />
          <select name="cakeId" value={form.cakeId} onChange={this.handleInputChange}>
            <option value="">Выберите торт</option>
            {cakes.map(c => <option key={c._id} value={c._id}>{c.name}</option>)}
          </select>
          <input name="address" placeholder="Адрес доставки" value={form.address} onChange={this.handleInputChange} />
          <input name="deliveryDate" type="datetime-local" value={form.deliveryDate} onChange={this.handleInputChange} />
          <select name="status" value={form.status} onChange={this.handleInputChange}>
            <option value="Ожидание">Ожидание</option>
            <option value="Готов">Готов</option>
            <option value="Отменен">Отменен</option>
          </select>
          <button type="submit">{editingOrderId ? "Сохранить" : "Добавить заказ"}</button>
        </form>

        <table className="order-table">
          <thead>
            <tr>
              <th>Клиент</th><th>Торт</th><th>Адрес</th><th>Дата доставки</th><th>Статус</th><th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(o => (
              <tr key={o._id}>
                <td>{o.customerName}</td>
                <td>{o.cakeId?.name || "—"}</td>
                <td>{o.address}</td>
                <td>{new Date(o.deliveryDate).toLocaleString()}</td>
                <td>
                  <select value={o.status} onChange={(e) => this.handleStatusChange(o._id, e.target.value)}>
                    <option value="Ожидание">Ожидание</option>
                    <option value="Готов">Готов</option>
                    <option value="Отменен">Отменен</option>
                  </select>
                </td>
                <td>
                  <button onClick={() => this.handleEdit(o)}>Редактировать</button>
                  <button onClick={() => this.handleDelete(o._id)} style={{ color: "red" }}>Удалить</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
}

export default OrderManager;
