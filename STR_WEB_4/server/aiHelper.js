const axios = require("axios");
async function sendToAssistant(message, session_id = "") {
  const url = `https://dewiar.com/dew_ai/api?key=${API_KEY}`;
  const data = {
    data: {
      message,
      image: "",
      idb: ASSISTANT_ID,
      session_id,
      midnight_clear: "yes"
    }
  };

  const response = await axios.post(url, data, {
    headers: { "Content-Type": "application/json" }
  });

  if (response.data.reaction === "ok") {
    return response.data;
  } else {
    throw new Error(response.data.response || "Ошибка ассистента");
  }
}

module.exports = { sendToAssistant };
