from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import current_app

mysql = MySQL()

def init_db(app):
    mysql.init_app(app)
    
    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role ENUM('manager', 'staff') DEFAULT 'staff',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create warehouses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS warehouses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    location VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create product_categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS product_categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT
                )
            ''')
            
            # Create products table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    sku VARCHAR(100) UNIQUE NOT NULL,
                    category_id INT,
                    unit_of_measure VARCHAR(50),
                    description TEXT,
                    min_stock_level INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES product_categories(id)
                )
            ''')
            
            # Create stock table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    warehouse_id INT NOT NULL,
                    quantity INT DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id),
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
                    UNIQUE KEY unique_product_warehouse (product_id, warehouse_id)
                )
            ''')
            
            # Create receipts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS receipts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    reference VARCHAR(100) UNIQUE NOT NULL,
                    supplier VARCHAR(255),
                    status ENUM('draft', 'waiting', 'ready', 'done', 'canceled') DEFAULT 'draft',
                    created_by INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users(id)
                )
            ''')
            
            # Create receipt_items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS receipt_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    receipt_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL,
                    warehouse_id INT NOT NULL,
                    FOREIGN KEY (receipt_id) REFERENCES receipts(id),
                    FOREIGN KEY (product_id) REFERENCES products(id),
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
                )
            ''')
            
            # Create delivery_orders table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS delivery_orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    reference VARCHAR(100) UNIQUE NOT NULL,
                    customer VARCHAR(255),
                    status ENUM('draft', 'waiting', 'ready', 'done', 'canceled') DEFAULT 'draft',
                    created_by INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users(id)
                )
            ''')
            
            # Create delivery_order_items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS delivery_order_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    delivery_order_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL,
                    warehouse_id INT NOT NULL,
                    FOREIGN KEY (delivery_order_id) REFERENCES delivery_orders(id),
                    FOREIGN KEY (product_id) REFERENCES products(id),
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
                )
            ''')
            
            # Create internal_transfers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS internal_transfers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    reference VARCHAR(100) UNIQUE NOT NULL,
                    from_warehouse_id INT NOT NULL,
                    to_warehouse_id INT NOT NULL,
                    status ENUM('draft', 'waiting', 'ready', 'done', 'canceled') DEFAULT 'draft',
                    created_by INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (from_warehouse_id) REFERENCES warehouses(id),
                    FOREIGN KEY (to_warehouse_id) REFERENCES warehouses(id),
                    FOREIGN KEY (created_by) REFERENCES users(id)
                )
            ''')
            
            # Create internal_transfer_items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS internal_transfer_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    transfer_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL,
                    FOREIGN KEY (transfer_id) REFERENCES internal_transfers(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            ''')
            
            # Create stock_adjustments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock_adjustments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    reference VARCHAR(100) UNIQUE NOT NULL,
                    reason TEXT,
                    created_by INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users(id)
                )
            ''')
            
            # Create stock_adjustment_items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock_adjustment_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    adjustment_id INT NOT NULL,
                    product_id INT NOT NULL,
                    warehouse_id INT NOT NULL,
                    quantity_before INT NOT NULL,
                    quantity_after INT NOT NULL,
                    FOREIGN KEY (adjustment_id) REFERENCES stock_adjustments(id),
                    FOREIGN KEY (product_id) REFERENCES products(id),
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
                )
            ''')
            
            # Create stock_movements table (for history)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock_movements (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    warehouse_id INT NOT NULL,
                    movement_type ENUM('receipt', 'delivery', 'transfer', 'adjustment'),
                    reference_id INT,
                    quantity_change INT NOT NULL,
                    quantity_after INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id),
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
                )
            ''')
            
            mysql.connection.commit()
            cursor.close()
            print("✅ Database tables created successfully!")
            
    except Exception as e:
        print(f"❌ Database initialization error: {str(e)}")
        raise e