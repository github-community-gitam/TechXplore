from flask import Flask, render_template, request, redirect, url_for
import pymysql
import config

app = Flask(__name__)

# MySQL connection function
def get_db_connection():
    connection = pymysql.connect(
        host=config.Config.MYSQL_HOST,
        user=config.Config.MYSQL_USER,
        password=config.Config.MYSQL_PASSWORD,
        database=config.Config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Step 1: Select source and destination
@app.route('/')
def index():
    connection = get_db_connection()
    with connection.cursor() as cur:
        # Fetch unique sources and destinations from the database
        cur.execute("SELECT DISTINCT source FROM ev_buses")
        sources = cur.fetchall()

        cur.execute("SELECT DISTINCT destination FROM ev_buses")
        destinations = cur.fetchall()
    connection.close()

    return render_template('index.html', sources=sources, destinations=destinations)

# Step 2: Show available buses based on source, destination, and date
@app.route('/search_buses', methods=['POST'])
def search_buses():
    source = request.form['source']
    destination = request.form['destination']

    connection = get_db_connection()
    with connection.cursor() as cur:
        # Query to get available buses between selected source and destination
        query = '''
            SELECT id, bus_name, available_seats FROM ev_buses
            WHERE source = %s AND destination = %s
        '''
        cur.execute(query, (source, destination))
        buses = cur.fetchall()
    connection.close()

    # Render available buses with their names and seat availability
    return render_template('available_buses.html', buses=buses, source=source, destination=destination)

# Step 3: Book a seat on a selected bus
@app.route('/book', methods=['POST'])
def book():
    bus_id = request.form['bus_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    mobile_number = request.form['mobile_number']
    seats_booked = int(request.form['seats_booked'])

    connection = get_db_connection()
    with connection.cursor() as cur:
        # Check if enough seats are available
        cur.execute("SELECT available_seats FROM ev_buses WHERE id = %s", (bus_id,))
        available_seats = cur.fetchone()['available_seats']

        if available_seats >= seats_booked:
            # Insert booking into the bookings table
            cur.execute(
                "INSERT INTO bookings (bus_id, first_name, last_name, mobile_number, seats_booked, booking_date) "
                "VALUES (%s, %s, %s, %s, %s, CURDATE())",
                (bus_id, first_name, last_name, mobile_number, seats_booked)
            )

            # Update the available seats in the ev_buses table
            cur.execute(
                "UPDATE ev_buses SET available_seats = available_seats - %s WHERE id = %s",
                (seats_booked, bus_id)
            )

            connection.commit()
            connection.close()

            # Pass the first name, bus ID, and seats booked to the success page
            return render_template('success.html', first_name=first_name, bus_id=bus_id, seats_booked=seats_booked)
        else:
            connection.close()
            return "Not enough seats available", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
