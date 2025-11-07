from fastapi import FastAPI, HTTPException
import requests
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from pydantic import BaseModel
from agents.AgentClasses import *

from agents.utils import clean_data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # or ["http://localhost:5173"] for React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class ProductInput(BaseModel):
    name: str
    description: str
    minPrice: float
    maxPrice: float

@app.post("/products_analyze")
async def products_analyze(data: ProductInput):
    print("📦 Received:", data.dict())
    avg_price = (data.minPrice + data.maxPrice) / 2
    agent=PricingAgent()
    recommended_price = agent.get_recommended_price(data.name, {"min":data.minPrice,"max":data.maxPrice})
    print(recommended_price)

    return {
        "message": "Product analyzed successfully",
        "product_name": data.name,
        "recommended_price": round(avg_price, 2),
    }