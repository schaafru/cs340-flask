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


@webapp.route('/weapon')
def weapon():
    cursor =  db_conn.cursor()
    cursor.execute("SELECT weapon_ID, order_ID, price FROM Weapon;")
    r = cursor.fetchall()
    print(r)
    return render_template('Weapon.html', rows=r)


@webapp.route('/orders')
def orders():
    cursor = db_conn.cursor()
    cursor.execute("SELECT order_ID, customer_ID, weapon_ID, currency, order_date FROM Orders;")
    r = cursor.fetchall()
    print(r)
    return render_template('Orders.html', rows=r)


@webapp.route('/stock')
def stock():
    cursor = db_conn.cursor()
    cursor.execute("SELECT total_number_of_items, number_of_items_available, weapon_ID, weapon_type FROM Stock;")
    r = cursor.fetchall()
    print(r)
    return render_template('Stock.html', rows=r)


@webapp.route('/customer', methods=['POST', 'GET'])
def customer():
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
        customer_ID = details['customer_ID']
        data = (name, address, customer_ID)
        cursor.execute("INSERT INTO Customer (name, address, customer_ID) VALUES (%s, %s, %s)", data)
        return render_template('Customer.html')

if __name__ == '__main__':
    webapp.run()
