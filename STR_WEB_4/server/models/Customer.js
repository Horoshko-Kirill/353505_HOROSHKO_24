const mongoose = require("mongoose");

const CustomerSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { 
    type: String, 
    required: true, 
    unique: true, 
    match: /.+\@.+\..+/ 
  },
  phone: { type: String },
  totalSpent: { type: Number, default: 0 },
  avatar: { type: String, default: "/avatar-placeholder.png" } // путь к фото
}, { timestamps: true });

module.exports = mongoose.model("Customer", CustomerSchema);
