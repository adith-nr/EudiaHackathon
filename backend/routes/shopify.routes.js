import { Router } from 'express';
import {
  listProducts,
  syncInventory,
  createPriceExperiment,
} from '../controllers/shopify.controller.js';

const router = Router();

router.get('/products', listProducts);
router.post('/inventory/sync', syncInventory);
router.post('/pricing/experiments', createPriceExperiment);

export default router;
