import express from 'express';
import cors from 'cors';

import shopifyRouter from './routes/shopify.routes.js';
import webhookRouter from './routes/webhook.routes.js';
import agentRouter from './routes/agent.routes.js';
import financeRouter from './routes/fi.routes.js';
import verifyShopify from './middlewares/verifyShopify.js';
import errorHandler from './middlewares/errorHandler.js';

const app = express();

app.use(cors());
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true }));

app.get('/health', (req, res) => {
  res.json({ ok: true, service: 'express-backend' });
});

app.use('/shopify', verifyShopify, shopifyRouter);
app.use('/webhooks', webhookRouter);
app.use('/agents', agentRouter);
app.use('/finance', financeRouter);

app.use(errorHandler);

export default app;
