import { Router } from 'express';
import {
  getFinanceSnapshot,
  reconcilePayouts,
} from '../controllers/fi.controller.js';

const router = Router();

router.get('/snapshot', getFinanceSnapshot);
router.post('/payouts/reconcile', reconcilePayouts);

export default router;
