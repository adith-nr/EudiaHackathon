import logger from './logger.service.js';

async function buildSnapshot() {
  logger.info('Building finance snapshot from FastAPI data');
  return { cashFlow: 0, runwayDays: 0 };
}

async function reconcilePayouts(payload) {
  logger.info('Reconciling payouts', payload);
  return { reconciled: true };
}

export default {
  buildSnapshot,
  reconcilePayouts,
};
