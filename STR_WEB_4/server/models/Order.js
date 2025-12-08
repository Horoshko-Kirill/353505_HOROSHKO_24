const mongoose = require("mongoose");

const OrderSchema = new mongoose.Schema({
  customerName: { type: String, required: true },
  cakeId: { type: mongoose.Schema.Types.ObjectId, ref: "Cake", required: true },
  address: { type: String, required: true },
  deliveryDate: { type: Date, required: true },
  status: { type: String, enum: ["pending", "delivered", "cancelled"], default: "pending" }
}, { timestamps: true });

module.exports = mongoose.model("Order", OrderSchema);
