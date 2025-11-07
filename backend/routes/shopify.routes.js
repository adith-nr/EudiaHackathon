import { Router } from 'express';
import {
  
  createProduct,
  UpdateInventory,
  getOrderData,
  getOrdersByProduct,
  getProducts
} from '../controllers/shopify.controller.js';

const router = Router();

router.post('/create', createProduct)
router.post('/updateInventory',UpdateInventory)
router.get('/order',getOrderData )
router.post("/pord",getOrdersByProduct)
router.get("/products",getProducts)

export default router;
