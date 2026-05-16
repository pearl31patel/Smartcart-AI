from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx
import asyncio

load_dotenv()

app = FastAPI(title="SmartCart AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERP_API_KEY = os.getenv("SERP_API_KEY")


class GroceryRequest(BaseModel):
    items: list[str]
    budget: float | None = None
    zip_code: str | None = "33620"


SEARCH_RULES = {
    "milk": {
        "query": "whole milk 1 gallon",
        "keywords": ["milk"],
        "unit": "1 gallon",
    },
    "eggs": {
        "query": "large eggs 12 count",
        "keywords": ["eggs"],
        "unit": "12 count",
    },
    "bread": {
        "query": "white sandwich bread loaf",
        "keywords": ["bread"],
        "unit": "loaf",
    },
    "rice": {
        "query": "white rice 5 lb",
        "keywords": ["rice"],
        "unit": "5 lb",
    },
    "chicken": {
        "query": "chicken breast 1 lb",
        "keywords": ["chicken"],
        "unit": "1 lb",
    },
}


def clean_price(price_text: str):
    if not price_text:
        return None

    price_text = price_text.replace("$", "").replace(",", "").strip()

    try:
        return float(price_text)
    except ValueError:
        return None

def normalize_grocery_query(item: str):
    text = item.lower().strip()
    words = text.split()

    unit_rules = {
    # Dairy
    "milk": "gallon",
    "almond milk": "half gallon",
    "oat milk": "half gallon",
    "soy milk": "half gallon",
    "cream": "pint",
    "half and half": "quart",
    "yogurt": "oz",
    "cheese": "oz",
    "butter": "lb",
    "sour cream": "oz",
    "cottage cheese": "oz",

    # Eggs
    "egg": "count",
    "eggs": "count",

    # Meat / Seafood
    "chicken": "lb",
    "chicken breast": "lb",
    "chicken thighs": "lb",
    "ground beef": "lb",
    "beef": "lb",
    "steak": "lb",
    "pork": "lb",
    "bacon": "oz",
    "turkey": "lb",
    "ground turkey": "lb",
    "sausage": "oz",
    "salmon": "lb",
    "shrimp": "lb",
    "tilapia": "lb",
    "fish": "lb",

    # Grains / Pantry
    "rice": "lb",
    "white rice": "lb",
    "brown rice": "lb",
    "flour": "lb",
    "sugar": "lb",
    "brown sugar": "lb",
    "pasta": "oz",
    "spaghetti": "oz",
    "macaroni": "oz",
    "noodles": "oz",
    "oats": "oz",
    "cereal": "oz",
    "bread": "loaf",
    "bagels": "count",
    "tortillas": "count",
    "english muffins": "count",

    # Produce
    "apple": "lb",
    "apples": "lb",
    "banana": "lb",
    "bananas": "lb",
    "orange": "lb",
    "oranges": "lb",
    "grapes": "lb",
    "strawberries": "lb",
    "blueberries": "oz",
    "avocado": "count",
    "avocados": "count",
    "potato": "lb",
    "potatoes": "lb",
    "onion": "lb",
    "onions": "lb",
    "tomato": "lb",
    "tomatoes": "lb",
    "carrot": "lb",
    "carrots": "lb",
    "lettuce": "head",
    "spinach": "oz",
    "broccoli": "lb",
    "cucumber": "count",
    "cucumbers": "count",
    "bell pepper": "count",
    "bell peppers": "count",

    # Canned / Jar
    "beans": "oz",
    "black beans": "oz",
    "kidney beans": "oz",
    "corn": "oz",
    "tuna": "oz",
    "soup": "oz",
    "pasta sauce": "oz",
    "peanut butter": "oz",
    "jam": "oz",
    "jelly": "oz",

    # Frozen
    "frozen pizza": "count",
    "frozen vegetables": "oz",
    "frozen fruit": "oz",
    "ice cream": "oz",

    # Drinks
    "water": "pack",
    "sparkling water": "pack",
    "soda": "pack",
    "juice": "oz",
    "coffee": "oz",
    "tea": "count",

    # Snacks
    "chips": "oz",
    "cookies": "oz",
    "crackers": "oz",
    "granola bars": "count",
    "popcorn": "oz",

    # Household
    "toilet paper": "rolls",
    "paper towels": "rolls",
    "trash bags": "count",
    "laundry detergent": "fl oz",
    "dish soap": "fl oz",
    "hand soap": "fl oz",
    "shampoo": "fl oz",
    "conditioner": "fl oz",
    "toothpaste": "oz",
}

    if len(words) >= 2 and words[-1].isdigit():
        number = words[-1]
        product = " ".join(words[:-1])

        if product in unit_rules:
            return f"{product} {number} {unit_rules[product]}"

    return text

async def fetch_serpapi_product(item: str, store: str, zip_code: str):
    if not SERP_API_KEY:
        return None

    item_key = normalize_grocery_query(item)
    rule = SEARCH_RULES.get(item_key)

    if rule:
        query = f'{rule["query"]} {store} near {zip_code}'
        keywords = rule["keywords"]
        unit = rule["unit"]
    else:
        query = f"{item_key} {store} grocery near {zip_code}"
        keywords = item_key.split()
        unit = "custom"

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERP_API_KEY,
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, params=params)
            data = response.json()

        results = data.get("shopping_results", [])

        for product in results[:10]:
            title = product.get("title", "")
            title_lower = title.lower()

            matched_words = sum(1 for keyword in keywords if keyword.lower() in title_lower)

            if matched_words == 0:
                continue

            price = clean_price(product.get("price", ""))

            if price is None:
                continue

            return {
                "store": store,
                "name": title,
                "price": price,
                "unit": unit,
                "price_per_unit": round(price, 2),
                "data_source": "real_api",
                "image": product.get("thumbnail"),
                "link": product.get("link") or product.get("product_link") or product.get("serpapi_product_api"),
            }

        return None

    except Exception as error:
        print(f"Error fetching {item} from {store}: {error}")
        return None


