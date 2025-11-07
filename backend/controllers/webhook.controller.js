import webhookService from '../services/shopify.service.js';
import fastapiService from '../services/fastapi.service.js';

export async function handleOrderWebhook(req, res, next) {
  try {
    await webhookService.handleOrderEvent(req.body);
    await fastapiService.enqueueAnalyticsJob('order', req.body);
    res.status(200).json({ received: true });
  } catch (error) {
    next(error);
  }
}

export async function handleProductWebhook(req, res, next) {
  try {
    await webhookService.handleProductEvent(req.body);
    res.status(200).json({ received: true });
  } catch (error) {
    next(error);
  }
}
