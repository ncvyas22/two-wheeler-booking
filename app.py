from flask import Flask, render_template_string, request
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    while True:
        try:
            return mysql.connector.connect(
                host=os.environ.get("DB_HOST", "mysql-db"),
                user=os.environ.get("DB_USER", "root"),
                password=os.environ.get("DB_PASSWORD", "RootPassword2026"),
                database=os.environ.get("DB_NAME", "twowheeler_db")
            )
        except mysql.connector.Error:
            time.sleep(2)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(100),
            address TEXT,
            phone VARCHAR(20),
            scooter_model VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Apex Rentals - Docker Compose Demo</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; display: flex; justify-content: center; padding: 40px; }
        .card { background: #1e293b; padding: 30px; border-radius: 12px; width: 450px; box-shadow: 0 10px 20px rgba(0,0,0,0.4); }
        h2 { color: #38bdf8; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-size: 0.9em; color: #94a3b8; }
        input, select { width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: #fff; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #22c55e; border: none; border-radius: 6px; color: #fff; font-weight: bold; cursor: pointer; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Two-Wheeler [Live Choice Demo] [Choice-1 Staging Update] [Build-2: v2.0 Ahmedabad Edition] Live CI - Ahmedabad/CD Live CI/CD Booking (Compose Stack)</h2>
        <form action="/add" method="POST">
            <div class="form-group"><label>Customer Name</label><input type="text" name="name" placeholder="Rahul Sharma" required></div>
            <div class="form-group"><label>Address</label><input type="text" name="address" placeholder="45 SG Highway, Ahmedabad" required></div>
            <div class="form-group"><label>Telephone Number</label><input type="text" name="phone" placeholder="9876543210" required></div>
            <div class="form-group">
                <label>Scooter Model</label>
                <select name="model">
                    <option value="Activa 6G">Activa 6G</option>
                    <option value="Ather 450X">Ather 450X</option>
                    <option value="TVS iQube">TVS iQube</option>
                </select>
            </div>
            <button type="submit">Save Booking to MySQL</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/add', methods=['POST'])
def add_booking():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO bookings (customer_name, address, phone, scooter_model) VALUES (%s, %s, %s, %s)',
        (request.form['name'], request.form['address'], request.form['phone'], request.form['model'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return '<body style="background:#0f172a;color:#22c55e;font-family:sans-serif;text-align:center;padding:50px;"><h2>Booking Saved via Docker Compose!</h2><a href="/" style="color:#38bdf8;">Add Another</a></body>'

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
