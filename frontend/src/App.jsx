import { useState } from "react";
import { motion } from "framer-motion";
import {
  ShoppingCart,
  Sparkles,
  Wallet,
  Store,
  Loader2,
  Plus,
  Trash2,
  Mail,
  Info,
} from "lucide-react";

const API_URL = "https://smartcart-ai-11vj.onrender.com/";

function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-slate-950/90 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <a href="#home" className="flex items-center gap-3">
          <div className="rounded-2xl bg-emerald-400 p-2 text-slate-950">
            <ShoppingCart size={24} />
          </div>
          <span className="text-xl font-bold text-white">SmartCart AI</span>
        </a>

        <nav className="flex items-center gap-5 md:gap-8">
          <a
            href="#home"
            className="text-sm text-slate-300 hover:text-emerald-300"
          >
            Home
          </a>
          <a
            href="#about"
            className="text-sm text-slate-300 hover:text-emerald-300"
          >
            About
          </a>
          <a
            href="#contact"
            className="text-sm text-slate-300 hover:text-emerald-300"
          >
            Contact
          </a>
        </nav>
      </div>
    </header>
  );
}

function Footer() {
  return (
    <footer
      id="contact"
      className="mt-20 border-t border-white/10 bg-slate-950/95"
    >
      <div className="mx-auto max-w-7xl px-6 py-12">
        <div className="flex flex-col gap-12 md:flex-row md:justify-between">
          <div className="w-full md:w-[260px]">
            <div className="mb-4 flex items-center gap-3">
              <ShoppingCart className="text-emerald-300" size={28} />
              <h3 className="text-2xl font-bold text-white">SmartCart AI</h3>
            </div>

            <p className="text-base leading-7 text-slate-400">
              A real-data grocery price comparison app that helps users shop
              smarter and save money.
            </p>
          </div>

          <div className="w-full md:w-[260px]">
            <div className="mb-4 flex items-center gap-3">
              <Info className="text-slate-200" size={22} />
              <h4 className="text-2xl font-bold text-white">Product</h4>
            </div>

            <div className="flex flex-col gap-3 text-base text-slate-400">
              <span>Real grocery search</span>
              <span>Cheapest shopping plan</span>
              <span>Budget-based comparison</span>
            </div>
          </div>

          <div className="w-full md:w-[260px]">
            <div className="mb-4 flex items-center gap-3">
              <Store className="text-slate-200" size={22} />
              <h4 className="text-2xl font-bold text-white">Stores</h4>
            </div>

            <div className="flex flex-col gap-3 text-base text-slate-400">
              <span>Walmart</span>
              <span>Target</span>
              <span>Costco</span>
              <span>Amazon Fresh</span>
            </div>
          </div>

          <div className="w-full md:w-[260px]">
            <div className="mb-4 flex items-center gap-3">
              <Mail className="text-slate-200" size={22} />
              <h4 className="text-2xl font-bold text-white">Contact</h4>
            </div>

            <p className="text-base text-slate-400">Built by Pearl Patel</p>

            <a
              href="mailto:pearl31patelus@gmail.com"
              className="mt-3 inline-block text-base font-medium text-emerald-300 hover:text-emerald-200"
            >
              pearl31patelus@gmail.com
            </a>
          </div>
        </div>
      </div>

      <div className="border-t border-white/10 py-5 text-center text-sm text-slate-500">
        © 2026 SmartCart AI. All rights reserved.
      </div>
    </footer>
  );
}

