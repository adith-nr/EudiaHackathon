export function sanitizeShopId(id) {
  return String(id || '').replace(/[^a-zA-Z0-9-_]/g, '');
}

export function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
