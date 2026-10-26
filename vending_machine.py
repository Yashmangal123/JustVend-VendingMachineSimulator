#Library Used
import json
import os
import datetime
import time
import readchar

DATA_FILE = "vending_data.json"
USERS_FILE = "users.json"
ADMIN_PASSWORD = "JustVend"

# Password input
def masked_input(prompt="Password: "):
    print(prompt, end="", flush=True)
    password = ""
    while True:
        char = readchar.readchar()
        if char in ["\n", "\r"]:  
            print()
            break
        if char in ["\x08", "\x7f"]:  
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end="", flush=True)
            continue
        if ord(char) < 32:  
            continue
        password += char
        print("*", end="", flush=True)
    return password

# Load data from JSON file
def load_data(file_path, default_value):
    return json.load(open(file_path)) if os.path.exists(file_path) else default_value

# Save data to JSON file 
def save_data(file_path, data):
    temp_file = file_path + ".tmp"
    with open(temp_file, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_file, file_path)

# Get current date and time
def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Clear terminal screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Interactive menu with toggle
def interactive_menu(options, title=""):
    if not options:
        return None
    selected_index = 0
    while True:
        clear_screen()
        if title:
            print("\033[96m" + title + "\033[0m\n")
        for i, option in enumerate(options):
            marker = "\033[92m> \033[0m" if i == selected_index else "  "
            print(marker + option)
        key = readchar.readkey()
        if key == readchar.key.UP:
            selected_index = (selected_index - 1) % len(options)
        elif key == readchar.key.DOWN:
            selected_index = (selected_index + 1) % len(options)
        elif key == readchar.key.ENTER:
            return selected_index


vending_db = load_data(DATA_FILE, {
    "items": {},
    "orders": [],
    "revenue": 0,
    "order_count": 0,
    "categories": []
})

user_db = load_data(USERS_FILE, {})
current_session = {"user": None}

# User registration function
def user_signup():
    clear_screen()
    print("\033[96m--- CREATE ACCOUNT ---\033[0m")
    username = input("Username: ").strip()
    if not username:
        print("Invalid username."); time.sleep(1); return
    if username in user_db:
        print("User already exists."); time.sleep(1); return
    password = masked_input("Password: ")
    user_db[username] = {"password": password, "disabled": False}
    save_data(USERS_FILE, user_db)
    print("Account created successfully!")
    time.sleep(1)

# User login function
def user_login():
    clear_screen()
    print("\033[96m--- LOGIN ---\033[0m")
    username = input("Username: ").strip()
    if username not in user_db:
        print("User does not exist.")
        time.sleep(0.5)
        return
    while True:
        password = masked_input("Password: ")
        if user_db[username]["password"] == password:
            current_session["user"] = username
            print("Login successful!")
            return
        print("Wrong password! Try again.")
        print("Press ENTER to retry or type 'back' to cancel.")
        if input("> ").strip().lower() == "back":
            return

# Delete user account
def delete_account():
    username = current_session["user"]
    if username:
        del user_db[username]
        save_data(USERS_FILE, user_db)
        current_session["user"] = None
        print("Account deleted.")
        time.sleep(0.5)

# Display all available items
def display_items():
    clear_screen()
    print("\033[96m--- ITEMS IN MACHINE ---\033[0m\n")
    if not vending_db["items"]:
        print("No items available.")
        return
    for name, item in vending_db["items"].items():
        print(f"{name} | ₹{item['price']} | qty:{item['qty']} | cat:{item['cat']}")

# Show detailed item information
def show_item_details():
    clear_screen()
    print("\033[96m--- ITEM DETAILS ---\033[0m\n")
    if not vending_db["items"]:
        print("No items found.")
        input("\nPress ENTER...")
        return
    for name, item in vending_db["items"].items():
        print(f"""
Name        : {name}
Price       : ₹{item['price']}
Quantity    : {item['qty']}
Category    : {item['cat']}
----------------------------------------------
""")
    input("Press ENTER to return...")

