import logger from '../services/logger.service.js';

export default function errorHandler(err, req, res, next) {
  logger.error('Express request failed', { err });
  if (res.headersSent) {
    return next(err);
  }
  res.status(err.status || 500).json({
    message: err.message || 'Internal server error',
  });
}
