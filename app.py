import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random 24-byte string each time the app starts

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='rohit!@#',
        database='flight_booking_db'
    )
    return connection

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM flights')
    flights = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', flights=flights)

@app.route('/add', methods=['GET', 'POST'])
def add_flight():
    if request.method == 'POST':
        flight_number = request.form['flight_number']
        source = request.form['source']
        destination = request.form['destination']
        departure_time = request.form['departure_time']
        arrival_time = request.form['arrival_time']
        price = request.form['price']
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute('INSERT INTO flights (flight_number, source, destination, departure_time, arrival_time, price) VALUES (%s, %s, %s, %s, %s, %s)', 
                           (flight_number, source, destination, departure_time, arrival_time, price))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                flash('Error: Flight number already exists.')
            else:
                flash(f'Error: {err}')
    return render_template('add_flight.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_flight(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM flights WHERE id = %s', (id,))
    flight = cursor.fetchone()
    cursor.close()
    connection.close()
    if request.method == 'POST':
        flight_number = request.form['flight_number']
        source = request.form['source']
        destination = request.form['destination']
        departure_time = request.form['departure_time']
        arrival_time = request.form['arrival_time']
        price = request.form['price']
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute('UPDATE flights SET flight_number = %s, source = %s, destination = %s, departure_time = %s, arrival_time = %s, price = %s WHERE id = %s', 
                           (flight_number, source, destination, departure_time, arrival_time, price, id))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                flash('Error: Flight number already exists.')
            else:
                flash(f'Error: {err}')
    return render_template('update_flight.html', flight=flight)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_flight(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM flights WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)