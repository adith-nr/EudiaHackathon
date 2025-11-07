import axios from 'axios';
import crypto from 'crypto';
import { agentPayloadSchema } from '../utils/schema.js';
import logger from './logger.service.js';

const fastapiClient = axios.create({
  baseURL: process.env.FASTAPI_BASE_URL || 'http://localhost:8000',
  timeout: 5000,
});

function validateAgentPayload(payload) {
  return agentPayloadSchema.parse(payload);
}

async function dispatchPricingExperiment(payload) {
  logger.info('Dispatching pricing experiment to FastAPI');
  return { id: crypto.randomUUID(), payload };
}

async function enqueueAnalyticsJob(topic, data) {
  logger.info(`Enqueue analytics job for ${topic}`);
  await fastapiClient.post('/analytics/enqueue', { topic, data });
}

async function runCoordinator(payload) {
  const { data } = await fastapiClient.post('/coordinator/run', payload);
  return data;
}

async function runPricingAgent(payload) {
  const { data } = await fastapiClient.post('/pricing/run', payload);
  return data;
}

async function fetchAnalyticsSummary() {
  const { data } = await fastapiClient.get('/insight/summary');
  return data;
}

export default {
  validateAgentPayload,
  dispatchPricingExperiment,
  enqueueAnalyticsJob,
  runCoordinator,
  runPricingAgent,
  fetchAnalyticsSummary,
};
