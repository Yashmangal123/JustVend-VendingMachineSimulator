Vending Machine Simulator
Team Information
Team Name: JustVend

Project Title: Advanced Vending Machine Simulator

Team Members:

Yash Mangal - BC2025118
Shubham Kuvad - BC2025052
Harsh Lotiya - BC2025038

Project Description
A sophisticated vending machine simulator built in Python that replicates real-world vending machine operations with advanced features including user authentication, inventory management, category-based shopping, digital receipts, and administrative controls. The system maintains persistent data storage using JSON files and provides an intuitive interactive interface.


Concepts and Libraries Used
Programming Concepts
File Handling & Data Persistence - JSON-based data storage
Exception Handling - Robust error management
Data Structures - Dictionaries, Lists, Nested data
User Input Validation - Comprehensive input checking
Modular Programming - Organized function-based structure
Session Management - User state maintenance
Interactive UI - Menu-driven interface


Python Libraries
json - Data serialization and persistent storage
os - File system operations and screen management
datetime - Timestamp generation for orders
time - Delay operations for user experience
readchar - Interactive keyboard input handling


Project Structure
text
JustVend/
├── src/
│   └── vending_machine.py
├── data/
│   ├── vending_data.json
│   └── users.json
├── docs/
│   └── README.md
└── receipts/
    └── (automatically generated receipt files)


Main Modules and Functions
1. Core Application Setup
python
DATA_FILE = "vending_data.json"
USERS_FILE = "users.json"
ADMIN_PASSWORD = "JustVend"

vending_db = {
    "items": {},
    "orders": [],
    "revenue": 0,
    "order_count": 0,
    "categories": []
}


2. User Authentication System

Key Functions:
user_signup() - Creates new user accounts with validation
user_login() - Authenticates users with secure password checking
masked_input() - Securely captures passwords with asterisk display
delete_account() - User account management

Example Workflow:

=== VENDING MACHINE ===
> Login
  Signup
  Owner Panel
  Exit

Username: harsh_lotiya
Password: ********
Login successful!

3. Inventory Management System
Functions:
display_items() - Shows all available items with details
admin_add_items() - Bulk item addition with category management
modify_item() - Dynamic item editing (price, quantity, category)
show_item_details() - Comprehensive item information display

Data Structure:

json
{
  "Lays Chips": {
    "price": 20,
    "qty": 25,
    "cat": "Snacks"
  },
  "Coca Cola": {
    "price": 30,
    "qty": 15,
    "cat": "Beverages"
  }
}

4. Advanced Shopping System
Core Functions:
user_shopping() - Main shopping interface controller
select_category() - Category-based navigation
select_item() - Item selection with real-time stock display
select_quantity() - Intelligent quantity validation

Interactive Menu Example:

--- SELECT CATEGORY ---
> Beverages
  Snacks
  Chocolates
  Back

--- SELECT ITEM (Beverages) ---
> Coca Cola (qty:15) - ₹30
  Pepsi (qty:12) - ₹25
  Mineral Water (qty:20) - ₹20
  Back

5. Shopping Cart Management
Features:
display_cart() - Real-time cart visualization
Dynamic quantity modification
Item removal capability
Running total calculation

Cart Display:

--- CART ---
Coca Cola x2 = ₹60
Lays Chips x1 = ₹20
KitKat x3 = ₹75
----------------
TOTAL: ₹155

6. Checkout & Payment System
Functions:
process_checkout() - Complete transaction processing
create_receipt() - Digital receipt generation
Stock updating
Order history recording

Payment Process:

--- CHECKOUT ---
Items in your order:
==================================================
• Coca Cola
  Quantity: 2
  Price: ₹30 each
  Subtotal: ₹60
--------------------------------------------------
• Lays Chips
  Quantity: 1
  Price: ₹20 each
  Subtotal: ₹20
--------------------------------------------------

TOTAL ITEMS: 3
TOTAL AMOUNT: ₹80
==================================================

Proceed to payment? (y/n): y

Enter payment amount (Total ₹80): 100
Payment successful! Change: ₹20

7. Administrative Control Panel
Admin Features:
Inventory management
Sales analytics and reporting
Order history tracking
Revenue monitoring
User management

Access:

Owner/Admin Password: ********

--- OWNER / ADMIN PANEL ---
> Manage Items
  Sales Report
  Back

****************************************
Setup Instructions
Prerequisites
Python 3.6 or higher
readchar library

Installation Steps
Install Required Library:

bash
pip install readchar
Project Setup:

bash
# Create project directory
mkdir JustVend
cd JustVend

# Place the vending_machine.py file in the directory
# Run the application
python vending_machine.py
Automatic File Generation
The application automatically creates:

vending_data.json - Items, orders, revenue data

users.json - User account information

receipt_*.txt - Transaction receipts

Complete Usage Guide
For Customers:
Account Creation & Login

→ Select "Signup" from main menu
→ Enter username and password
→ Account created successfully
→ Login with credentials
Shopping Process

→ Select "Buy Items"
→ Browse categories (Beverages, Snacks, etc.)
→ Select items and quantities
→ Manage cart (add/remove/modify)
→ Proceed to checkout
→ Make payment
→ Receive digital receipt
Account Management

→ Delete account if needed
→ Secure logout
For Administrators:
Access Admin Panel

→ Select "Owner Panel" from main menu
→ Enter password: "JustVend"
→ Access administrative features
Inventory Management

→ Add new items in bulk
→ Modify existing items (price, quantity, category)
→ View detailed item information
→ Monitor stock levels
Sales Analytics

→ View total revenue
→ Analyze order history
→ Track sales performance
→ Generate sales reports

**********************
Technical Features
Data Persistence
Automatic Saving: All changes saved immediately
JSON Format: Human-readable data storage
Backup System: Temporary file writing for data integrity
*****************************
Error Handling
Input Validation: Comprehensive user input checking
Stock Management: Prevent over-selling items
Payment Verification: Ensure sufficient payment amounts
File Operation Safety: Handle file read/write errors
*******************************
User Experience
Interactive Menus: Keyboard-driven navigation
Real-time Updates: Immediate cart and stock updates
Visual Feedback: Color-coded interface elements
Session Management: Maintain user state throughout usage

************************************
Example Scenarios
Scenario 1: Complete Customer Journey
text
1. Main Menu → Signup → Create account (yash_mangal)
2. Login → Access system
3. Buy Items → Select "Beverages" category
4. Add "Coca Cola" x2 to cart
5. Add "Mineral Water" x1 to cart
6. View Cart → Verify items
7. Checkout → Pay ₹80
8. Receive receipt_receipt_001.txt
Scenario 2: Administrative Operations
text
1. Owner Panel → Enter "JustVend" password
2. Manage Items → Add Items
3. Add new product: "Orange Juice", ₹35, Qty: 10, Category: "Beverages"
4. Edit existing item: Update "Lays Chips" price to ₹25
5. View Sales Report → Check revenue: ₹1250
Code Structure Highlights
Main Program Flow
python
def main():
    while True:
        if current_session["user"] is None:
            # Show login/signup menu
        else:
            # Show user shopping menu
Data Management
python
def load_data(file_path, default_value):
    return json.load(open(file_path)) if os.path.exists(file_path) else default_value

def save_data(file_path, data):
    # Safe file writing with temporary files
Interactive Interface
python
def interactive_menu(options, title=""):
    # Handles keyboard navigation with arrow keys
    # Provides visual selection feedback

Team Contribution
Yash Mangal: Core architecture, user authentication, data persistence
Shubham Kuvad: Shopping system, cart management, UI/UX design
Harsh Lotiya: Inventory management, admin features, payment system