import React, { useState } from "react";
import "./css/AIRecipeGenerator.css"

const AIRecipeGenerator = ({ onRecipeGenerated }) => {
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/api/generate-recipe", { method: "POST" });
      const data = await res.json();
      if (!data || !data.title) {
        alert("AI вернул некорректный рецепт");
        setLoading(false);
        return;
      }
      onRecipeGenerated(data);
    } catch (err) {
      console.error("Ошибка генерации рецепта:", err);
      alert("Ошибка генерации рецепта");
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      type="button"
      onClick={handleGenerate}
      disabled={loading}
      className="ai-button"
    >
      {loading ? "Генерация..." : "Сгенерировать рецепт AI"}
    </button>
  );
};

AIRecipeGenerator.defaultProps = {
  onRecipeGenerated: () => {}
};

export default AIRecipeGenerator;
