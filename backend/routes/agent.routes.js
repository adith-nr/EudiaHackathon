import { Router } from 'express';
import {
  triggerCoordinator,
  runPricingAgent,
  fetchAnalyticsSummary,
} from '../controllers/agent.controller.js';

const router = Router();

router.post('/coordinator/run', triggerCoordinator);
router.post('/pricing/run', runPricingAgent);
router.get('/analytics/summary', fetchAnalyticsSummary);

export default router;
