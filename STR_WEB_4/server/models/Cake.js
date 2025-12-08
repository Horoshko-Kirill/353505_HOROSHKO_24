const mongoose = require("mongoose");

const CakeSchema = new mongoose.Schema({
  name: { type: String, required: true },
  ingredients: [{ type: String, required: true }],
  price: { type: Number, required: true, min: 0 },
  customizationOptions: { type: [String], default: [] },
  image: { type: String, default: "/placeholder.png" }, 
  description: { type: String, default: "" },
}, { timestamps: true });

module.exports = mongoose.model("Cake", CakeSchema);
