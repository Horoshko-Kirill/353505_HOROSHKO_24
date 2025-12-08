require("dotenv").config();
const express = require("express");
const cors = require("cors");
const uploadRoutes = require("./routes/uploadRoutes");

const connectDB = require("./config/db");
connectDB();

const passport = require("passport");
require("./config/passport");

const newsRoutes = require("./routes/newsRoute");
const aiRoutes = require("./routes/ai");

const app = express();
app.use(cors());
app.use(express.json());
app.use(passport.initialize());

app.use("/api/auth", require("./routes/authRoutes"));
app.use("/api/cakes", require("./routes/cakeRoutes"));
app.use("/api/orders", require("./routes/orderRoutes"));
app.use("/api/recipes", require("./routes/recipeRoutes"));
app.use("/api/customers", require("./routes/customerRoutes"));
app.use("/api/upload", uploadRoutes);
app.use("/uploads", express.static("uploads"));
app.use("/api/news", newsRoutes);
app.use(express.json());
app.use("/api", aiRoutes);

app.listen(5000, () => console.log("Server started on port 5000"));
