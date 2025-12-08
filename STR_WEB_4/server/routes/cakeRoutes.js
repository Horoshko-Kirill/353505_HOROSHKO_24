const express = require("express");
const router = express.Router();
const Cake = require("../models/Cake");
const { protect } = require("../middleware/authMiddleware");


router.get("/", async (req, res) => {
  try {
    const { search, sortBy, sortOrder } = req.query;

    const query = {};

    if (search) {
      query.name = { $regex: search, $options: "i" }; 
    }

    const sort = {};
    if (sortBy) {
      sort[sortBy] = sortOrder === "desc" ? -1 : 1;
    }

    const cakes = await Cake.find(query).sort(sort);

    res.json(cakes);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post("/", protect, async (req, res) => {
  try {
    const cake = await Cake.create(req.body);
    res.json(cake);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.get("/:id", async (req, res) => {
  try {
    const cake = await Cake.findById(req.params.id);
    if (!cake) return res.status(404).json({ error: "Cake not found" });
    res.json(cake);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.put("/:id", protect, async (req, res) => {
  try {
    const cake = await Cake.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
    });
    res.json(cake);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.delete("/:id", protect, async (req, res) => {
  try {
    await Cake.findByIdAndDelete(req.params.id);
    res.json({ message: "Cake deleted" });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

module.exports = router;
