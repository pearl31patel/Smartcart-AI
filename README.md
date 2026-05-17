# 🛒 SmartCart AI

SmartCart AI is an AI-powered grocery comparison platform that helps users find the cheapest shopping plan across multiple stores like Walmart, Target, Costco, and Amazon Fresh.

The app compares real grocery prices using live shopping data and recommends the best store for each product based on price and product matching.

---

API Docs:  
https://smartcart-ai-11vj.onrender.com/docs

---

# ✨ Features

- Compare grocery prices across multiple stores
- AI-powered product matching
- Budget tracking
- Real-time shopping data using SerpAPI
- Finds cheapest shopping plan automatically
- Product image and direct product links
- Smart filtering for unrelated products
- Responsive modern UI

---

# 🧠 AI Features

SmartCart AI uses AI-inspired product matching logic to:

- Understand grocery search intent
- Match similar products across stores
- Filter unrelated products
- Remove incorrect product categories
- Recommend cheapest valid product
- Normalize grocery queries automatically

Examples:
- `"eggs 18"` → finds 18 count eggs
- `"white bread"` → avoids breadcrumbs
- `"rice 20"` → understands 20 lb rice

---

# 🛠️ Tech Stack

## Frontend
- React.js
- Tailwind CSS
- Framer Motion
- Axios

## Backend
- FastAPI
- Python
- Async HTTP Requests
- SerpAPI

## Deployment
- Netlify (Frontend)
- Render (Backend)

---

# 📂 Project Structure

```bash
SMARTCART-AI/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

---

# ⚙️ Backend Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/pearl31patel/Smartcart-AI.git
cd Smartcart-AI
```

---

## 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Add Environment Variables

Create `.env` file inside backend folder:

```env
SERP_API_KEY=your_serpapi_key
```

---

## 5️⃣ Run Backend

```bash
uvicorn main:app --reload
```

Backend runs on:

```txt
http://127.0.0.1:8000
```

---

# 🎨 Frontend Setup

```bash
npm install
npm run dev
```

Frontend runs on:

```txt
http://localhost:5173
```

---

# 📡 API Endpoint

## Compare Grocery Prices

### POST `/compare`

### Example Request

```json
{
  "items": ["milk", "eggs", "bread"],
  "budget": 30,
  "zip_code": "33613"
}
```

---

## Example Response

```json
{
  "total_cost": 8.44,
  "budget_message": "Your cart is under budget by $21.56."
}
```

---

# 📸 Screenshots

## Home Page

- Grocery input
- Budget planning
- Cheapest shopping recommendation

## Full Store Comparison

- Compare same product across stores
- Direct product links
- Product images

---

# 🔥 Future Improvements

- Better AI product ranking
- Quantity understanding
- Shopping cart optimization
- Nearby store detection
- User authentication
- Saved grocery lists
- Price history tracking
- AI recommendation engine

---

# 👨‍💻 Author

Pearl Patel

GitHub:  
https://github.com/pearl31patel

---

# ⭐ Support

If you like this project, give it a star on GitHub ⭐
