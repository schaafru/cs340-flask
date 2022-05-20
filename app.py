import MySQLdb.cursors
from flask import render_template
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


@webapp.route('/customer')
def customer():
    cursor = db_conn.cursor()
    cursor.execute("SELECT name, address, customer_ID FROM Customer;")
    r = cursor.fetchall()
    print(r)
    return render_template('Customer.html', rows=r)


if __name__ == '__main__':
    webapp.run()
