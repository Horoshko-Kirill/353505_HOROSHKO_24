import { useState, useEffect, useContext, useRef } from "react";
import { getCakes, createCake, deleteCake } from "../api/cakes";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";
import { TimezoneContext } from "../context/TimezoneContext";
import CakeCard from "../components/CakeCard";

const AdminPage = () => {
  const [cakes, setCakes] = useState([]);
  const [form, setForm] = useState({ name: "", price: "", description: "", image: "" });
  const { user } = useContext(AuthContext);
  const { timezone, toggleTimezone } = useContext(TimezoneContext);
  const fileInputRef = useRef(null);
  const [editingCake, setEditingCake] = useState(null);

  useEffect(() => { loadCakes(); }, []);

  const loadCakes = async () => {
    try {
      const { data } = await getCakes();
      setCakes(data);
    } catch (err) {
      console.error("Ошибка загрузки тортов:", err);
    }
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    try {
      const res = await axios.post("http://localhost:5000/api/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setForm(prev => ({ ...prev, image: `http://localhost:5000${res.data.imageUrl}` }));
    } catch (err) { console.error("Ошибка загрузки изображения:", err); }
  };

  const handleCreateCake = async () => {
    if (!form.name || !form.price) return alert("Название и цена обязательны!");
    try {
      await createCake(form, user.token);
      resetForm();
      loadCakes();
    } catch (err) { console.error("Ошибка при добавлении торта:", err); }
  };

  const handleDeleteCake = async (id) => {
    try {
      await deleteCake(id, user.token);
      loadCakes();
    } catch (err) { console.error("Ошибка при удалении торта:", err); }
  };

  const handleEdit = (cake) => {
    setEditingCake(cake);
    setForm({
      name: cake.name,
      price: cake.price,
      description: cake.description,
      image: cake.image || "",
    });
    if (fileInputRef.current) fileInputRef.current.value = null;
  };

  const handleUpdateCake = async () => {
    if (!form.name || !form.price) return alert("Название и цена обязательны!");
    try {
      const updateData = { ...form };
      if (!updateData.image && editingCake.image) updateData.image = editingCake.image;

      await axios.put(
        `http://localhost:5000/api/cakes/${editingCake._id}`,
        updateData,
        { headers: { Authorization: `Bearer ${user.token}` } }
      );

      resetForm();
      loadCakes();
    } catch (err) { console.error("Ошибка при обновлении торта:", err); }
  };

  const resetForm = () => {
    setEditingCake(null);
    setForm({ name: "", price: "", description: "", image: "" });
    if (fileInputRef.current) fileInputRef.current.value = null;
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return "";
    const date = new Date(dateStr);
    return timezone === "utc" ? date.toUTCString() : date.toLocaleString();
  };

  return (
    <div>
      <h1>Админ-панель</h1>

      <p>
        Таймзона пользователя {timezone === "local" ? "Локальное" : "UTC"}
      </p>

      <h2>{editingCake ? "Редактировать торт" : "Добавить торт"}</h2>
      <input placeholder="Название" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
      <input placeholder="Цена" type="number" value={form.price} onChange={e => setForm({ ...form, price: e.target.value })} />
      <input placeholder="Описание" value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
      <input type="file" ref={fileInputRef} onChange={handleFileChange} />
      {form.image && <div><p>Превью изображения:</p><img src={form.image} alt="Preview" width={150} /></div>}
      <button onClick={editingCake ? handleUpdateCake : handleCreateCake}>
        {editingCake ? "Сохранить изменения" : "Добавить"}
      </button>

      <h2>Список тортов</h2>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
        {cakes.map(c => (
          <div key={c._id} style={{ border: "1px solid #ccc", padding: "10px", width: "220px" }}>
            <CakeCard cake={c} onDetails={() => alert(`Название: ${c.name}\nЦена: ${c.price}₽\nОписание: ${c.description}`)} />
            <p>Создано: {formatDate(c.createdAt)}</p>
            <p>Обновлено: {formatDate(c.updatedAt)}</p>
            <button onClick={() => handleEdit(c)} style={{ background: "blue", color: "#fff", marginRight: "5px" }}>Редактировать</button>
            <button onClick={() => handleDeleteCake(c._id)} style={{ background: "red", color: "#fff" }}>Удалить</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminPage;
