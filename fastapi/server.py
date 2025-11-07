from fastapi import FastAPI, HTTPException
import requests
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

from agents.AgentClasses import *

from agents.utils import clean_data

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

@app.get("/products_analyze")
def products_analyze(responce):
    # agent = PricingAgent()
    product_name = "Diwali Lights String Lights 20 Meters"
    price_range = {"min": 900, "max": 1500}

    print(responce)
    
    # recommended_price = agent.get_recommended_price(product_name, price_range)

    # if recommended_price:
    #     print("💰 Final price to use for listing:", recommended_price)
    #     # 🔧 Next: call your Express `/create-listing` route here
    # else:
    #     print("❌ Failed to get a recommended price.")