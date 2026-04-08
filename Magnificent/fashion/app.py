from flask import Flask, render_template, request, redirect, url_for, session
import os
from brand_products import brand_products
from tech_products import tech_products

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fashion123")

_base_products = [
    # Clothing
    {"id": 1,  "name": "White Classic Tee",          "price": 29.99,  "category": "T-Shirts",  "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",  "badge": "New",  "desc": "Premium 100% cotton classic fit tee. Soft, breathable and timeless."},
    {"id": 2,  "name": "Slim Denim Jeans",            "price": 59.99,  "category": "Jeans",     "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",  "badge": "Hot",  "desc": "Modern slim fit jeans with stretch fabric for all-day comfort."},
    {"id": 3,  "name": "Floral Dress",                "price": 49.99,  "category": "Dresses",   "image": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400",  "badge": "New",  "desc": "Elegant floral wrap dress perfect for summer outings."},
    {"id": 4,  "name": "Leather Jacket",              "price": 129.99, "category": "Jackets",   "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",  "badge": "Sale", "desc": "Premium faux leather biker jacket with quilted lining."},
    {"id": 5,  "name": "Oversized Hoodie",            "price": 54.99,  "category": "Hoodies",   "image": "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=400",  "badge": "Hot",  "desc": "Ultra-soft fleece oversized hoodie for ultimate comfort."},
    {"id": 6,  "name": "Yoga Pants",                  "price": 39.99,  "category": "Activewear","image": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400",  "badge": "New",  "desc": "4-way stretch high-waist yoga pants with moisture-wicking fabric."},
    {"id": 7,  "name": "Oxford Shirt",                "price": 44.99,  "category": "Shirts",    "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400",  "badge": "Sale", "desc": "Classic Oxford weave button-down shirt for office or casual wear."},
    {"id": 8,  "name": "Trench Coat",                 "price": 119.99, "category": "Jackets",   "image": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400",  "badge": "Hot",  "desc": "Timeless double-breasted trench coat with belt and storm flap."},
    # Premium Shoes
    {"id": 9,  "name": "Nike Air Max 270",            "price": 189.99, "category": "Shoes",     "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",  "badge": "Hot",  "desc": "Iconic Air Max cushioning with a large heel unit for all-day comfort and bold style."},
    {"id": 10, "name": "Adidas Ultraboost 23",        "price": 219.99, "category": "Shoes",     "image": "https://images.unsplash.com/photo-1608231387042-66d1773d3028?w=400",  "badge": "New",  "desc": "Responsive Boost midsole with a Primeknit upper for an incredible running experience."},
    {"id": 11, "name": "Classic Leather Oxford",      "price": 249.99, "category": "Shoes",     "image": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=400",  "badge": "Sale", "desc": "Handcrafted full-grain leather Oxford shoes. Perfect for formal occasions."},
    {"id": 12, "name": "Suede Chelsea Boots",         "price": 299.99, "category": "Shoes",     "image": "https://images.unsplash.com/photo-1638247025967-b4e38f787b76?w=400",  "badge": "New",  "desc": "Premium suede Chelsea boots with elastic side panels and stacked heel."},
    {"id": 13, "name": "White Leather Sneakers",      "price": 159.99, "category": "Shoes",     "image": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=400",  "badge": "Hot",  "desc": "Minimalist white leather sneakers. Clean, versatile and effortlessly stylish."},
    {"id": 14, "name": "Running Pro Elite",           "price": 179.99, "category": "Shoes",     "image": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400",  "badge": "Sale", "desc": "Lightweight carbon-plate running shoes built for speed and performance."},
    # Premium Watches
    {"id": 15, "name": "Rolex Submariner Style",      "price": 899.99, "category": "Watches",   "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",  "badge": "Hot",  "desc": "Luxury diver-inspired watch with sapphire crystal glass and stainless steel bracelet."},
    {"id": 16, "name": "Minimalist Gold Watch",       "price": 349.99, "category": "Watches",   "image": "https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e?w=400",  "badge": "New",  "desc": "Slim minimalist watch with a gold-tone case and genuine leather strap."},
    {"id": 17, "name": "Chronograph Sport Watch",     "price": 499.99, "category": "Watches",   "image": "https://images.unsplash.com/photo-1548171915-e79a380a2a4b?w=400",  "badge": "Hot",  "desc": "Bold chronograph with tachymeter bezel, 100m water resistance and sapphire glass."},
    {"id": 18, "name": "Rose Gold Dress Watch",       "price": 429.99, "category": "Watches",   "image": "https://images.unsplash.com/photo-1612817288484-6f916006741a?w=400",  "badge": "New",  "desc": "Elegant rose gold dress watch with mother-of-pearl dial and mesh bracelet."},
    {"id": 19, "name": "Smart Luxury Watch",          "price": 649.99, "category": "Watches",   "image": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=400",  "badge": "Sale", "desc": "Premium smartwatch with health tracking, AMOLED display and titanium casing."},
    {"id": 20, "name": "Vintage Pilot Watch",         "price": 379.99, "category": "Watches",   "image": "https://images.unsplash.com/photo-1509941943102-10c232535736?w=400",  "badge": "Hot",  "desc": "Classic aviator-inspired watch with large Arabic numerals and anti-reflective glass."},
]

products = _base_products + brand_products

def get_cart():
    return session.get("cart", {})

def cart_total():
    cart = get_cart()
    total = 0
    for pid, qty in cart.items():
        p = next((x for x in products if x["id"] == int(pid)), None)
        if p:
            total += p["price"] * qty
    return round(total, 2)

def cart_count():
    return sum(get_cart().values())

@app.route("/")
def home():
    category = request.args.get("category", "")
    brand    = request.args.get("brand", "")
    search   = request.args.get("search", "").lower()
    filtered = [p for p in products if
        (not category or p["category"] == category) and
        (not brand    or p.get("brand","") == brand) and
        (not search   or search in p["name"].lower() or search in p.get("brand","").lower())]
    categories = sorted(set(p["category"] for p in products))
    brands     = sorted(set(p["brand"] for p in products if p.get("brand")))
    return render_template("home.html", products=filtered,
        categories=categories, brands=brands,
        selected=category, selected_brand=brand,
        search=search, cart_count=cart_count())

@app.route("/product/<int:pid>")
def product(pid):
    p = next((x for x in products if x["id"] == pid), None)
    if not p:
        return redirect(url_for("home"))
    return render_template("product.html", product=p, cart_count=cart_count())

@app.route("/add/<int:pid>")
def add(pid):
    cart = get_cart()
    key  = str(pid)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    return redirect(request.referrer or url_for("home"))

@app.route("/cart")
def cart():
    cart = get_cart()
    items = []
    for pid, qty in cart.items():
        p = next((x for x in products if x["id"] == int(pid)), None)
        if p:
            items.append({"product": p, "qty": qty, "sub": round(p["price"] * qty, 2)})
    return render_template("cart.html", items=items,
        total=cart_total(), cart_count=cart_count())

@app.route("/remove/<pid>")
def remove(pid):
    cart = get_cart()
    cart.pop(pid, None)
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/ask/<int:pid>", methods=["POST"])
def ask_product(pid):
    import json, re
    p = next((x for x in products if x["id"] == pid), None)
    if not p:
        return json.dumps({"answer": "Product not found."}), 404

    question = request.form.get("question", "").lower().strip()
    name     = p["name"]
    brand    = p.get("brand", "MAISON LUXE")
    cat      = p["category"]
    price    = p["price"]
    desc     = p["desc"]
    badge    = p.get("badge", "")

    # ── Smart rule-based AI responses ──────────────────────────
    def answer():
        # Price / value
        if any(w in question for w in ["price", "cost", "worth", "value", "expensive", "cheap", "afford"]):
            if price < 50:
                tier = "budget-friendly"
            elif price < 150:
                tier = "mid-range"
            elif price < 400:
                tier = "premium"
            else:
                tier = "luxury"
            return (f"The {name} is priced at ${price:.2f}, placing it in the {tier} segment. "
                    f"For a {brand} {cat.lower()}, this represents excellent value — "
                    f"you're paying for quality craftsmanship and brand heritage. "
                    f"{'It is currently on sale, making it an even better deal!' if badge == 'Sale' else 'It is a solid investment for your wardrobe.'}")

        # Quality / material
        if any(w in question for w in ["quality", "material", "fabric", "made", "durable", "last", "feel"]):
            return (f"The {name} by {brand} is crafted with premium materials expected from a {cat.lower()} at this price point. "
                    f"{desc} "
                    f"Based on the brand's reputation, you can expect excellent durability and a refined finish that holds up well over time.")

        # Fit / size
        if any(w in question for w in ["fit", "size", "sizing", "small", "large", "tight", "loose", "true to size"]):
            return (f"For the {name}, {brand} typically follows standard sizing. "
                    f"We recommend ordering your usual size. "
                    f"If you're between sizes, go up for a more relaxed fit or down for a snug, tailored look. "
                    f"Check the size guide on the product page for exact measurements.")

        # Occasion / use
        if any(w in question for w in ["occasion", "wear", "use", "casual", "formal", "office", "party", "gym", "sport", "outdoor", "event"]):
            occasion_map = {
                "Shoes":      "casual outings, smart-casual events, and everyday wear",
                "Watches":    "formal occasions, business meetings, and everyday luxury",
                "Jackets":    "layering in cooler weather, casual outings, and smart-casual looks",
                "Dresses":    "parties, dinners, summer events, and casual daytime wear",
                "Jeans":      "everyday casual wear, weekend outings, and smart-casual styling",
                "T-Shirts":   "everyday wear, gym sessions, and casual outings",
                "Hoodies":    "casual wear, lounging, gym warm-ups, and street style",
                "Activewear": "gym workouts, yoga, running, and active outdoor activities",
                "Shirts":     "office wear, smart-casual events, and formal occasions",
                "Bags":       "daily use, travel, shopping, and evening outings",
            }
            occ = occasion_map.get(cat, "a wide range of occasions")
            return (f"The {name} is perfectly suited for {occ}. "
                    f"{desc} "
                    f"Its versatile design makes it a great addition to any wardrobe.")

        # Brand / authenticity
        if any(w in question for w in ["brand", "authentic", "original", "fake", "genuine", "real"]):
            return (f"{brand} is a globally recognised fashion house known for quality and style. "
                    f"All products on MAISON LUXE are 100% authentic and sourced directly from authorised distributors. "
                    f"Every {name} comes with authenticity documentation and our 30-day return guarantee.")

        # Shipping / delivery
        if any(w in question for w in ["ship", "deliver", "delivery", "arrive", "dispatch", "fast", "express"]):
            return (f"We offer complimentary standard shipping on orders over $150. "
                    f"The {name} typically ships within 1–2 business days and arrives in 3–7 business days depending on your location. "
                    f"Express delivery is available at checkout for faster arrival.")

        # Return / refund
        if any(w in question for w in ["return", "refund", "exchange", "policy", "send back"]):
            return (f"We offer a hassle-free 30-day return and exchange policy on all items including the {name}. "
                    f"Simply contact our concierge team and we'll arrange a free collection. "
                    f"Refunds are processed within 5–7 business days.")

        # Comparison / alternatives
        if any(w in question for w in ["compare", "better", "alternative", "vs", "versus", "difference", "similar"]):
            return (f"The {name} stands out in the {cat.lower()} category for its combination of brand prestige and quality. "
                    f"Compared to alternatives at this price point, {brand} offers superior craftsmanship and a more refined aesthetic. "
                    f"If you're looking for something similar, browse our {cat} collection for more options.")

        # Recommendation / should I buy
        if any(w in question for w in ["recommend", "buy", "should i", "worth it", "good", "opinion", "review", "suggest"]):
            verdict = "highly recommend" if price < 300 else "consider a worthwhile investment"
            return (f"Based on the product details, we {verdict} the {name}. "
                    f"{desc} "
                    f"At ${price:.2f}, it offers the quality and style you'd expect from {brand}. "
                    f"{'The current sale price makes it an exceptional deal.' if badge == 'Sale' else ''} "
                    f"It has received strong interest from our customers and is a popular choice in the {cat.lower()} category.")

        # Care / washing
        if any(w in question for w in ["wash", "care", "clean", "maintain", "iron", "dry"]):
            care_map = {
                "Shoes":    "Wipe with a damp cloth and use appropriate shoe cleaner. Avoid machine washing.",
                "Watches":  "Wipe with a soft dry cloth. Avoid prolonged water exposure unless water-resistant.",
                "Jackets":  "Dry clean recommended. Spot clean with a damp cloth for minor marks.",
                "Dresses":  "Hand wash or gentle machine cycle in cold water. Lay flat to dry.",
                "Jeans":    "Machine wash cold, inside out. Tumble dry low or hang to dry to preserve colour.",
                "T-Shirts": "Machine wash cold. Tumble dry low. Do not bleach.",
                "Hoodies":  "Machine wash cold. Tumble dry low. Wash inside out to preserve print.",
                "Bags":     "Wipe with a dry cloth. Use leather conditioner for leather bags.",
            }
            care = care_map.get(cat, "Follow the care label instructions on the garment.")
            return f"Care instructions for the {name}: {care} Proper care will significantly extend the life of your {brand} piece."

        # Default — general summary
        return (f"The {name} by {brand} is a {cat.lower()} priced at ${price:.2f}. "
                f"{desc} "
                f"{'Currently marked as ' + badge + ' — a great time to buy!' if badge else 'A timeless addition to your collection.'} "
                f"Feel free to ask me anything specific — about sizing, quality, occasions, shipping, or whether it's worth buying!")

    return json.dumps({"answer": answer()})


@app.route("/festival")
def festival():
    # Festival discounts: pick 20 products and apply discounts
    import random
    random.seed(42)
    picks = random.sample(products, 20)
    deals = []
    discount_tiers = [10, 15, 20, 25, 30, 40, 50]
    for i, p in enumerate(picks):
        disc = discount_tiers[i % len(discount_tiers)]
        sale_price = round(p["price"] * (1 - disc / 100), 2)
        deals.append({**p, "discount": disc, "sale_price": sale_price})
    deals.sort(key=lambda x: x["discount"], reverse=True)
    return render_template("festival.html", deals=deals, cart_count=cart_count())

@app.route("/add_festival/<int:pid>/<int:disc>")
def add_festival(pid, disc):
    # Store festival price in session separately
    cart = get_cart()
    key  = str(pid)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    return redirect(url_for("festival"))


@app.route("/tech")
def tech():
    category = request.args.get("category", "")
    brand    = request.args.get("brand", "")
    search   = request.args.get("search", "").lower()
    filtered = [p for p in tech_products if
        (not category or p["category"] == category) and
        (not brand    or p.get("brand","") == brand) and
        (not search   or search in p["name"].lower() or search in p.get("brand","").lower())]
    categories = sorted(set(p["category"] for p in tech_products))
    brands     = sorted(set(p["brand"] for p in tech_products))
    return render_template("tech.html", products=filtered,
        categories=categories, brands=brands,
        selected=category, selected_brand=brand,
        search=search, cart_count=cart_count())

@app.route("/tech/product/<int:pid>")
def tech_product(pid):
    p = next((x for x in tech_products if x["id"] == pid), None)
    if not p:
        return redirect(url_for("tech"))
    return render_template("tech_product.html", product=p, cart_count=cart_count())

@app.route("/tech/add/<int:pid>")
def tech_add(pid):
    cart = get_cart()
    key  = "t" + str(pid)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    return redirect(request.referrer or url_for("tech"))

@app.route("/tech/cart")
def tech_cart():
    cart = get_cart()
    items = []
    total = 0.0
    for key, qty in cart.items():
        if key.startswith("t"):
            pid = int(key[1:])
            p = next((x for x in tech_products if x["id"] == pid), None)
            if p:
                sub = p["price"] * qty
                total += sub
                items.append({"product": p, "qty": qty, "sub": round(sub, 2), "key": key})
    return render_template("tech_cart.html", items=items,
        total=round(total, 2), cart_count=cart_count())

@app.route("/tech/remove/<key>")
def tech_remove(key):
    cart = get_cart()
    cart.pop(key, None)
    session["cart"] = cart
    return redirect(url_for("tech_cart"))

@app.route("/tech/checkout", methods=["GET", "POST"])
def tech_checkout():
    if request.method == "POST":
        # clear only tech items
        cart = get_cart()
        for k in list(cart.keys()):
            if k.startswith("t"):
                del cart[k]
        session["cart"] = cart
        return render_template("success.html", cart_count=cart_count())
    cart = get_cart()
    total = 0.0
    items = []
    for key, qty in cart.items():
        if key.startswith("t"):
            pid = int(key[1:])
            p = next((x for x in tech_products if x["id"] == pid), None)
            if p:
                sub = p["price"] * qty
                total += sub
                items.append({"product": p, "qty": qty, "sub": round(sub, 2)})
    return render_template("tech_checkout.html", items=items,
        total=round(total, 2), cart_count=cart_count())


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        session["cart"] = {}
        return render_template("success.html", cart_count=0)
    return render_template("checkout.html",
        total=cart_total(), cart_count=cart_count())

if __name__ == "__main__":
    import socket
    port = 5000

    # Get local network IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"

    print("\n" + "="*55)
    print("   MAISON LUXE + TECHZONE — Server Started")
    print("="*55)
    print(f"   Local:    http://127.0.0.1:{port}")
    print(f"   Network:  http://{local_ip}:{port}")
    print("="*55)
    print("   Share the Network URL with anyone on your WiFi")
    print("   Press CTRL+C to stop the server")
    print("="*55 + "\n")

    app.run(host="0.0.0.0", port=port, debug=False)
