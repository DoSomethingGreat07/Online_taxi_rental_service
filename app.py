# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_connection  # Assuming you have a database connection setup

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to the server!"

# -------------------- Manager APIs --------------------

@app.route('/manager/register', methods=['POST'])
def register_manager():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Manager (ssn, name, email) VALUES (%s, %s, %s)", (data['ssn'], data['name'], data['email']))
        conn.commit()
        return jsonify({'message': 'Manager registered successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/manager/login', methods=['POST'])
def login_manager():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Manager WHERE ssn = %s", (data['ssn'],))
        manager = cur.fetchone()
        if manager:
            manager_name = manager[1]  # assuming index 1 is name
            ssn = manager[0]           # assuming index 0 is SSN
            return jsonify({
                'success': True,
                'message': 'Manager login successful',
                'name': manager_name,
                'ssn': ssn
            })
        else:
            return jsonify({'success': False, 'error': 'Invalid SSN'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()


@app.route('/manager/remove_car', methods=['POST'])
def remove_car():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Car WHERE brand = %s", (data['brand'],))
        conn.commit()
        return jsonify({'message': 'Car removed'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/manager/add_car', methods=['POST'])
def add_car():
    data = request.get_json()
    brand = data.get('brand')
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Car (brand) VALUES (%s)", (brand,))
        conn.commit()
        return jsonify({"message": "Car added successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

# Add a Model
@app.route('/manager/add_model', methods=['POST'])
def add_model():
    data = request.get_json()
    car_id = data.get('car_id')
    color = data.get('color')
    construction_year = data.get('construction_year')
    transmission_type = data.get('transmission_type')
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Model (car_id, color, construction_year, transmission_type)
            VALUES (%s, %s, %s, %s)
        """, (car_id, color, construction_year, transmission_type))
        conn.commit()
        return jsonify({"message": "Model added successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

# Delete a Car
@app.route('/manager/delete_car', methods=['POST'])
def delete_car():
    data = request.get_json()
    car_id = data.get('car_id')
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Car WHERE car_id = %s", (car_id,))
        conn.commit()
        return jsonify({"message": "Car deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

# Delete a Model
@app.route('/manager/delete_model', methods=['POST'])
def delete_model():
    data = request.get_json()
    car_id = data.get('car_id')
    model_id = data.get('model_id')
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Model WHERE car_id = %s AND model_id = %s", (car_id, model_id))
        conn.commit()
        return jsonify({"message": "Model deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/manager/get_cars', methods=['GET'])
def get_cars():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT car_id, brand FROM Car ORDER BY car_id")
        cars = cur.fetchall()
        result = [{"car_id": row[0], "brand": row[1]} for row in cars]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/manager/view_models', methods=['GET'])
def view_models():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 
                Car.car_id,
                Model.model_id,
                Car.brand,
                Model.color,
                Model.construction_year,
                Model.transmission_type
            FROM 
                Car
            INNER JOIN 
                Model ON Car.car_id = Model.car_id
            ORDER BY 
                Car.car_id, Model.model_id
        """)
        models = cur.fetchall()
        result = []
        for row in models:
            result.append({
                "car_id": row[0],
                "model_id": row[1],
                "brand": row[2],
                "color": row[3],
                "construction_year": row[4],
                "transmission_type": row[5]
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()



@app.route('/manager/insert_address', methods=['POST'])
def insert_address():
    data = request.get_json()
    nameofroad = data.get('nameofroad')
    number = data.get('number')
    city = data.get('city')
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Address (nameofroad, number, city)
            VALUES (%s, %s, %s)
        """, (nameofroad, number, city))
        conn.commit()
        return jsonify({"message": "Address inserted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


@app.route('/manager/insert_driver', methods=['POST'])
def insert_driver():
    data = request.get_json()
    name = data.get('name')
    nameofroad = data.get('nameofroad')
    number = data.get('number')
    city = data.get('city')

    # Validate all required fields
    if not all([name, nameofroad, number, city]):
        return jsonify({"error": "All fields are required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    try:
        conn.autocommit = False  # Start transaction

        # 1. Insert address if not exists
        cur.execute("""
            INSERT INTO Address (nameofroad, number, city)
            VALUES (%s, %s, %s)
            ON CONFLICT (nameofroad, number, city) DO NOTHING
            RETURNING *
        """, (nameofroad, number, city))

        # 2. Insert driver (which references the address)
        cur.execute("""
            INSERT INTO Driver (name, nameofroad, number, city)
            VALUES (%s, %s, %s, %s)
        """, (name, nameofroad, number, city))

        conn.commit()

        return jsonify({
            "message": "Driver inserted successfully",
            "address_action": "Created new address" if cur.rowcount > 0 else "Used existing address"
        })

    except Exception as e:
        conn.rollback()
        return jsonify({
            "error": "Failed to insert driver",
            "details": str(e),
            "solution": "Check if driver already exists or address is valid"
        }), 400
    finally:
        cur.close()
        conn.close()



@app.route('/manager/delete_driver', methods=['POST'])
def delete_driver():
    data = request.get_json()
    name = data.get('name')
    
    # Validate input
    if not name or not isinstance(name, str):
        return jsonify({"error": "Valid driver name is required"}), 400
    
    conn = None
    cur = None
    try:
        conn = get_connection()
        if not conn:
            raise Exception("Database connection failed")
            
        cur = conn.cursor()
        
        # Start transaction
        conn.autocommit = False
        
        # Verify driver exists WITHIN the same transaction
        cur.execute("SELECT 1 FROM Driver WHERE name = %s FOR UPDATE", (name.strip(),))
        if not cur.fetchone():
            conn.rollback()
            return jsonify({"error": "Driver not found"}), 404
        
        # Check for active rentals
        cur.execute("""
            SELECT rent_id FROM Rent 
            WHERE name = %s AND rent_date >= CURRENT_DATE
            LIMIT 1
        """, (name.strip(),))
        if cur.fetchone():
            conn.rollback()
            return jsonify({
                "error": "Driver has active rentals",
                "solution": "Cancel rentals first"
            }), 400
        
        # Delete related records
        cur.execute("DELETE FROM Review WHERE name = %s", (name.strip(),))
        reviews_deleted = cur.rowcount
        
        cur.execute("DELETE FROM Driver_Model WHERE name = %s", (name.strip(),))
        models_unlinked = cur.rowcount
        
        cur.execute("DELETE FROM Rent WHERE name = %s", (name.strip(),))
        rentals_deleted = cur.rowcount
        
        # Delete driver
        cur.execute("DELETE FROM Driver WHERE name = %s", (name.strip(),))
        if cur.rowcount != 1:
            conn.rollback()
            return jsonify({
                "error": "Driver deletion failed",
                "details": {
                    "expected": 1,
                    "actual": cur.rowcount,
                    "possible_cause": "Driver was modified by another process"
                }
            }), 400
        
        conn.commit()
        
        return jsonify({
            "message": "Driver deleted successfully",
            "stats": {
                "reviews_deleted": reviews_deleted,
                "models_unlinked": models_unlinked,
                "rentals_canceled": rentals_deleted
            }
        })
        
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({
            "error": "Operation failed",
            "details": str(e),
            "solution": "Check database consistency"
        }), 500
        
    finally:
        if cur: cur.close()
        if conn: conn.close()

@app.route('/manager/top_k_clients', methods=['GET'])
def top_k_clients():
    k = request.args.get('k', type=int)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, c.email_address, COUNT(r.rent_id) AS rent_count
        FROM Client c
        JOIN Rent r ON c.email_address = r.client_email
        GROUP BY c.name, c.email_address
        ORDER BY rent_count DESC
        LIMIT %s
    """, (k,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    results = [{'name': row[0], 'email': row[1], 'rent_count': row[2]} for row in rows]
    return jsonify(results), 200

@app.route('/manager/model_usage', methods=['GET'])
def model_usage():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.model_id, m.color, m.construction_year, COUNT(r.rent_id) AS times_rented
        FROM Model m
        LEFT JOIN Rent r ON m.model_id = r.model_id
        GROUP BY m.model_id, m.color, m.construction_year
        ORDER BY times_rented DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    results = [{'model_id': row[0], 'color': row[1], 'year': row[2], 'times_rented': row[3]} for row in rows]
    return jsonify(results), 200

@app.route('/manager/driver_stats', methods=['GET'])
def driver_stats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.name, COUNT(r.rent_id) AS total_rents, 
               ROUND(AVG(rv.rating), 2) AS avg_rating
        FROM Driver d
        LEFT JOIN Rent r ON d.name = r.name
        LEFT JOIN Review rv ON d.name = rv.name
        GROUP BY d.name
        ORDER BY total_rents DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    results = [{'name': row[0], 'total_rents': row[1], 'avg_rating': float(row[2]) if row[2] else None} for row in rows]
    return jsonify(results), 200


@app.route('/manager/clients_by_city', methods=['GET'])
def clients_by_city():
    c1 = request.args.get('c1')
    c2 = request.args.get('c2')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT cl.name, cl.email_address
        FROM Client cl
        JOIN Client_Address ca ON cl.email_address = ca.client_email
        JOIN Rent r ON cl.email_address = r.client_email
        JOIN Driver d ON r.name = d.name
        WHERE ca.city = %s AND d.city = %s
    """, (c1, c2))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = [{'name': row[0], 'email': row[1]} for row in rows]
    return jsonify(result), 200


# -------------------- Driver APIs --------------------

@app.route('/driver/login', methods=['POST'])
def driver_login():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Driver WHERE name = %s", (data['name'],))
        driver = cur.fetchone()
        if driver:
            return jsonify({'message': 'Driver login successful'})
        else:
            return jsonify({'error': 'Invalid driver name'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/driver/update_driver_address', methods=['POST'])
def update_driver_address():
    data = request.get_json()
    name = data.get('name')
    new_nameofroad = data.get('nameofroad')
    new_number = data.get('number')
    new_city = data.get('city')
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Check if the address exists
        cur.execute("""
            SELECT * FROM Address
            WHERE nameofroad = %s AND number = %s AND city = %s
        """, (new_nameofroad, new_number, new_city))
        address_exists = cur.fetchone()

        # If not, insert the new address
        if not address_exists:
            cur.execute("""
                INSERT INTO Address (nameofroad, number, city)
                VALUES (%s, %s, %s)
            """, (new_nameofroad, new_number, new_city))

        # Now update the driver's address
        cur.execute("""
            UPDATE Driver
            SET nameofroad = %s, number = %s, city = %s
            WHERE name = %s
        """, (new_nameofroad, new_number, new_city, name))

        if cur.rowcount == 0:
            conn.rollback()
            return jsonify({"error": "Driver not found."}), 404

        conn.commit()
        return jsonify({"message": "Driver address updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


@app.route('/driver/list_models', methods=['GET'])
def list_models():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Model")
        models = cur.fetchall()
        return jsonify(models)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/driver/view_driver_models', methods=['GET'])
def view_driver_models():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT 
                c.car_id,
                m.model_id,
                c.brand,
                m.color,
                m.construction_year,
                m.transmission_type
            FROM Model m
            JOIN Car c ON m.car_id = c.car_id
            ORDER BY c.car_id, m.model_id
        """)
        rows = cur.fetchall()
        result = [{
            "car_id": r[0],
            "model_id": r[1],
            "brand": r[2],
            "color": r[3],
            "construction_year": r[4],
            "transmission_type": r[5]
        } for r in rows]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


@app.route('/driver/declare_driver_model', methods=['POST'])
def declare_driver_model():
    data = request.get_json()
    driver_name = data.get('driver_name')
    model_id = data.get('model_id')
    car_id = data.get('car_id')

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Driver_Model (name, model_id, car_id)
            VALUES (%s, %s, %s)
        """, (driver_name, model_id, car_id))
        conn.commit()
        return jsonify({"message": "Driver model declaration added successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

# -------------------- Client APIs --------------------

@app.route('/client/register', methods=['POST'])
def register_client():
    data = request.get_json()
    email_address = data.get('email_address')
    name = data.get('name')
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Client (email_address, name)
            VALUES (%s, %s)
        """, (email_address, name))
        conn.commit()
        return jsonify({"message": "Client registered successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


@app.route('/client/add_address', methods=['POST'])
def add_client_address():
    data = request.get_json()
    print("Received address data:", data)  # Debug logging
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    required_fields = ['client_email', 'nameofroad', 'number', 'city']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    conn = get_connection()
    cur = conn.cursor()
    try:
        conn.autocommit = False
        
        # 1. Insert address if not exists
        cur.execute("""
            INSERT INTO Address (nameofroad, number, city)
            VALUES (%s, %s, %s)
            ON CONFLICT (nameofroad, number, city) DO NOTHING
        """, (data['nameofroad'], data['number'], data['city']))
        
        # 2. Link to client
        cur.execute("""
            INSERT INTO Client_Address (client_email, nameofroad, number, city)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (client_email, nameofroad, number, city) DO NOTHING
            RETURNING *
        """, (data['client_email'], data['nameofroad'], data['number'], data['city']))
        
        conn.commit()
        
        if cur.rowcount > 0:
            return jsonify({"message": "Address linked successfully"})
        else:
            return jsonify({"message": "Address was already linked to client"})
            
    except Exception as e:
        conn.rollback()
        print("Error in add_address:", str(e))
        return jsonify({
            "error": "Failed to process address",
            "details": str(e)
        }), 400
    finally:
        cur.close()
        conn.close()

@app.route('/client/add_creditcard', methods=['POST'])
def add_credit_card():
    data = request.get_json()
    ccnum = data.get('ccnum')
    client_email = data.get('client_email')
    nameofroad = data.get('nameofroad')
    number = data.get('number')
    city = data.get('city')

    conn = get_connection()
    cur = conn.cursor()
    try:
        # Check if address exists
        cur.execute("""
            SELECT * FROM Address WHERE nameofroad = %s AND number = %s AND city = %s
        """, (nameofroad, number, city))
        address = cur.fetchone()

        # If not, insert the address
        if not address:
            cur.execute("""
                INSERT INTO Address (nameofroad, number, city)
                VALUES (%s, %s, %s)
            """, (nameofroad, number, city))

        # Now insert the credit card linked to the address
        cur.execute("""
            INSERT INTO CreditCard (ccnum, client_email, nameofroad, number, city)
            VALUES (%s, %s, %s, %s, %s)
        """, (ccnum, client_email, nameofroad, number, city))

        conn.commit()
        return jsonify({"message": "Credit card added successfully, address linked to the credit card"})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


@app.route('/client/login', methods=['POST'])
def client_login():
    data = request.get_json()
    email_address = data.get('email_address')  # match frontend key

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Client WHERE email_address = %s", (email_address,))
        client = cur.fetchone()

        if client:
            client_name = client[1]  # assuming column 1 is name
            return jsonify({
                'success': True,
                'message': 'Client login successful',
                'name': client_name
            })
        else:
            return jsonify({'success': False, 'error': 'Invalid client email'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()





@app.route('/client/view_available_models', methods=['POST'])
def view_available_models():
    data = request.get_json()
    rent_date = data.get('rent_date')  # expecting format 'YYYY-MM-DD'
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT DISTINCT m.model_id, m.car_id, c.brand, m.color, m.construction_year, m.transmission_type
            FROM Model m
            JOIN Car c ON m.car_id = c.car_id
            WHERE NOT EXISTS (
                SELECT 1
                FROM Rent r1
                WHERE r1.model_id = m.model_id AND r1.car_id = m.car_id
                  AND r1.rent_date = %s
            )
            AND EXISTS (
                SELECT 1
                FROM Driver_Model dm
                WHERE dm.model_id = m.model_id AND dm.car_id = m.car_id
                  AND NOT EXISTS (
                    SELECT 1
                    FROM Rent r2
                    WHERE r2.name = dm.name
                      AND r2.rent_date = %s
                  )
            )
        """, (rent_date, rent_date))
        
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append({
                "model_id": row[0],
                "car_id": row[1],
                "brand": row[2],
                "color": row[3],
                "construction_year": row[4],
                "transmission_type": row[5]
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


@app.route('/client/book_rent', methods=['POST'])
def book_rent():
    data = request.get_json()
    rent_date = data.get('rent_date')
    client_email = data.get('client_email')
    model_id = data.get('model_id')
    car_id = data.get('car_id')
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Step 1: Check if model is available
        cur.execute("""
            SELECT 1
            FROM Model m
            WHERE m.model_id = %s AND m.car_id = %s
              AND NOT EXISTS (
                  SELECT 1 FROM Rent r
                  WHERE r.model_id = m.model_id AND r.car_id = m.car_id
                    AND r.rent_date = %s
              )
        """, (model_id, car_id, rent_date))
        model_available = cur.fetchone()

        if not model_available:
            return jsonify({"error": "Car model is not available on selected date"}), 400

        # Step 2: Find an available driver who can drive it
        cur.execute("""
            SELECT dm.name
            FROM Driver_Model dm
            WHERE dm.model_id = %s AND dm.car_id = %s
              AND NOT EXISTS (
                  SELECT 1 FROM Rent r
                  WHERE r.name = dm.name
                    AND r.rent_date = %s
              )
            LIMIT 1
        """, (model_id, car_id, rent_date))
        driver = cur.fetchone()

        if not driver:
            return jsonify({"error": "No available driver for this model on selected date"}), 400

        driver_name = driver[0]

        # Step 3: Insert rent
        cur.execute("""
            INSERT INTO Rent (rent_date, client_email, name, model_id, car_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (rent_date, client_email, driver_name, model_id, car_id))

        conn.commit()
        return jsonify({"message": f"Rent booked successfully! Driver assigned: {driver_name}"})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


@app.route('/client/view_rents', methods=['POST'])
def view_client_rents():
    data = request.get_json()
    client_email = data.get('client_email')

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT r.rent_id, r.rent_date, r.name AS driver_name,
                   c.brand, m.model_id, m.color, m.construction_year, m.transmission_type
            FROM Rent r
            JOIN Model m ON r.model_id = m.model_id AND r.car_id = m.car_id
            JOIN Car c ON m.car_id = c.car_id
            WHERE r.client_email = %s
            ORDER BY r.rent_date DESC
        """, (client_email,))
        
        rents = cur.fetchall()
        result = []
        for row in rents:
            result.append({
                "rent_id": row[0],
                "rent_date": row[1].strftime("%Y-%m-%d"),
                "driver_name": row[2],
                "brand": row[3],
                "model_id": row[4],
                "color": row[5],
                "construction_year": row[6],
                "transmission_type": row[7]
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


@app.route('/client/add_review', methods=['POST'])
def add_review():
    data = request.get_json()
    client_email = data.get('client_email')
    driver_name = data.get('driver_name')
    message = data.get('message')
    rating = data.get('rating')

    conn = get_connection()
    cur = conn.cursor()
    try:
        # Step 1: Check if client rented this driver before
        cur.execute("""
            SELECT 1
            FROM Rent
            WHERE client_email = %s
              AND name = %s
            LIMIT 1
        """, (client_email, driver_name))
        rent_exists = cur.fetchone()

        if not rent_exists:
            return jsonify({"error": "You cannot review this driver. No previous rent found."}), 400

        # Step 2: Insert review
        cur.execute("""
            INSERT INTO Review (name, client_email, message, rating)
            VALUES (%s, %s, %s, %s)
        """, (driver_name, client_email, message, rating))

        conn.commit()
        return jsonify({"message": "Review added successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    print("✅ Server is running fine at http://127.0.0.1:5050 🚀")
    app.run(debug=True, port=5050)