# Edit existing item details (Admin function)
def modify_item():
    clear_screen()
    print("\033[96m--- EDIT ITEM ---\033[0m\n")
    if not vending_db["items"]:
        print("No items available.")
        time.sleep(1)
        return
    items = list(vending_db["items"].keys())
    choice = interactive_menu(items + ["Back"], "--- SELECT ITEM TO EDIT ---")
    if choice is None or choice == len(items):
        return
    item_name = items[choice]
    item = vending_db["items"][item_name]
    clear_screen()
    print(f"\033[96mEditing: {item_name}\033[0m")
    print(f"Current Price: {item['price']}")
    print(f"Current Quantity: {item['qty']}")
    print(f"Current Category: {item['cat']}")
    print("--------------------------------")
    try:
        new_price = input("New Price (leave blank to keep same): ").strip()
        new_qty = input("New Quantity (leave blank to keep same): ").strip()
        new_cat = input("New Category (leave blank to keep same): ").strip()
        if new_price != "":
            item["price"] = int(new_price)
        if new_qty != "":
            item["qty"] = int(new_qty)
        if new_cat != "":
            item["cat"] = new_cat
        save_data(DATA_FILE, vending_db)
        print("Item updated successfully!")
        time.sleep(1)
    except (ValueError, TypeError):
        print("Invalid input. Update failed.")
        time.sleep(1)

# Add items to inventory (Admin function)
def admin_add_items():
    clear_screen()
    print("\033[96m--- ADD MULTIPLE ITEMS ---\033[0m")
    if vending_db["items"]:
        print("\nCurrent Items:\n")
        for name, item in vending_db["items"].items():
            print(f"• {name} | ₹{item['price']} | qty:{item['qty']} | cat:{item['cat']}")
    print("\nLeave item name blank to stop.\n")
    while True:
        name = input("Item Name: ").strip()
        if name == "":
            print("Finished adding items.")
            time.sleep(1)
            return
        if name in vending_db["items"]:
            print("Item already exists. Skipping...")
            time.sleep(0.5)
            continue
        try:
            price = int(input("Price: "))
            qty = int(input("Qty: "))
        except ValueError:
            print("Invalid values. Skipped.")
            time.sleep(1)
            continue
        print("Available Categories:")
        for cat in vending_db["categories"]:
            print(" -", cat)
        category = input("Category: ").strip()
        if category not in vending_db["categories"]:
            vending_db["categories"].append(category)
        vending_db["items"][name] = {"price": price, "qty": qty, "cat": category}
        save_data(DATA_FILE, vending_db)
        print(f"Added: {name}")
        time.sleep(0.5)

# Display cart 
def display_cart(cart):
    clear_screen()
    print("\033[96m--- CART ---\033[0m\n")
    if not cart:
        print("Cart is empty.")
    else:
        for item_name, quantity in cart.items():
            price = vending_db["items"][item_name]["price"]
            print(f"{item_name} x{quantity} = ₹{price * quantity}")
    input("\nPress ENTER...")

# Receipt Generation
def create_receipt(order_id, cart, total, paid):
    filename = f"receipt_{order_id}.txt"
    change = paid - total
    with open(filename, "w") as f:
        f.write(f"""
************ RECEIPT ************
Order ID : {order_id}
Date     : {current_time()}
-----------------------------------------
Items Purchased:
""")
        for item_name, quantity in cart.items():
            price = vending_db['items'][item_name]['price']
            f.write(f"- {item_name}\n")
            f.write(f"  Quantity: {quantity} × ₹{price} = ₹{price * quantity}\n")
        f.write(f"""
-----------------------------------------
Total Items: {sum(cart.values())}
Total Bill : ₹{total}
Paid       : ₹{paid}
Change     : ₹{change}
=========================================
        THANK YOU FOR SHOPPING!
=========================================
""")
    print(f"Receipt saved → {filename}")
    time.sleep(1)

