import { createServer } from 'http';
import dotenv from 'dotenv';
import app from './app.js';
import logger from './services/logger.service.js';

dotenv.config();

const PORT = process.env.PORT || 4000;

const server = createServer(app);

server.listen(PORT, () => {
  console.log(`Express layer listening on port ${PORT}`);
});

