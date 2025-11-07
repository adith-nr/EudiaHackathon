from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv

from utils import clean_data

app = FastAPI()

load_dotenv()


# Load Shopify credentials from environment variables
SHOPIFY_STORE = os.getenv("SHOPIFY_STORE")  # e.g. mystore
SHOPIFY_TOKEN = os.getenv("ACCESS_TOKEN")  # Admin access token
API_VERSION = "2024-10"

@app.on_event("startup")
async def startup_event():
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "4000")
    print(f"\n🚀 FastAPI server running at: http://{host}:{port}")
    print(f"🛍️  Shopify store: {SHOPIFY_STORE or 'Not set'}\n")

@app.get("/")
def root():
    return {"message": "Shopify Analytics API is running 🚀"}

@app.get("/analytics")
def get_products(limit: int = 10):
    """
    Fetch products from Shopify Admin API.
    Example: GET /analytics?limit=5
    """

    print(SHOPIFY_STORE, SHOPIFY_TOKEN)

    if not SHOPIFY_STORE or not SHOPIFY_TOKEN:
        raise HTTPException(status_code=400, detail="Missing Shopify credentials in environment")

    # Handle both formats: "store-name" or "store-name.myshopify.com"
    if SHOPIFY_STORE.endswith('.myshopify.com'):
        shopify_domain = SHOPIFY_STORE
    else:
        shopify_domain = f"{SHOPIFY_STORE}.myshopify.com"
    
    url = f"https://{shopify_domain}/admin/api/{API_VERSION}/.json"

    headers = {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params={"limit": limit})
        response.raise_for_status()
        data = response.json()

        products = [
            {
                "id": p["id"],
                "title": p["name"],
                "vendor": p.get("vendor"),
                "price": p["totalPrice"],
                "created_at": p.get("createdAt")
            }
            for p in data['recentOrders']
        ]

            
        res_data = clean_data(products)

        return {"count": len(res_data), "data": res_data}

    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail=str(e))
