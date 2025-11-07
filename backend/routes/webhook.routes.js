import { Router } from 'express';
import {
  handleOrderWebhook,
  handleProductWebhook,
} from '../controllers/webhook.controller.js';

const router = Router();

router.post('/orders', handleOrderWebhook);
router.post('/products', handleProductWebhook);

export default router;