# Process checkout and payment
def process_checkout(cart):
    username = current_session["user"]
    clear_screen()
    print("\033[96m--- CHECKOUT ---\033[0m\n")
    if not cart:
        print("Cart is empty. Nothing to checkout.")
        time.sleep(1)
        return
    print("Items in your order:")
    print("=" * 50)
    total_amount = 0
    item_count = 0
    for item_name, quantity in cart.items():
        if item_name in vending_db["items"]:
            item = vending_db["items"][item_name]
            price = item["price"]
            subtotal = price * quantity
            total_amount += subtotal
            item_count += quantity
            print(f"• {item_name}")
            print(f"  Quantity: {quantity}")
            print(f"  Price: ₹{price} each")
            print(f"  Subtotal: ₹{subtotal}")
            print("-" * 30)
    print(f"\nTOTAL ITEMS: {item_count}")
    print(f"TOTAL AMOUNT: ₹{total_amount}")
    print("=" * 50)
    confirm = input("\nProceed to payment? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Checkout cancelled.")
        time.sleep(1)
        return
    amount_paid = 0
    while True:
        try:
            if amount_paid == 0:
                inp = input(f"\nEnter payment amount (Total ₹{total_amount}, or type 'cancel' to abort): ").strip().lower()
                if inp in ["cancel", "back", "exit"]:
                    print("Payment cancelled.")
                    time.sleep(1)
                    return
                try:
                    value = int(inp)
                except ValueError:
                    print("Invalid amount. Please enter a number.")
                    time.sleep(1)
                    continue
            else:
                remaining = total_amount - amount_paid
                inp = input(f"\nRemaining amount required: ₹{remaining} → Pay now (or type 'cancel' to abort and refund): ").strip().lower()
                if inp in ["cancel", "back", "exit"]:
                    print("Payment cancelled. Refunding ₹", amount_paid)
                    time.sleep(1)
                    return
                try:
                    value = int(inp)
                except ValueError:
                    print("Invalid amount. Please enter a number.")
                    time.sleep(1)
                    continue
        except Exception:
            print("Invalid amount. Please enter a number.")
            time.sleep(1)
            continue
        if value <= 0:
            print("Please enter an amount greater than 0.")
            time.sleep(1)
            continue
        amount_paid += value
        if amount_paid < total_amount:
            remaining = total_amount - amount_paid
            print(f"Amount insufficient. You still need to pay ₹{remaining}.")
            time.sleep(1)
            continue
        break
    paid = amount_paid
    for item_name, quantity in cart.items():
        vending_db["items"][item_name]["qty"] -= quantity
    vending_db["order_count"] += 1
    order_id = vending_db["order_count"]
    order_data = {"id": order_id, "user": username, "items": cart.copy(), "total": total_amount, "time": current_time()}
    vending_db["orders"].append(order_data)
    vending_db["revenue"] += total_amount
    save_data(DATA_FILE, vending_db)
    create_receipt(order_id, cart, total_amount, paid)
    cart.clear()

# Instock items filter
def get_categories_with_stock():
    categories = {}
    for name, item in vending_db["items"].items():
        if item.get("qty", 0) > 0:
            cat = item.get("cat", "Uncategorized")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(name)
    return categories

# Select category from categories
def select_category():
    categories = get_categories_with_stock()
    if not categories:
        print("No categories with items available.")
        time.sleep(1)
        return None
    
    options = sorted(list(categories.keys())) + ["Back"]
    choice = interactive_menu(options, "--- SELECT CATEGORY ---")
    
    if choice is None or options[choice] == "Back":
        return None
    return options[choice]

# Select item from chosen category
def select_item(category):
    categories = get_categories_with_stock()
    items = categories.get(category, [])
    
    if not items:
        print("No items available in this category.")
        time.sleep(1)
        return None
    item_options = [f"{item} (qty:{vending_db['items'][item]['qty']})" for item in sorted(items)]
    options = item_options + ["Back"]
    
    choice = interactive_menu(options, f"--- SELECT ITEM ({category}) ---")
    
    if choice is None or options[choice] == "Back":
        return None
    return sorted(items)[choice]  

# Select quantity for chosen item
def select_quantity(item_name):
    item = vending_db['items'][item_name]
    while True:
        clear_screen()
        print("\033[96m=== ITEM DETAILS ===\033[0m\n")
        print(f"Name      : {item_name}")
        print(f"Price     : ₹{item['price']}")
        print(f"Available : {item['qty']}")
        print(f"Category  : {item['cat']}")
        print("----------------------------------")
        print("Enter quantity (0 = Back):")
        try:
            qty = int(input("Quantity: "))
        except ValueError:
            print("Invalid number.")
            time.sleep(1)
            continue
        if qty == 0:
            return None
        if qty < 0:
            print("Quantity must be > 0")
            time.sleep(1)
            continue
        if qty > item['qty']:
            print("Not enough stock! Try again.")
            time.sleep(1)
            continue
        return qty

