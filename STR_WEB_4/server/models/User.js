const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String },
  googleId: { type: String },
  createdAt: { type: Date, default: Date.now },
});

userSchema.methods.matchPassword = async function (entered) {
  if (!this.password) return false; 
  return await bcrypt.compare(entered, this.password);
};


module.exports = mongoose.model("User", userSchema);
