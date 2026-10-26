# JustVend — Advanced Vending Machine Simulator

A Python-based, terminal vending machine simulator that models the core flow of a real vending machine: account access, browsing products, managing a shopping cart, checkout, payments, receipts, and inventory administration.

Built by **Team JustVend** as a modular project using Python’s standard library and JSON-based storage, with `readchar` for keyboard-driven menu navigation.

## Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Using JustVend](#using-justvend)
- [Data Storage](#data-storage)
- [Implementation Highlights](#implementation-highlights)
- [Team](#team)
- [Future Improvements](#future-improvements)

## Features

### Customer experience
- **Sign up and log in** to access shopping features.
- **Masked password entry** displays asterisks while typing.
- **Browse by category** to find products more easily.
- **View product availability**, price, and stock quantity.
- **Manage a shopping cart** by adding items, changing quantities, removing items, and reviewing the total.
- **Checkout and payment validation**, including change calculation when the amount paid exceeds the total.
- **Digital receipts** generated for completed transactions.
- **Account management**, including account deletion and logout.

### Owner / admin controls
- **Inventory management:** add products in bulk and modify item details such as price, quantity, and category.
- **Stock monitoring** to help prevent purchases beyond available inventory.
- **Sales reports and revenue tracking.**
- **Order history** for reviewing transactions.
- **User management** through the administrative interface.

### Reliability and usability
- **Persistent JSON storage** for product, user, and transaction data.
- **Input validation and error handling** for common invalid operations.
- **Keyboard-driven menus** with interactive selection.
- **Automatic saving** of data changes.
- **Temporary-file-based saving** to help reduce the risk of corrupting data during writes.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and core functionality |
| `json` | Reading and writing persistent data |
| `os` | File-system operations |
| `datetime` | Order timestamps |
| `time` | Short delays for interface feedback |
| `readchar` | Character-by-character keyboard input and interactive navigation |

The project uses dictionaries, lists, modular functions, exception handling, input validation, and session state management.

## Project Structure

The project can be organised as follows:

```text
JustVend/
├── src/
│   └── vending_machine.py
├── data/
│   ├── vending_data.json
│   └── users.json
├── receipts/
│   └── receipt_*.txt
└── README.md
```

**Note:** The exact locations of generated JSON and receipt files depend on the paths configured in the code. Keep the paths consistent with your implementation.

## Getting Started

### Prerequisites

- Python 3.6 or later
- `pip` (or another way to install Python packages)
- A terminal that supports interactive keyboard input

### 1. Get the project

Clone your repository, or download and extract the project files.

```bash
git clone <your-repository-url>
cd JustVend
```

Replace `<your-repository-url>` with your actual Git repository URL.

### 2. Install the dependency

```bash
python3 -m pip install readchar
```

If `pip` is unavailable, install or configure it for your Python environment before running the application.

### 3. Run the application

If the main file is at `src/vending_machine.py`, run:

```bash
python3 src/vending_machine.py
```

If your file is in the project root instead, run:

```bash
python3 vending_machine.py
```

The application should open its main interactive menu in the terminal.

## Using JustVend

### Customer workflow

1. Start the application.
2. Choose **Sign up** to create an account, or **Login** if you already have one.
3. Browse the available product categories.
4. Select products and specify quantities.
5. Review and update your cart as needed.
6. Proceed to checkout and enter the payment amount.
7. Complete the transaction and review the generated receipt.
8. Log out when finished.

### Owner / admin workflow

1. Select **Owner Panel** from the main menu.
2. Enter the configured admin password.
3. Open the inventory-management options to add or modify products.
4. Review sales reports, revenue, and order history.
5. Return to the main menu when finished.

**Admin access:** The supplied project notes specify `JustVend` as the default admin password. If this value is still hard-coded in your implementation, change it before sharing or deploying the project. A hard-coded password is suitable only for a local demonstration, not a production system.

## Data Storage

JustVend uses JSON files to preserve application data between runs.

| File | Purpose |
|---|---|
| `vending_data.json` | Product inventory, categories, orders, revenue, and order count |
| `users.json` | User account data |
| `receipt_*.txt` | Text receipts generated for completed transactions |

The application can initialise data files when they do not exist, depending on the configured loading and saving logic.

**Tip:** Back up the JSON files before manually editing them. Keep the data structure consistent with what the program expects.

## Implementation Highlights

- **Modular design:** separate functions handle authentication, shopping, inventory, checkout, and administration.
- **Session management:** tracks the currently logged-in user during an application session.
- **Stock validation:** checks product availability before confirming quantities.
- **Transaction handling:** updates inventory and records orders after checkout.
- **Persistent state:** saves changes to JSON so data can be reused in later sessions.
- **Interactive terminal UI:** uses keyboard input to navigate menu options.

## Example Scenario

A customer logs in, selects two soft drinks priced at ₹30 each and one snack priced at ₹20, then proceeds to checkout.

| Item | Quantity | Unit price | Subtotal |
|---|---:|---:|---:|
| Soft drink | 2 | ₹30 | ₹60 |
| Snack | 1 | ₹20 | ₹20 |
| **Total** | **3** |  | **₹80** |

If the customer pays ₹100, the application calculates ₹20 in change, assuming the payment is accepted and the transaction completes successfully.

## Team

**Team Name:** JustVend  
**Project:** Advanced Vending Machine Simulator

| Team member | Register number | Contribution |
|---|---|---|
| Yash Mangal | BC2025118 | Core architecture, user authentication, and data persistence |
| Shubham Kuvad | BC2025052 | Shopping system, cart management, and user interface |
| Harsh Lotiya | BC2025038 | Inventory management, admin features, and payment system |

## Future Improvements

Possible next steps for the project include:

- Add automated tests for shopping, stock updates, and checkout edge cases.
- Improve credential security with password hashing and safer configuration.
- Add inventory low-stock alerts and exportable sales reports.
- Introduce clearer error messages and recovery for malformed JSON data.
- Add a configurable settings file for paths and administrative settings.

---

*JustVend is an educational simulator intended to demonstrate Python programming, file handling, data structures, modular design, and transaction workflows.*
