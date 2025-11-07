import financeService from '../services/fi.service.js';

export async function getFinanceSnapshot(req, res, next) {
  try {
    const snapshot = await financeService.buildSnapshot();
    res.json(snapshot);
  } catch (error) {
    next(error);
  }
}

export async function reconcilePayouts(req, res, next) {
  try {
    const result = await financeService.reconcilePayouts(req.body);
    res.json(result);
  } catch (error) {
    next(error);
  }
}
