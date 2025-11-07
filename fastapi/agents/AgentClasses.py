import os
import pandas
import json
import re
import statistics
from typing import List, Dict, Any, Optional
# from serpapi import GoogleSearch
import google.generativeai as genai


test_data = ''
#api call should  me made here to fetch similiar products detail in here 
# with open('test_pricing_data.json', "r") as file:
#     test_data = json.load(file) 

class PricingAgent:
    def __init__(self, serpapi_key: str = None, gemini_api_key: str = None):
        self.serpapi_key = serpapi_key or os.getenv(
            "SERPAPI_KEY", 
            "bb0eb596ffef3937f1f85387229f771b8286763d335d95b49d2db212ecfa00da"
        )
        self.gemini_api_key = "AIzaSyB14qOB70MyIgv2EI91KDWfunJlXZKE3YU" or os.getenv("GEMINI_API_KEY")
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel("gemini-2.5-flash")
        else:
            self.gemini_model = None
        
    
    def scrape_amazon_products(
        self, 
        product_name: str, 
        max_results: int = 10,
    ) -> List[Dict[str, Any]]:
    
        params = {
            "engine": "amazon",
            "k": product_name,
            "amazon_domain": "amazon.in",
            "api_key": self.serpapi_key
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            products = []

            for item in results.get("organic_results", [])[:max_results]:
                product = {
                    "title": item.get("title"),
                    "price": item.get("price"),
                    "rating": item.get("rating"),
                    "reviews": item.get("reviews"),
                    "description": ", ".join(item.get("tags", [])) if item.get("tags") else None,
                    "url": item.get("link_clean") or item.get("link"),
                    "thumbnail": item.get("thumbnail"),
                }
                products.append(product)

            return products
            
        except Exception as e:
            print(f"Error scraping Amazon: {str(e)}")
            return []
    
    def extract_price_value(self, price_str: Optional[str]) -> Optional[float]:
        if not price_str:
            return None
        
        # print("ENtered extract price value with:", price_str)
        
        try:
            price_match = re.search(r'[\d,]+\.?\d*', str(price_str))
            if price_match:
                price_clean = price_match.group().replace(',', '')
                return float(price_clean)
        except Exception as e:
            print(f"Error extracting price from '{price_str}': {e}")
            return None
        
        return None
    
    def analyze_market_prices(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        prices = []
        
        # print("Analyzing market prices for products:", products)
        for product in products:
            price_val = self.extract_price_value(product.get("price"))
            if price_val:
                prices.append(price_val)
        
        if not prices:
            return {
                "min_price": None,
                "max_price": None,
                "avg_price": None,
                "median_price": None,
                "total_products": len(products),
                "products_with_price": 0,
                "price_distribution": {"low": [], "medium": [], "high": []}
            }
        
        median_price = statistics.median(prices)
        
        return {
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": round(sum(prices) / len(prices), 2),
            "median_price": median_price,
            "total_products": len(products),
            "products_with_price": len(prices),
            "price_distribution": {
                "low": [p for p in prices if p < median_price * 0.8],
                "medium": [p for p in prices if median_price * 0.8 <= p <= median_price * 1.2],
                "high": [p for p in prices if p > median_price * 1.2]
            }
        }
    
    def generate_pricing_recommendation(
        self,
        product_name: str,
        user_price_range: Dict[str, float],
        market_data: Dict[str, Any],
        products: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        # Check if Gemini model is configured
        if not self.gemini_model:
            raise ValueError(
                "Gemini API key not configured."
            )
        
        # Prepare context for Gemini
        context = self._build_llm_context(
            product_name, user_price_range, market_data, products
        )
        # print("LLM Context:", context)
        
        # Generate response using Gemini 
        response = self.gemini_model.generate_content(
            context,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                response_mime_type="application/json",
            )
        )
        
        # Parse JSON response
        recommendation = json.loads(response.text)
        
        # Add metadata
        recommendation["product_name"] = product_name
        recommendation["user_price_range"] = user_price_range
        recommendation["market_data"] = market_data
        recommendation["llm_powered"] = True
        recommendation["llm_model"] = "gemini-2.0-flash-exp"
        
        return recommendation
    
    def _build_llm_context(
        self,
        product_name: str,
        user_price_range: Dict[str, float],
        market_data: Dict[str, Any],
        products: List[Dict[str, Any]]
    ) -> str:
        
        context = f"""
            Analyze the following market data and provide pricing recommendations.

            **Product:** {product_name}
            **User's Price Range:** ₹{user_price_range.get('min', 0):,.2f} - ₹{user_price_range.get('max', 0):,.2f}

            **Market Analysis:**
            - Competitor Price Range: ₹{market_data.get('min_price', 0):,.2f} - ₹{market_data.get('max_price', 0):,.2f}
            - Average Market Price: ₹{market_data.get('avg_price', 0):,.2f}
            - Median Market Price: ₹{market_data.get('median_price', 0):,.2f}
            - Total Competitors Analyzed: {market_data.get('products_with_price', 0)}

            **Top 5 Competitor Products:**
        """
        
        # Add top 5 competitor details
        for i, product in enumerate(products[:5], 1):
            title = product.get('title', 'Unknown')[:80]  # Truncate long titles
            price = product.get('price', 'N/A')
            rating = product.get('rating', 'N/A')
            reviews = product.get('reviews', 'N/A')
            context += f"{i}. {title}\n   Price: {price} | Rating: {rating} | Reviews: {reviews}\n"
        
        context += """

        **Instructions:**
        You are an expert e-commerce pricing strategist. Analyze the market data and provide pricing recommendations.

        **Required Analysis:**
        Provide pricing recommendations with the following fields:
        1. **recommended_price**: Optimal price (number, prefer within user's range)
        2. **min_competitive_price**: Minimum viable competitive price (number)
        3. **max_premium_price**: Maximum price for premium positioning (number)
        4. **strategy**: One of ["value", "competitive", "premium", "penetration"]
        5. **reasoning**: Detailed explanation (2-3 sentences)
        6. **risk_level**: One of ["low", "medium", "high"]
        7. **market_position**: Brief description of positioning

        **IMPORTANT:** Return ONLY valid JSON, no markdown or explanation. Use this exact format:
        {
            "recommended_price": 1149,
            "min_competitive_price": 999,
            "max_premium_price": 1799,
            "strategy": "competitive",
            "reasoning": "Based on market analysis...",
            "risk_level": "low",
            "market_position": "competitive_pricing"
        }
        """
        return context
    
    def run_pricing_analysis(
        self,
        product_name: str,
        price_range: Dict[str, float],
        max_competitors: int = 10,
        save_output: bool = False
    ) -> Dict[str, Any]:
        
        #Scrape competitor products
        # products = self.scrape_amazon_products(
        #     product_name, 
        #     max_results=max_competitors
        # )
        products = test_data
        
        if not products:
            return {
                "status": "error",
                "message": "Failed to scrape competitor data",
                "product_name": product_name,
                "user_price_range": price_range
            }
        
        # Analyze market data
        market_data = self.analyze_market_prices(products)
        print(market_data)
        
        #Generate AI recommendations
        try:
            recommendations = self.generate_pricing_recommendation(
                product_name,
                price_range,
                market_data,
                products
            )
        except ValueError as e:
            # Gemini API key not configured
            return {
                "status": "error",
                "error_type": "configuration_error",
                "message": str(e),
                "product_name": product_name,
                "user_price_range": price_range,
                "market_analysis": market_data,
                "competitor_products": products[:5]
            }
        except Exception as e:
            # LLM generation failed
            return {
                "status": "error",
                "error_type": "llm_generation_error",
                "message": f"Failed to generate pricing recommendations: {str(e)}",
                "product_name": product_name,
                "user_price_range": price_range,
                "market_analysis": market_data,
                "competitor_products": products[:5]
            }
        
        result = {
            "status": "success",
            "product_name": product_name,
            "user_price_range": price_range,
            "market_analysis": market_data,
            "recommendations": recommendations,
            "competitor_products": products[:5],  # Return top 5 for reference
            "total_competitors_analyzed": len(products)
        }
        
        
        return result
    def get_recommended_price(
            self,
            product_name: str,
            price_range: Dict[str, float],
            max_competitors: int = 10
        ) -> Optional[float]:
            """
            Runs full pricing pipeline and returns the final recommended price.
            """
            print(f"🔍 Running pricing analysis for: {product_name}")
            result = self.run_pricing_analysis(
                product_name=product_name,
                price_range=price_range,
                max_competitors=max_competitors
            )

            if result.get("status") != "success":
                print(f"❌ Pricing analysis failed: {result.get('message')}")
                return None

            recommendations = result.get("recommendations", {})
            recommended_price = recommendations.get("recommended_price")

            if not recommended_price:
                print("⚠️ No recommended price returned by model.")
                return None

            print(f"✅ Recommended price for '{product_name}': ₹{recommended_price}")
            return recommended_price
