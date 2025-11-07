import fastapiService from '../services/fastapi.service.js';

export async function triggerCoordinator(req, res, next) {
  try {
    const result = await fastapiService.runCoordinator(req.body);
    res.json(result);
  } catch (error) {
    next(error);
  }
}

export async function runPricingAgent(req, res, next) {
  try {
    const result = await fastapiService.runPricingAgent(req.body);
    res.json(result);
  } catch (error) {
    next(error);
  }
}

export async function fetchAnalyticsSummary(req, res, next) {
  try {
    const summary = await fastapiService.fetchAnalyticsSummary();
    res.json(summary);
  } catch (error) {
    next(error);
  }
}
