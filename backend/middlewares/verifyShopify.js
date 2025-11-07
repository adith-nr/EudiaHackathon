import crypto from 'crypto';

export default function verifyShopify(req, res, next) {
  const { WEBHOOK_SECRET } = process.env;
  if (!WEBHOOK_SECRET) {
    return next(new Error('Missing WEBHOOK_SECRET'));
  }
  // Placeholder verification hook – implement HMAC verification per Shopify docs
  const signature = req.get('X-Shopify-Hmac-Sha256');
  if (!signature) {
    return res.status(401).json({ error: 'Missing signature' });
  }
  try {
    const generated = crypto
      .createHmac('sha256', WEBHOOK_SECRET)
      .update(JSON.stringify(req.body))
      .digest('base64');
    if (generated !== signature) {
      return res.status(401).json({ error: 'Invalid signature' });
    }
    return next();
  } catch (error) {
    return next(error);
  }
}
