const express  = require('express');
const router   = express.Router();
const { protect } = require('../middlewares/auth');
const { getAnalytics } = require('../controllers/analyticsController');

// GET /api/analytics?range=30d
router.get('/', protect, getAnalytics);

module.exports = router;