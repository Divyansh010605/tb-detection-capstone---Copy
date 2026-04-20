const express  = require('express');
const router   = express.Router();
const { protect } = require('../middlewares/auth');   // your existing JWT middleware
const {
  getHistory,
  getReport,
} = require('../controllers/historyController');

// GET /api/history  — paginated scan history for the logged-in user
router.get('/',         protect, getHistory);

// GET /api/history/:id/report  — stream a PDF diagnostic report
router.get('/:id/report', protect, getReport);

module.exports = router;