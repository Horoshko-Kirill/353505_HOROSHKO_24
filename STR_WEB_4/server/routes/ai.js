const express = require("express");
const router = express.Router();
const axios = require("axios");

const API_KEY = "Dwr_d49782447d22cec05069b3c704b50ca276e5f01bc8c1999b1178894bb651a742";
const ASSISTANT_ID = 1765158462;

router.post("/generate-recipe", async (req, res) => {
  const prompt = `Придумай десертный рецепт. Верни строго JSON, без текста вокруг: 
{
  "title": "...",
  "category": "dessert",
  "ingredients": ["..."],
  "steps": ["..."]
}`;

  try {
    const response = await axios.post(
      `https://dewiar.com/dew_ai/api?key=${API_KEY}`,
      {
        data: {
          message: prompt,
          image: "",
          idb: ASSISTANT_ID,
          session_id: "",
          midnight_clear: "yes"
        }
      },
      { headers: { "Content-Type": "application/json" } }
    );

    let text = response.data.response;

    text = text.replace(/^```json/, "").replace(/```$/, "").trim();

    const recipe = JSON.parse(text);

    res.json(recipe);

  } catch (err) {
    console.error("Ошибка AI:", err.response?.data || err.message);
    res.status(500).json({ error: "Ошибка генерации рецепта" });
  }
});

module.exports = router;
