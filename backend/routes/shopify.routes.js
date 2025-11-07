import { Router } from 'express';
import {
  listProducts,
  syncInventory,
  createPriceExperiment,
  createProduct,
  UpdateInventory,
  getOrderData
} from '../controllers/shopify.controller.js';

const router = Router();

router.get('/createProduct', createProduct);
router.post('/inventory',UpdateInventory);
router.post('/order',getOrderData );

export default router;
