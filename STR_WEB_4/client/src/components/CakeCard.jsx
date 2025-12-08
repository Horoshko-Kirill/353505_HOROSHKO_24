import React from "react";
import { useNavigate } from "react-router-dom";

const CakeCard = ({ cake }) => {
  const navigate = useNavigate();

  return (
    <div className="recipe-card">
      <div className="image-wrapper">
        <img src={cake.image || "/placeholder.png"} alt={cake.name} />
      </div>
      <h3>{cake.name}</h3>
      <p>Цена: {cake.price}₽</p>
      <button className="ai-button" onClick={() => navigate(`/cakes/${cake._id}`)}>Подробнее</button>
    </div>
  );
};

export default CakeCard;
