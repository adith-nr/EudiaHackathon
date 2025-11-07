import shopifyService from '../services/shopify.service.js';
import fastapiService from '../services/fastapi.service.js';

export async function listProducts(req, res, next) {
  try {
    const products = await shopifyService.fetchProducts();
    res.json({ products });
  } catch (error) {
    next(error);
  }
}

export async function syncInventory(req, res, next) {
  try {
    const result = await shopifyService.syncInventoryWithCache();
    res.json({ message: 'Inventory syncing queued', result });
  } catch (error) {
    next(error);
  }
}

export async function createPriceExperiment(req, res, next) {
  try {
    const payload = req.body;
    const validated = fastapiService.validateAgentPayload(payload);
    const job = await fastapiService.dispatchPricingExperiment(validated);
    res.status(202).json({ jobId: job.id, status: 'queued' });
  } catch (error) {
    next(error);
  }
}
