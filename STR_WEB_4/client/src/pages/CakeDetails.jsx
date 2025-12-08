import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { getCake } from "../api/cakes";

const CakeDetails = () => {
  const { id } = useParams();
  const [cake, setCake] = useState(null);

  useEffect(() => {
    const fetchCake = async () => {
      const { data } = await getCake(id);
      setCake(data);
    };
    fetchCake();
  }, [id]);

  if (!cake) return <p>Загрузка...</p>;

  return (
    <div>
      <h1>{cake.name}</h1>
      <img src={cake.image || "/placeholder.png"} alt={cake.name} width={200} />
      <p>Цена: {cake.price}₽</p>
      <p>{cake.description}</p>
    </div>
  );
};

export default CakeDetails;
