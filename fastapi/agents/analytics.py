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
    
    # Correct endpoint for Shopify orders
    url = f"https://{shopify_domain}/admin/api/{API_VERSION}/orders.json"

    headers = {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params={"limit": limit})
        response.raise_for_status()
        data = response.json()

        # Check if we have orders in the response
        if 'orders' not in data or not data['orders']:
            return {
                "status": "success",
                "total_orders": 0,
                "total_revenue": 0,
                "average_order_value": 0,
                "currency": "USD",
                "orders": [],
                "message": "No orders found"
            }

        # Organize the data from Shopify orders
        products = []
        for order in data['orders']:
            # Get the first line item for simplicity, or you can aggregate all line items
            if order.get('line_items'):
                for item in order['line_items']:
                    products.append({
                        "id": order["id"],
                        "order_name": order.get("name", ""),
                        "title": item.get("title", ""),
                        "vendor": item.get("vendor"),
                        "price": float(item.get("price", 0)),
                        "quantity": item.get("quantity", 1),
                        "total_price": float(order.get("total_price", 0)),
                        "created_at": order.get("created_at")
                    })

        # Convert to pandas DataFrame for analytics
        import pandas as pd
        
        df = pd.DataFrame(products)
        
        # Convert price columns to numeric for calculations
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce')
        
        # Group by order id and aggregate
        order_analytics = df.groupby('id').agg({
            'order_name': 'first',
            'title': lambda x: ', '.join(x.astype(str)),  # Combine all product titles
            'vendor': 'first',
            'total_price': 'first',  # Use the order total price
            'created_at': 'first'
        }).reset_index()
        
        # Calculate overall analytics
        total_orders = len(order_analytics)
        total_revenue = order_analytics['total_price'].sum()
        average_order_value = order_analytics['total_price'].mean() if total_orders > 0 else 0
        
        # Convert DataFrame to JSON format
        orders_data = order_analytics.to_dict('records')
        
        # Get currency from first order
        currency = data['orders'][0].get('currency', 'USD') if data.get('orders') else 'USD'
        
        # Prepare final analytics response
        analytics_response = {
            "status": "success",
            "total_orders": total_orders,
            "total_revenue": round(total_revenue, 2),
            "average_order_value": round(average_order_value, 2),
            "currency": currency,
            "orders": orders_data
        }
        
        return analytics_response

    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail=str(e))
