from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-in-production'

# Simple in-memory user storage
users_db = {}

class SimpleUser(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

# Add a default user
default_user = SimpleUser(1, 'Admin User', 'admin@stockmaster.com')
users_db[1] = default_user

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return users_db.get(int(user_id))

# Essential Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',
                         total_products=15,
                         low_stock=3,
                         pending_receipts=2,
                         pending_deliveries=1,
                         pending_transfers=0,
                         recent_activities=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Simple authentication - any email/password works for demo
        if email and password:
            # Create or get user
            user_id = len(users_db) + 1
            if email not in [user.email for user in users_db.values()]:
                new_user = SimpleUser(user_id, email.split('@')[0], email)
                users_db[user_id] = new_user
                user = new_user
            else:
                # Find existing user
                user = next((u for u in users_db.values() if u.email == email), None)
            
            if user:
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
        
        flash('Please enter both email and password', 'error')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Check if email already exists
        if any(user.email == email for user in users_db.values()):
            flash('Email already registered', 'error')
        else:
            user_id = len(users_db) + 1
            new_user = SimpleUser(user_id, name, email)
            users_db[user_id] = new_user
            
            login_user(new_user)
            flash('Registration successful!', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# PRODUCTS ROUTES
@app.route('/products')
@login_required
def products():
    return render_template('products/products.html', 
                         products=[], 
                         categories=[],
                         warehouses=[])

@app.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        # Handle form submission
        flash('Product added successfully! (Demo mode)', 'success')
        return redirect(url_for('products'))
    
    return render_template('products/add_product.html', categories=[])

@app.route('/operations/receipts')
@login_required
def receipts():
    print("📥 Receipts route accessed")  # Debug line
    return render_template('operations/receipts.html', 
                         receipts=[], 
                         products=[],
                         warehouses=[])

@app.route('/operations/delivery-orders')
@login_required
def delivery_orders():
    return render_template('operations/delivery_orders.html', 
                         delivery_orders=[],
                         products=[],
                         warehouses=[])

@app.route('/operations/internal-transfers')
@login_required
def internal_transfers():
    return render_template('operations/internal_transfers.html', 
                         transfers=[],
                         products=[],
                         warehouses=[])

@app.route('/operations/adjustments')
@login_required
def adjustments():
    return render_template('operations/adjustments.html', 
                         adjustments=[],
                         products=[],
                         warehouses=[])

# HISTORY ROUTES
@app.route('/move-history')
@login_required
def move_history():
    return render_template('move_history.html', movements=[])

# SETTINGS ROUTES
@app.route('/settings/warehouses')
@login_required
def warehouses():
    return render_template('settings/warehouses.html', warehouses=[])

@app.route('/settings/profile')
@login_required
def profile():
    return render_template('settings/profile.html', user=current_user)

# TEST ROUTES
@app.route('/test')
def test():
    return "Flask is working! All routes should work now."

@app.route('/debug-routes')
def debug_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'path': str(rule)
        })
    return {'routes': routes}

if __name__ == '__main__':
    print("🚀 Starting StockMaster (Complete Fixed Version)...")
    print("📧 Use any email/password to login")
    print("🌐 Available at: http://localhost:5000")
    print("🔧 Debug routes at: http://localhost:5000/debug-routes")
    app.run(debug=True, port=5000)