# Shopping interface
def user_shopping():
    shopping_cart = {}
    while True:
        clear_screen()
        print("\033[96m--- BUY MENU ---\033[0m\n")
        choice = interactive_menu(
            ["Add Item", "Remove Item", "Change Quantity", "View Cart", "Checkout", "Back"],
            "--- BUY MENU ---"
        )
        if choice == 0:
            current_category = None
            while True:
                if not current_category:
                    current_category = select_category()
                    if not current_category:
                        break
                
                item = select_item(current_category)
                if not item:
                    current_category = None
                    continue
                
                available_stock = vending_db['items'][item]['qty']
                current_in_cart = shopping_cart.get(item, 0)
                
                max_allowed = available_stock - current_in_cart
                if max_allowed <= 0:
                    print(f"Already have all available {available_stock} {item} in cart!")
                    time.sleep(1)
                    continue
                
                qty = select_quantity(item)
                if qty is None:
                    continue
                
                if current_in_cart + qty > available_stock:
                    print(f"Cannot add {qty} more! You already have {current_in_cart} in cart.")
                    print(f"Available stock: {available_stock}, Maximum you can add: {max_allowed}")
                    time.sleep(1)
                    continue
                
                shopping_cart[item] = shopping_cart.get(item, 0) + qty
                print(f"\033[92mAdded {qty} x {item} to cart!\033[0m\n")
                time.sleep(0.4)
                
                clear_screen()
                continue_choice = interactive_menu(
                    ["Add more from same category", "Change category", "Back to Buy Menu"],
                    "--- ADD MORE? ---"
                )
                if continue_choice == 0:
                    continue
                elif continue_choice == 1:
                    current_category = None 
                    continue
                else:
                    break
        elif choice == 1:
            if not shopping_cart:
                print("Cart empty.")
                time.sleep(0.5)
                continue
            items = list(shopping_cart.keys())
            idx = interactive_menu(items + ["Back"], "--- REMOVE WHICH ITEM? ---")
            if idx is not None and idx < len(items):
                del shopping_cart[items[idx]]
                print("Item removed.")
                time.sleep(0.5)
        elif choice == 2:
            if not shopping_cart:
                print("Cart empty.")
                time.sleep(0.5)
                continue
            cart_items = list(shopping_cart.keys())
            idx = interactive_menu(cart_items + ["Back"], "--- SELECT ITEM TO EDIT ---")
            if idx is not None and idx < len(cart_items):
                selected_item = cart_items[idx]
                available_stock = vending_db['items'][selected_item]['qty']
                qty = select_quantity(selected_item)
                if qty is not None:
                    if qty > available_stock:
                        print(f"Cannot set quantity to {qty}! Only {available_stock} available.")
                        time.sleep(1)
                        continue
                    shopping_cart[selected_item] = qty
                    print("Quantity updated!")
                    time.sleep(0.5)
        elif choice == 3:
            display_cart(shopping_cart)
        elif choice == 4:
            if shopping_cart:
                process_checkout(shopping_cart)
            return
        else:
            return

# Admin panel
def admin_access():
    current_session["user"] = None
    pw = masked_input("Owner/Admin Password: ")
    if pw != ADMIN_PASSWORD:
        print("Incorrect password.")
        time.sleep(0.5)
        return
    while True:
        choice = interactive_menu(
            ["Manage Items", "Sales Report", "Back"],
            "--- OWNER / ADMIN PANEL ---"
        )
        if choice == 0:
            sub = interactive_menu(
                ["Add Items", "Edit Item", "View Item Details", "Back"],
                "--- MANAGE ITEMS ---"
            )
            if sub == 0:
                admin_add_items()
            elif sub == 1:
                modify_item()
            elif sub == 2:
                show_item_details()
            else:
                return
        elif choice == 1:
            clear_screen()
            print("\033[96m--- SALES REPORT ---\033[0m")
            print("Total Revenue:", vending_db["revenue"])
            print("\nOrders:\n")
            for order in vending_db["orders"]:
                print(", ".join(f"{key}: {value}" for key, value in order.items()))
            input("\nPress ENTER...")
        else:
            return

# Main loop
def main():
    while True:
        clear_screen()
        if current_session["user"] is None:
            choice = interactive_menu(
                ["Login", "Signup", "Owner Panel", "Exit"],
                "=== VENDING MACHINE ==="
            )
            if choice == 0:
                user_login()
            elif choice == 1:
                user_signup()
            elif choice == 2:
                admin_access()
            else:
                return
        else:
            username = current_session["user"]
            choice = interactive_menu(
                ["Buy Items", "Delete My Account", "Logout"],
                f"=== WELCOME {username} ==="
            )
            if choice == 0:
                time.sleep(0.1)
                user_shopping()
            elif choice == 1:
                time.sleep(0.1)
                delete_account()
            else:
                current_session["user"] = None

main()
