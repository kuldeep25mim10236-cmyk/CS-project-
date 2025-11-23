Fastcart
A simple e-commerce web application built with Flask and JavaScript.

What is this?
Fastcart is an online shopping website where you can:

Browse 28 products in 8 different categories

Search for products

Add items to your shopping cart

The cart saves automatically (even after closing the browser)

What's included?
Frontend: A website you can open in any browser

Backend: A server that handles data and API requests

Database: Stores all products and orders

How to run this project
Step 1: Run the Backend
bash
cd backend
pip install -r requirements.txt
python app.py
The server will start at http://localhost:5000

Step 2: Open the Frontend
bash
cd frontend
Then double-click index.html or open it in your browser.

Project folders
text
ecommerce-project/
├── frontend/
│   └── index.html          (the website)
├── backend/
│   ├── app.py              (main server file)
│   ├── config.py           (settings)
│   ├── requirements.txt    (what to install)
│   ├── models/             (database structure)
│   └── routes/             (API endpoints)
└── README.md               (this file)
What you can do
Browse Products - See all 28 products

Search - Type to find products

Filter - Click category buttons to filter

Shopping Cart - Add, remove, change quantities

Order - Place orders through the API

Technologies used
Frontend:

HTML

CSS

JavaScript

Backend:

Python 3.7+

Flask

SQLite database

Product categories
Electronics (4 items)

Fashion (4 items)

Home & Living (4 items)

Books (4 items)

Sports (4 items)

Beauty (4 items)

Toys (4 items)

Total: 28 products

API endpoints
Get products
text
GET /api/products
GET /api/products?category=electronics
GET /api/products?search=laptop
Manage products
text
POST /api/products
PUT /api/products/<id>
DELETE /api/products/<id>
Orders
text
GET /api/orders
POST /api/orders
PUT /api/orders/<id>
DELETE /api/orders/<id>
Testing
Start backend: python app.py

Open frontend/index.html in browser

Try searching, filtering, adding to cart
