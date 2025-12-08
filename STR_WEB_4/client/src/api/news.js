import api from "./axios";

export const getNews = () => api.get("/news");
export const createNews = (data) => api.post("/news", data);
export const deleteNews = (id) => api.delete(`/news/${id}`);