async def get_prices_for_item(item: str, zip_code: str):
    stores = ["Walmart", "Target", "Costco", "Amazon Fresh"]

    tasks = [fetch_serpapi_product(item, store, zip_code) for store in stores]
    results = await asyncio.gather(*tasks)

    return [result for result in results if result]


@app.get("/")
def home():
    return {
        "message": "SmartCart AI backend is running",
        "data_mode": "real_api_only",
    }


@app.post("/compare")
async def compare_groceries(request: GroceryRequest):
    final_results = []
    cheapest_plan = []
    total_cost = 0

    for item in request.items:
        prices = await get_prices_for_item(item, request.zip_code)

        if not prices:
            final_results.append(
                {
                    "item": item,
                    "prices": [],
                    "cheapest": None,
                    "message": "No reliable real data found for this item.",
                }
            )
            continue

        cheapest = min(prices, key=lambda x: x["price"])

        final_results.append(
            {
                "item": item,
                "prices": prices,
                "cheapest": cheapest,
            }
        )

        cheapest_plan.append(
            {
                "item": item,
                "store": cheapest["store"],
                "name": cheapest["name"],
                "price": cheapest["price"],
                "unit": cheapest["unit"],
                "data_source": cheapest["data_source"],
                "image": cheapest["image"],
                "link": cheapest["link"],
            }
        )

        total_cost += cheapest["price"]

    budget_message = "No budget added."

    if request.budget:
        if total_cost <= request.budget:
            budget_message = f"Your cart is under budget by ${round(request.budget - total_cost, 2)}."
        else:
            budget_message = f"Your cart is over budget by ${round(total_cost - request.budget, 2)}."

    return {
        "zip_code": request.zip_code,
        "results": final_results,
        "cheapest_plan": cheapest_plan,
        "total_cost": round(total_cost, 2),
        "budget_message": budget_message,
        "note": "Only real API results are used. No mock data is included.",
    }