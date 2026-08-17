PIXEL VAULT - FULL-STACK DIGITAL SHOPPING WEBSITE

OVERVIEW
Pixel Vault is a full-stack shopping website designed for purchasing digital gaming products. The website provides both a customer storefront and an admin sales dashboard.

FEATURES
- Digital product catalogue containing 10+ products
- Products retrieved from an SQLite database
- Add products to a shopping cart
- Change product quantities
- Remove products from the cart
- Automatic cart total calculations
- Customer delivery details including:
  - Email address
  - Phone number
  - Suburb
- Input validation for customer information
- Checkout and sale completion
- Completed sales stored persistently in the database
- Unique order numbers generated for completed transactions
- Admin sales dashboard
- Displays total sales count
- Displays gross revenue
- Displays total cost
- Displays net profit
- Displays individual completed transactions and purchased products
- Responsive design for desktop, tablet and mobile devices

TECHNOLOGIES USED
Front End:
- HTML
- CSS
- JavaScript

Back End:
- Python
- Flask

Database:
- SQLite

SECURITY AND DATA VALIDATION
Pixel Vault demonstrates basic security practices including:
- Parameterised SQL queries to reduce SQL injection risk
- Server-side email validation
- Server-side Australian mobile number validation
- Required suburb validation
- Cart validation
- Product and quantity validation
- Product pricing retrieved from the database during checkout rather than trusting customer-submitted prices

PROJECT FILES
- app.py
- init_db.py
- pixelvault.db
- templates/index.html
- static/css/style.css
- static/js/script.js
- README.txt

HOW TO RUN LOCALLY
1. Ensure Python and Flask are installed.
2. Open a terminal in the Pixel Vault project directory.
3. Run:

   python app.py

4. Open a web browser.
5. Navigate to the local Flask address displayed in the terminal, typically:

   http://127.0.0.1:5000

DATABASE
Pixel Vault uses an SQLite database named pixelvault.db.

The database stores:
- Product information
- Product cost and sell prices
- Product image information
- Completed customer orders
- Individual items associated with each order

ADMIN DASHBOARD
The Admin Portal provides a sales summary containing:
- Total sales count
- Gross revenue
- Total cost
- Net profit
- Completed transaction details
- Purchaser information
- Products purchased
- Cost price
- Sale price
- Profit

RESPONSIVE DESIGN
The website has been designed to operate across desktop, tablet and mobile screen sizes. Responsive CSS media queries adjust the website layout based on the available screen width.

PROJECT PURPOSE
This project was developed as a full-stack web technologies project demonstrating front-end development, back-end development, database integration, responsive web design, data validation and basic web security practices.