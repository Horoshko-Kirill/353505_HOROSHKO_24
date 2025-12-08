import api from "./axios";

export const getCakes = (search = "", sort = "") =>
  api.get(`/cakes?search=${search}&sort=${sort}`);

export const getCake = (id) => api.get(`/cakes/${id}`);

export const createCake = (data) => api.post("/cakes", data);

export const updateCake = (id, data) => api.put(`/cakes/${id}`, data);

export const deleteCake = (id) => api.delete(`/cakes/${id}`);
