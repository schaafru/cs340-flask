import MySQLdb.cursors
from flask import render_template, request
import flask
import configparser


def read_mysql_config(mysql_config_file_name: str):
    config = configparser.ConfigParser()
    config.read(mysql_config_file_name)
    return dict(config['client'])


config_info = read_mysql_config("../.my.cnf")

db_conn = MySQLdb.connect(config_info['host'],
                          config_info['user'],
                          config_info['password'],
                          config_info['database'])

webapp = flask.Flask(__name__, static_url_path='/static')


@webapp.route('/')
def home():
    return render_template('Home.html')


@webapp.route('/weapon/')
def weapon():
    return render_template('Weapon.html')


@webapp.route('/weapon', methods=['POST', 'GET'])
def weapon_result():
    cursor =  db_conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT weapon_ID, order_ID, price FROM Weapon;")
        r = cursor.fetchall()
        print(r)
        return render_template('Weapon.html', rows=r)

    elif request.method == "POST":
        cursor = db_conn.cursor()
        details = request.form
        currency = details['currency']
        customer_ID = details['customer_ID']
        order_date = details['order_date']
        order_ID = details['order_ID']
        weapon_ID = details['weapon_ID']
        data = (currency, customer_ID, order_date, order_ID, weapon_ID)
        cursor.execute("INSERT INTO Weapon (currency, customer_ID, order_date, order_ID, weapon_ID) VALUES "
                       "(%s, %s, %s, %s, %s)", data)
        db_conn.commit()
        return render_template('Weapon.html')


@webapp.route('/orders/')
def orders():
    return render_template('Orders.html')


@webapp.route('/orders', methods=['POST', 'GET'])
def order_results():
    cursor = db_conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT order_ID, customer_ID, weapon_ID, currency, order_date FROM Orders;")
        r = cursor.fetchall()
        print(r)
        return render_template('Orders.html', rows=r)

    elif request.method == "POST":
        cursor = db_conn.cursor()
        details = request.form
        order_ID = details['order_ID']
        price = details['price']
        weapon_ID = details['weapon_ID']
        currency = details['currency']
        order_date = details['order_date']
        data = (order_ID, price, weapon_ID, currency, order_date)
        cursor.execute("INSERT INTO Orders (order_ID, price, weapon_ID) VALUES (%s, %s, %s, %s, %s)", data)
        db_conn.commit()
        return render_template('Orders.html')


@webapp.route('/stock', methods=['POST', 'GET'])
def stock():
    cursor = db_conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT number_of_items_available, total_number_of_items, weapon_ID, weapon_type FROM Stock;")
        r = cursor.fetchall()
        print(r)
        return render_template('Stock.html', rows=r)

    elif request.method == "POST":
        cursor = db_conn.cursor()
        details = request.form
        number_of_items_available = details['number_of_items_available']
        total_number_of_items = details['total_number_of_items']
        weapon_ID = details['weapon_ID']
        weapon_type = details['weapon_type']
        data = (number_of_items_available, total_number_of_items, weapon_ID, weapon_type)
        cursor.execute("INSERT INTO Stock (number_of_items_available, total_number_of_items, weapon_ID, weapon_type) "
                       "VALUES (%s, %s, %s, %s)", data)
        db_conn.commit()
        return render_template('Stock.html')


@webapp.route('/customer/')
def customer():
    return render_template('Customer.html')


@webapp.route('/customer', methods=['POST', 'GET'])
def customer_results():
    cursor = db_conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT name, address, customer_ID FROM Customer;")
        r = cursor.fetchall()
        print(r)
        return render_template('Customer.html', rows=r)

    elif request.method == "POST":
        cursor = db_conn.cursor()
        details = request.form
        name = details['name']
        address = details['address']
        # customer_ID = details['customer_ID']
        data = (name, address)
        cursor.execute("INSERT INTO Customer (name, address) VALUES (%s, %s)", data)
        db_conn.commit()
        return render_template('Customer.html')


if __name__ == '__main__':
    webapp.run()
