import os
import pandas
import json
import re
import statistics
from typing import List, Dict, Any, Optional
# from serpapi import GoogleSearch
import google.generativeai as genai


from AgentClasses import *


if __name__ == "__main__":
    agent = PricingAgent()

    product_name = "Diwali Lights String Lights 20 Meters"
    price_range = {"min": 900, "max": 1500}
    
    recommended_price = agent.get_recommended_price(product_name, price_range)

    if recommended_price:
        print("💰 Final price to use for listing:", recommended_price)
        # 🔧 Next: call your Express `/create-listing` route here
    else:
        print("❌ Failed to get a recommended price.")
    
   
