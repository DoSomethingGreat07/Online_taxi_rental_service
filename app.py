# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_connection  # Assuming you have a database connection setup

app = Flask(__name__)
CORS(app)

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
            return jsonify({'message': 'Manager login successful'})
        else:
            return jsonify({'error': 'Invalid SSN'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/manager/insert_car', methods=['POST'])
def insert_car():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Car (brand) VALUES (%s)", (data['brand'],))
        conn.commit()
        return jsonify({'message': 'Car inserted'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
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

@app.route('/manager/insert_driver', methods=['POST'])
def insert_driver():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Address (nameofroad, number, city) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", (data['nameofroad'], data['number'], data['city']))
        cur.execute("INSERT INTO Driver (name, nameofroad, number, city) VALUES (%s, %s, %s, %s)", (data['name'], data['nameofroad'], data['number'], data['city']))
        conn.commit()
        return jsonify({'message': 'Driver inserted'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/manager/remove_driver', methods=['POST'])
def remove_driver():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Driver WHERE name = %s", (data['name'],))
        conn.commit()
        return jsonify({'message': 'Driver removed'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/manager/top_k_clients', methods=['POST'])
def top_k_clients():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT Client.name, Client.email_address
            FROM Client
            JOIN Rent ON Client.email_address = Rent.client_email
            GROUP BY Client.email_address
            ORDER BY COUNT(Rent.rent_id) DESC
            LIMIT %s
        """, (data['k'],))
        clients = cur.fetchall()
        return jsonify(clients)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/manager/cars_rent_count', methods=['GET'])
def cars_rent_count():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT Model.model_id, COUNT(Rent.rent_id)
            FROM Model
            LEFT JOIN Rent ON Model.model_id = Rent.model_id
            GROUP BY Model.model_id
        """)
        models = cur.fetchall()
        return jsonify(models)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/manager/driver_stats', methods=['GET'])
def driver_stats():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT Driver.name, COUNT(Rent.rent_id), AVG(Review.rating)
            FROM Driver
            LEFT JOIN Rent ON Driver.name = Rent.name
            LEFT JOIN Review ON Driver.name = Review.name
            GROUP BY Driver.name
        """)
        stats = cur.fetchall()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/manager/clients_by_city', methods=['POST'])
def clients_by_city():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT DISTINCT Client.name, Client.email_address
            FROM Client
            JOIN Client_Address CA ON Client.email_address = CA.client_email
            JOIN Rent ON Client.email_address = Rent.client_email
            JOIN Driver ON Rent.name = Driver.name
            WHERE CA.city = %s AND Driver.city = %s
        """, (data['city1'], data['city2']))
        clients = cur.fetchall()
        return jsonify(clients)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

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

@app.route('/driver/update_address', methods=['POST'])
def driver_update_address():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE Driver SET nameofroad=%s, number=%s, city=%s WHERE name=%s", (data['nameofroad'], data['number'], data['city'], data['name']))
        conn.commit()
        return jsonify({'message': 'Address updated'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
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

@app.route('/driver/declare_model', methods=['POST'])
def declare_model():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Driver_Model (name, model_id, car_id) VALUES (%s, %s, %s)", (data['name'], data['model_id'], data['car_id']))
        conn.commit()
        return jsonify({'message': 'Model declared'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()
# -------------------- Client APIs --------------------

@app.route('/client/register', methods=['POST'])
def client_register():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Insert client
        cur.execute("INSERT INTO Client (email_address, name) VALUES (%s, %s)", (data['email'], data['name']))

        # Insert addresses
        for address in data.get('addresses', []):
            cur.execute("INSERT INTO Address (nameofroad, number, city) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", (address['nameofroad'], address['number'], address['city']))
            cur.execute("INSERT INTO Client_Address (client_email, nameofroad, number, city) VALUES (%s, %s, %s, %s)", (data['email'], address['nameofroad'], address['number'], address['city']))

        # Insert credit cards
        for card in data.get('credit_cards', []):
            cur.execute("INSERT INTO CreditCard (ccnum, client_email, nameofroad, number, city) VALUES (%s, %s, %s, %s, %s)", (card['ccnum'], data['email'], card['nameofroad'], card['number'], card['city']))

        conn.commit()
        return jsonify({'message': 'Client registered successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/client/login', methods=['POST'])
def client_login():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM Client WHERE email_address = %s", (data['email'],))
        client = cur.fetchone()
        if client:
            return jsonify({'message': 'Client login successful', 'email_address': client[0]})
        else:
            return jsonify({'error': 'Invalid email'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/client/available_cars', methods=['POST'])
def available_cars():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        date = data['date']
        cur.execute("""
            SELECT DISTINCT Model.model_id, Car.brand, Model.color, Model.construction_year, Model.transmission_type
            FROM Model
            JOIN Car ON Model.car_id = Car.car_id
            WHERE (Model.model_id, Model.car_id) NOT IN (
                SELECT model_id, car_id FROM Rent WHERE rent_date = %s
            )
        """, (date,))
        cars = cur.fetchall()
        return jsonify(cars)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/client/book_rent', methods=['POST'])
def book_rent():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Find a driver who can drive the model and is available
        cur.execute("""
            SELECT name FROM Driver_Model
            WHERE model_id = %s AND car_id = %s
            AND name NOT IN (SELECT name FROM Rent WHERE rent_date = %s)
            LIMIT 1
        """, (data['model_id'], data['car_id'], data['date']))
        driver = cur.fetchone()
        if not driver:
            return jsonify({'error': 'No available driver for this car model on the given date'}), 400

        driver_name = driver[0]

        # Insert into Rent
        cur.execute("""
            INSERT INTO Rent (rent_date, client_email, name, model_id, car_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['date'], data['client_email'], driver_name, data['model_id'], data['car_id']))

        conn.commit()
        return jsonify({'message': 'Rent booked successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/client/my_rents', methods=['POST'])
def my_rents():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT Rent.rent_date, Car.brand, Model.color, Driver.name
            FROM Rent
            JOIN Car ON Rent.car_id = Car.car_id
            JOIN Model ON Rent.model_id = Model.model_id
            JOIN Driver ON Rent.name = Driver.name
            WHERE Rent.client_email = %s
        """, (data['client_email'],))
        rents = cur.fetchall()
        return jsonify(rents)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/client/leave_review', methods=['POST'])
def leave_review():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Validate if driver served the client
        cur.execute("""
            SELECT 1 FROM Rent
            WHERE client_email = %s AND name = %s
        """, (data['client_email'], data['driver_name']))
        assignment = cur.fetchone()

        if not assignment:
            return jsonify({'error': 'Driver was never assigned to client'}), 400

        cur.execute("""
            INSERT INTO Review (name, client_email, message, rating)
            VALUES (%s, %s, %s, %s)
        """, (data['driver_name'], data['client_email'], data.get('message', ''), data['rating']))

        conn.commit()
        return jsonify({'message': 'Review submitted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5050)
