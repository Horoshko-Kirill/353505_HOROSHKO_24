import { useState, useEffect } from "react";
import api from "../api";
import CakeCard from "../components/CakeCard";

const CatalogPage = () => {
  const [cakes, setCakes] = useState([]);
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState("price-asc");

  useEffect(() => {
    loadCakes();
  }, []);

const loadCakes = async () => {
  let sortBy = "price";
  let sortOrder = "asc";

  if (sort === "price-desc") sortOrder = "desc";

  const res = await api.get(
    `/cakes?search=${query}&sortBy=${sortBy}&sortOrder=${sortOrder}`
  );
  setCakes(res.data);
};


  return (
    <div>
      <h1>Каталог тортов</h1>

      <input
        type="text"
        placeholder="Поиск"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <select value={sort} onChange={(e) => setSort(e.target.value)}>
        <option value="price-asc">Цена ↑</option>
        <option value="price-desc">Цена ↓</option>
      </select>

      <button onClick={loadCakes}>Поиск</button>

      <div className="cake-list">
        {cakes.map((c) => (
          <CakeCard key={c._id} cake={c} />
        ))}
      </div>
    </div>
  );
};

export default CatalogPage;
