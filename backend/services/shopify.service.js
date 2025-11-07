import axios from 'axios';
import logger from './logger.service.js';

const SHOPIFY_BASE_URL = `https://${process.env.SHOPIFY_STORE_DOMAIN}/admin/api/2024-04`;

async function fetchProducts() {
  logger.info('Fetching products from Shopify');
  await axios.get(`${SHOPIFY_BASE_URL}/products.json`, {
    headers: {
      'X-Shopify-Access-Token': process.env.SHOPIFY_API_SECRET,
    },
  });
  return [];
}

async function syncInventoryWithCache() {
  logger.info('Syncing inventory with FastAPI cache');
  return { status: 'queued' };
}

async function handleOrderEvent(payload) {
  logger.info('Handling Shopify order webhook');
  return payload;
}

async function handleProductEvent(payload) {
  logger.info('Handling Shopify product webhook');
  return payload;
}

export default {
  fetchProducts,
  syncInventoryWithCache,
  handleOrderEvent,
  handleProductEvent,
};
