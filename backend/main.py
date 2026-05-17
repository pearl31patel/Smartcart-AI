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
        "rice": "lb",
        "flour": "lb",
        "sugar": "lb",
        "chicken": "lb",
        "beef": "lb",
        "pork": "lb",
        "eggs": "count",
        "egg": "count",
        "water": "pack",
        "milk": "gallon",
        "bread": "loaf",
        "potato": "lb",
        "potatoes": "lb",
        "onion": "lb",
        "onions": "lb",
        "juice": "oz",
    }

    if len(words) >= 2 and words[-1].isdigit():
        number = words[-1]
        product = " ".join(words[:-1])

        if product in unit_rules:
            return f"{product} {number} {unit_rules[product]}"

    return text


def get_store_brand_hint(item_key: str, store: str):
    if "bread" in item_key:
        hints = {
            "Walmart": "Great Value",
            "Target": "Market Pantry Good & Gather",
            "Costco": "Kirkland",
            "Amazon Fresh": "Amazon Fresh",
        }
        return hints.get(store, "")

    return ""

def score_product_match(item_key: str, title: str, source: str, store: str):
    title_lower = title.lower()
    source_lower = source.lower()
    words = item_key.split()

    score = 0

    for word in words:
        if word in title_lower:
            score += 3

    store_sources = {
        "Walmart": ["walmart"],
        "Target": ["target"],
        "Costco": ["costco"],
        "Amazon Fresh": ["amazon", "amazon fresh"],
    }

    allowed_sources = store_sources.get(store, [])

    if allowed_sources and any(s in source_lower for s in allowed_sources):
        score += 10
    else:
        return -999

    bad_words = [
        "crumb",
        "crumbs",
        "crouton",
        "croutons",
        "panko",
        "stuffing",
        "powder",
        "candy",
        "toy",
        "decor",
        "holder",
        "container",
        "shirt",
        "poster",
        "book",
    ]

    for bad in bad_words:
        if bad in title_lower and bad not in item_key:
            score -= 20

    return score


async def fetch_serpapi_product(item: str, store: str, zip_code: str):
    if not SERP_API_KEY:
        return None

    item_key = normalize_grocery_query(item)
    rule = SEARCH_RULES.get(item_key)

    if rule:
        base_query = rule["query"]
        keywords = rule["keywords"]
        unit = rule["unit"]
    else:
        base_query = item_key
        keywords = item_key.split()
        unit = "custom"

    brand_hint = get_store_brand_hint(item_key, store)
    query = f"{base_query} {brand_hint} {store} grocery near {zip_code}"

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERP_API_KEY,
    }

    store_sources = {
        "Walmart": ["walmart"],
        "Target": ["target"],
        "Costco": ["costco"],
        "Amazon Fresh": ["amazon", "amazon fresh"],
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, params=params)
            data = response.json()

        results = data.get("shopping_results", [])
        valid_products = []

        for product in results[:30]:
            title = product.get("title", "")
            title_lower = title.lower()

            source = (
                product.get("source")
                or product.get("seller")
                or product.get("merchant")
                or ""
            )

            source_lower = source.lower()
            allowed_sources = store_sources.get(store, [])

            if allowed_sources and not any(
                allowed_source in source_lower for allowed_source in allowed_sources
            ):
                continue

            match_score = score_product_match(item_key, title, source, store)

            if match_score < 5:
                continue

            price = clean_price(product.get("price", ""))

            if price is None:
                continue

            valid_products.append(
                {
                    "store": store,
                    "seller": source,
                    "name": title,
                    "price": price,
                    "unit": unit,
                    "price_per_unit": round(price, 2),
                    "match_score": match_score,
                    "data_source": "real_api",
                    "image": product.get("thumbnail"),
                    "link": product.get("link")
                    or product.get("product_link")
                    or product.get("serpapi_product_api"),
                }
            )

        if not valid_products:
            return None

        valid_products.sort(key=lambda x: (-x["match_score"], x["price"]))
        return valid_products[0]

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
                "seller": cheapest.get("seller"),
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