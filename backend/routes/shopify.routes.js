import { Router } from 'express';
import {
  
  createProduct,
  UpdateInventory,
  getOrderData,
  getOrdersByProduct
} from '../controllers/shopify.controller.js';

const router = Router();

router.post('/create', createProduct);
router.post('/updateInventory',UpdateInventory);
router.get('/order',getOrderData );
router.post("/pord",getOrdersByProduct)

export default router;
