import React, { useState, useEffect } from "react";
import { getNews, createNews, deleteNews } from "../api/news";
import "./css/NewsManager.css";

const NewsManager = () => {
  const [newsList, setNewsList] = useState([]);
  const [form, setForm] = useState({ title: "", description: "", videoUrl: "" });
  const [error, setError] = useState("");

  useEffect(() => { loadNews(); }, []);

  const loadNews = async () => {
    try {
      const { data } = await getNews();
      setNewsList(data);
    } catch (err) {
      console.error("Ошибка загрузки новостей:", err.response?.data || err.message);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!form.title.trim() || !form.description.trim()) return setError("Заполните заголовок и описание!");
    try {
      await createNews(form);
      setForm({ title: "", description: "", videoUrl: "" });
      loadNews();
    } catch (err) {
      console.error("Ошибка создания новости:", err.response?.data || err.message);
      setError("Ошибка при создании новости.");
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteNews(id);
      loadNews();
    } catch (err) {
      console.error("Ошибка удаления новости:", err.response?.data || err.message);
    }
  };

  return (
    <div className="news-list">
      <h2>Новости</h2>

      <form onSubmit={handleSubmit} style={{ marginBottom: "30px" }}>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <input placeholder="Заголовок" name="title" value={form.title} onChange={handleInputChange} />
        <textarea placeholder="Описание" name="description" value={form.description} onChange={handleInputChange} rows={3} />
        <input placeholder="Ссылка на YouTube видео" name="videoUrl" value={form.videoUrl} onChange={handleInputChange} />

        {form.videoUrl && extractYouTubeId(form.videoUrl) && (
          <iframe
            src={`https://www.youtube.com/embed/${extractYouTubeId(form.videoUrl)}`}
            title="Предпросмотр"
            frameBorder="0"
            allowFullScreen
          ></iframe>
        )}
        <button type="submit">Добавить новость</button>
      </form>

      {newsList.map((n) => (
        <div key={n._id} className="news-card">
          <h4>{n.title}</h4>
          <p>{n.description}</p>
          {n.videoUrl && extractYouTubeId(n.videoUrl) && (
            <iframe
              src={`https://www.youtube.com/embed/${extractYouTubeId(n.videoUrl)}`}
              title={n.title}
              frameBorder="0"
              allowFullScreen
            ></iframe>
          )}
          <button onClick={() => handleDelete(n._id)} style={{ color: "white", background: "red" }}>Удалить</button>
        </div>
      ))}
    </div>
  );
};

const extractYouTubeId = (url) => {
  if (!url) return null;
  const regExp = /(?:youtu\.be\/|youtube\.com\/(?:embed\/|watch\?v=|v\/))([\w-]{11})/;
  const match = url.match(regExp);
  return match ? match[1] : null;
};

export default NewsManager;
