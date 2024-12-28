# Desktop Application for Shopkeepers

## Overview
This project is a desktop application designed to simplify the daily operations of shopkeepers. The application allows shopkeepers to manage their inventory, process billing, and monitor sales through an intuitive interface.

---

## Features

1. **Product Management**:
   - Add new products with details such as name, price, and quantity.
   - Update stock levels as needed.

2. **Billing System**:
   - Generate bills for customers.
   - Automatically adjust stock levels after each sale.

3. **Sales Dashboard**:
   - View a detailed dashboard of daily, weekly, or monthly sales.
   - Analyze sales trends and performance.

---

## Project Structure

```
app/
|-- pages/
|   |-- 1_add_customer.py          # Add customer details
|   |-- 2_add_product.py           # Add products to inventory
|   |-- 3_view_products.py         # View and search products
|   |-- 4_update_stock.py          # Manage stock updates
|   |-- 5_create_order.py          # Process orders and generate bills
|   |-- 6_view_orders.py           # View all completed orders
|   |-- 7_sales_dashboard.py       # Display sales statistics
|-- db_utils.py                    # Database connection and utility functions
|-- home.py                        # Main entry point for the application

---
db-setup/
|-- db-schema.JPG                  # Visual representation of the database schema
|-- db-schema.mwb                  # MySQL Workbench schema file
|-- db-script.sql                  # SQL script to set up the database

.env                               # Environment variables file
requirements.txt                   # Python dependencies
```

---

## Prerequisites

1. **Python**: Ensure Python 3.8 or higher is installed on your system.
2. **Dependencies**: Install the required Python packages using:
   ```bash
   pip install -r requirements.txt
   ```
3. **Database**:
   - Use MySQL to set up the database.
   - Execute the `db-script.sql` file to initialize the required tables.

4. **Environment Variables**:
   - Create a `.env` file in the root directory with the following structure:
     ```env
     DB_HOST=your_database_host
     DB_USER=your_database_user
     DB_PASSWORD=your_database_password
     DB_DATABASE=your_database_name
     ```

---

## How to Run

1. Clone this repository to your local machine.
2. Navigate to the `app` directory:
   ```bash
   cd app
   ```
3. Launch the application:
   ```bash
  streamlit run home.py
   ```

---

## Usage

1. Start the application and navigate to the desired section:
   - Add products, update stock, or view inventory.
   - Generate customer bills under the "Create Order" section.
   - View sales reports in the "Sales Dashboard".
2. Ensure the database is connected and operational for seamless functionality.

---


## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact

For any issues or suggestions, feel free to reach out to the project maintainer.
