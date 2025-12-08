import React, { useState, useEffect } from "react";
import { getRecipes, createRecipe, deleteRecipe } from "../api/recipes";
import AIRecipeGenerator from "./AIRecipeGenerator";
import "./css/RecipeBook.css";

const RecipeBook = () => {
  const [recipes, setRecipes] = useState([]);
  const [form, setForm] = useState({ title: "", category: "" });
  const [ingredientInput, setIngredientInput] = useState("");
  const [stepInput, setStepInput] = useState("");
  const [ingredients, setIngredients] = useState([]);
  const [steps, setSteps] = useState([]);
  const [searchText, setSearchText] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadRecipes();
  }, []);

  const loadRecipes = async () => {
    try {
      const { data } = await getRecipes();
      setRecipes(data);
    } catch (err) {
      console.error(err);
    }
  };

  const showMessage = (text, duration = 3000) => {
    setMessage(text);
    setTimeout(() => setMessage(""), duration);
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    const title = form.title.trim();
    if (!title || ingredients.length === 0 || steps.length === 0)
      return alert("Заполните все поля!");
    try {
      await createRecipe({ title, ingredients, steps, category: form.category });
      showMessage("Рецепт успешно создан!");
      setForm({ title: "", category: "dessert" });
      setIngredients([]);
      setSteps([]);
      setIngredientInput("");
      setStepInput("");
      loadRecipes();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div
      className="recipe-book"
      onMouseEnter={() => showMessage("Добро пожаловать в книгу рецептов!", 1500)}   // #3
      onMouseLeave={() => showMessage("Вы покинули область рецептов", 1500)}        // #4
    >
      <h2
        onDoubleClick={() => showMessage("Заголовок был двойным кликом!")}         // #2
      >
        База рецептов
      </h2>

      {message && (
        <div
          style={{
            background: "#4CAF50",
            color: "#fff",
            padding: "5px 10px",
            marginBottom: "10px"
          }}
        >
          {message}
        </div>
      )}

      <div style={{ marginBottom: "20px" }}>
        <input
          placeholder="Поиск по названию"
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          onKeyDown={(e) => showMessage(`Нажата клавиша: ${e.key}`, 800)}          // #5
        />

        <button
          onClick={async () => {
            const { data } = await getRecipes(searchText);
            setRecipes(data);
          }}                                                                      // #1
        >
          Поиск
        </button>
      </div>

      <AIRecipeGenerator
        onRecipeGenerated={(recipe) => {
          setForm({ title: recipe.title, category: recipe.category });
          setIngredients(recipe.ingredients);
          setSteps(recipe.steps);
        }}
      />

      <form onSubmit={handleCreate}>
        <input
          placeholder="Название рецепта"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          onFocus={() => showMessage("Вы начали вводить название")}              // #6
          onBlur={() => showMessage("Вы закончили ввод названия")}              // #7
        />

        <input
          placeholder="Категория"
          value={form.category}
          onChange={(e) => setForm({ ...form, category: e.target.value })}
        />

        <div>
          <h4>Ингредиенты</h4>
          <input
            placeholder="Новый ингредиент"
            value={ingredientInput}
            onChange={(e) => setIngredientInput(e.target.value)}
          />

          <button
            type="button"
            onClick={() => {
              if (ingredientInput.trim()) {
                setIngredients([...ingredients, ingredientInput.trim()]);
                setIngredientInput("");
              }
            }}
          >
            Добавить ингредиент
          </button>

          <ul>
            {ingredients.map((i, idx) => (
              <li key={idx}>
                {i}
                <button
                  type="button"
                  onClick={() =>
                    setIngredients(ingredients.filter((_, j) => j !== idx))
                  }
                >
                  Удалить
                </button>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h4>Шаги</h4>
          <input
            placeholder="Новый шаг"
            value={stepInput}
            onChange={(e) => setStepInput(e.target.value)}
          />

          <button
            type="button"
            onClick={() => {
              if (stepInput.trim()) {
                setSteps([...steps, stepInput.trim()]);
                setStepInput("");
              }
            }}
          >
            Добавить шаг
          </button>

          <ol>
            {steps.map((s, idx) => (
              <li key={idx}>
                {s}
                <button
                  type="button"
                  onClick={() => setSteps(steps.filter((_, j) => j !== idx))}
                >
                  Удалить
                </button>
              </li>
            ))}
          </ol>
        </div>

        <button type="submit">Создать рецепт</button>
      </form>

      <h3>Список рецептов</h3>

      <div className="recipe-list">
        {recipes.map((r) => (
          <div key={r._id} className="recipe-card">
            <h3>{r.title}</h3>
            <p>Категория: {r.category}</p>

            <div>
              <strong>Ингредиенты:</strong> {r.ingredients.join(", ")}
            </div>

            <div>
              <strong>Шаги:</strong> {r.steps.join(" ")}
            </div>

            <button
              onClick={async () => {
                await deleteRecipe(r._id);
                loadRecipes();
              }}
              style={{ color: "red" }}
            >
              Удалить
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecipeBook;
