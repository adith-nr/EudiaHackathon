
export async function handleOrderWebhook(req, res, next) {
  try {
    
    
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