export default function App() {
  const [item, setItem] = useState("");
  const [items, setItems] = useState(["milk", "eggs", "bread"]);
  const [budget, setBudget] = useState(30);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const addItem = () => {
    if (!item.trim()) return;
    setItems([...items, item.trim()]);
    setItem("");
  };

  const removeItem = (index) => {
    setItems(items.filter((_, i) => i !== index));
  };

  const comparePrices = async () => {
    setLoading(true);
    setData(null);

    try {
      const response = await fetch(`${API_URL}/compare`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          items,
          budget: Number(budget),
          zip_code: "33613",
        }),
      });

      const result = await response.json();
      setData(result);
    } catch (error) {
      alert("Backend is not running. Please start FastAPI server.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen overflow-hidden bg-gradient-to-br from-slate-950 via-blue-950 to-emerald-950 text-white">
      <Header />

      <div className="absolute left-10 top-20 h-72 w-72 rounded-full bg-emerald-400 opacity-20 blur-[130px]" />
      <div className="absolute bottom-10 right-10 h-72 w-72 rounded-full bg-blue-400 opacity-20 blur-[130px]" />

      <main id="home" className="relative mx-auto max-w-7xl px-6 py-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center"
        >
          <h1 className="text-5xl font-bold leading-tight md:text-7xl">
            Save Money With
            <span className="block bg-gradient-to-r from-emerald-300 to-blue-300 bg-clip-text text-transparent">
              SmartCart AI
            </span>
          </h1>

          <p className="mx-auto mt-5 max-w-2xl text-lg text-slate-300">
            Compare Walmart, Target, Costco, and Amazon Fresh. Get the cheapest
            shopping plan based on your grocery list and budget.
          </p>
        </motion.div>

        <div className="mt-12 grid gap-8 lg:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass rounded-3xl p-6 shadow-2xl"
          >
            <div className="mb-6 flex items-center gap-3">
              <div className="rounded-2xl bg-emerald-400/20 p-3">
                <ShoppingCart className="text-emerald-300" />
              </div>
              <div>
                <h2 className="text-2xl font-bold">Build Grocery List</h2>
                <p className="text-sm text-slate-300">
                  Add items you want to compare.
                </p>
              </div>
            </div>

            <div className="flex gap-3">
              <input
                value={item}
                onChange={(e) => setItem(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addItem()}
                placeholder="Example: rice 20, eggs 12, milk 1"
                className="w-full rounded-2xl border border-white/10 bg-white/10 px-4 py-3 text-white outline-none placeholder:text-slate-400"
              />

              <button
                onClick={addItem}
                className="rounded-2xl bg-emerald-400 px-5 text-slate-950 transition hover:bg-emerald-300"
              >
                <Plus />
              </button>
            </div>

            <div className="mt-5 flex flex-wrap gap-3">
              {items.map((grocery, index) => (
                <motion.div
                  key={index}
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className="flex items-center gap-2 rounded-full bg-white/10 px-4 py-2"
                >
                  <span>{grocery}</span>
                  <button onClick={() => removeItem(index)}>
                    <Trash2 size={15} className="text-red-300" />
                  </button>
                </motion.div>
              ))}
            </div>

            <div className="mt-8">
              <label className="mb-2 flex items-center gap-2 text-sm text-slate-300">
                <Wallet size={16} />
                Budget
              </label>

              <input
                type="number"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                className="w-full rounded-2xl border border-white/10 bg-white/10 px-4 py-3 text-white outline-none"
              />
            </div>

            <button
              onClick={comparePrices}
              disabled={loading || items.length === 0}
              className="mt-8 flex w-full items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-emerald-400 to-blue-400 px-6 py-4 font-bold text-slate-950 transition hover:scale-[1.02] disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin" />
                  Comparing prices...
                </>
              ) : (
                <>
                  <Sparkles />
                  Find Cheapest Plan
                </>
              )}
            </button>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass rounded-3xl p-6 shadow-2xl"
          >
            <div className="mb-6 flex items-center gap-3">
              <div className="rounded-2xl bg-blue-400/20 p-3">
                <Store className="text-blue-300" />
              </div>
              <div>
                <h2 className="text-2xl font-bold">Cheapest Plan</h2>
                <p className="text-sm text-slate-300">
                  AI-powered shopping recommendation.
                </p>
              </div>
            </div>

            {!data && !loading && (
              <div className="flex h-80 items-center justify-center rounded-3xl border border-dashed border-white/20 text-center text-slate-400">
                Add grocery items and compare prices.
              </div>
            )}

            {loading && (
              <div className="flex h-80 flex-col items-center justify-center gap-4">
                <Loader2 className="h-12 w-12 animate-spin text-emerald-300" />
                <p className="text-slate-300">Searching best prices...</p>
              </div>
            )}

            {data && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <div className="rounded-3xl bg-emerald-400/10 p-5">
                  <p className="text-sm text-slate-300">Estimated Total</p>
                  <h3 className="mt-1 text-4xl font-bold text-emerald-300">
                    ${data.total_cost}
                  </h3>
                  <p className="mt-3 text-sm text-slate-300">
                    {data.budget_message}
                  </p>
                </div>

                <div className="mt-6 space-y-4">
                  {data.cheapest_plan.map((product, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 15 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.08 }}
                      className="rounded-2xl bg-white/10 p-4"
                    >
                      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                        {product.image && (
                          <img
                            src={product.image}
                            alt={product.name}
                            className="h-28 w-28 rounded-2xl object-cover"
                          />
                        )}

                        <div className="flex-1">
                          <p className="text-lg font-semibold">
                            {product.item}
                          </p>
                          <p className="text-sm text-slate-300">
                            {product.name}
                          </p>
                          <p className="mt-1 text-sm text-blue-300">
                            Best store: {product.store}
                          </p>

                          {product.link && (
                            <a
                              href={product.link}
                              target="_blank"
                              rel="noreferrer"
                              className="mt-3 inline-block rounded-xl bg-emerald-400 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-emerald-300"
                            >
                              Open Product
                            </a>
                          )}
                        </div>

                        <div className="w-fit rounded-2xl bg-emerald-400 px-4 py-2 font-bold text-slate-950">
                          ${product.price}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            )}
          </motion.div>
        </div>

        {data && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass mt-8 rounded-3xl p-6"
          >
            <h2 className="mb-5 text-2xl font-bold">Full Store Comparison</h2>

            <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {data.results.map((group, index) => (
                <div key={index} className="rounded-2xl bg-white/10 p-5">
                  <h3 className="mb-4 text-xl font-bold capitalize">
                    {group.item}
                  </h3>

                  <div className="space-y-3">
                    {group.prices.map((p, i) => (
                      <div
                        key={i}
                        className={`flex justify-between gap-4 rounded-xl px-4 py-3 ${
                          p.store === group.cheapest.store
                            ? "bg-emerald-400/20"
                            : "bg-white/5"
                        }`}
                      >
                        <div>
                          <p className="font-medium">{p.store}</p>
                          <p className="text-xs text-slate-400">{p.name}</p>
                        </div>
                        <p className="font-bold">${p.price}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        <section id="about" className="glass mt-16 rounded-3xl p-6">
          <h2 className="text-2xl font-bold">About SmartCart AI</h2>
          <p className="mt-3 text-slate-300">
            SmartCart AI helps users compare grocery prices from major stores
            and create a cheaper shopping plan. It is designed for daily grocery
            decisions, budget planning, and smarter shopping.
          </p>
        </section>
      </main>

      <Footer />
    </div>
  );
}
