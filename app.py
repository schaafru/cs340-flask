import MySQLdb, MySQLdb.cursors, os
from flask import render_template, request
import flask
import configparser


def read_config_section(config_file_name: str,
                        section: str) -> dict:
    config = configparser.ConfigParser()
    config.read(config_file_name)
    return dict(config[section if section is not None else 'client'])


mysql_config = read_config_section(os.path.join(os.path.expanduser("~"), ".my.cnf"),
                                   "client")

config_info_list = [mysql_config[k]
                    for k in ['host', 'user', 'password', 'database']]

# connects to the database
def db_conn():
    return MySQLdb.connect(*config_info_list)


webapp = flask.Flask(__name__, static_url_path='/static')


@webapp.route('/')
def home():
    return render_template('Home.html')

# displays weapon page
@webapp.route('/weapon/')
def weapon():
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT weapon_ID, price FROM Weapon;")
    r = cursor.fetchall()
    print(r)
    return render_template('Weapon.html', rows=r)

# displays weapon insert form
@webapp.route('/weapon_result', methods=['POST', 'GET'])
def weapon_result():
    conn = db_conn()
    cursor = conn.cursor()

    if request.method == "POST":
        details = request.form
        price = details['price']
        weapon_ID = details['weapon_ID']
        data = (price, weapon_ID)
        cursor.execute("INSERT INTO Weapon (price, weapon_ID) VALUES "
                       "(%s, %s)", data)
        conn.commit()
        return render_template('Weapon.html')

# displays weapon update form
@webapp.route('/weapon_update', methods=['POST', 'GET'])
def weapon_update():
    conn = db_conn()
    cursor = conn.cursor()

    if request.method == "POST":
        details = request.form
        price = details['price']
        weapon_ID = details['weapon_ID']
        data = (price, weapon_ID)
        cursor.execute("UPDATE Weapon SET (price, weapon_ID) VALUES "
                       "(%s, %s)", data)
        conn.commit()
        return render_template('Weapon.html')

# displays order page
@webapp.route('/orders/')
def orders():
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT order_ID, customer_ID, weapon_ID, currency, order_date FROM Orders;")
    r = cursor.fetchall()
    print(r)
    return render_template('Orders.html', rows=r)

# displays order request form
@webapp.route('/orders', methods=['POST', 'GET'])
def order_results():
    conn = db_conn()
    cursor = conn.cursor()

    if request.method == "POST":
        details = request.form
        order_ID = details['order_ID']
        price = details['price']
        weapon_ID = details['weapon_ID']
        currency = details['currency']
        order_date = details['order_date']
        data = (order_ID, price, weapon_ID, currency, order_date)
        cursor.execute("INSERT INTO Orders (order_ID, price, weapon_ID) VALUES (%s, %s, %s, %s, %s)", data)
        conn.commit()
        return render_template('Orders.html')

# displays stock page
@webapp.route('/stock/')
def stock():
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT number_of_items_available, total_number_of_items, weapon_ID, weapon_type FROM Stock;")
    r = cursor.fetchall()
    print(r)
    return render_template('Stock.html', rows=r)

# displays stock request form
@webapp.route('/stock', methods=['POST', 'GET'])
def stock_results():
    conn = db_conn()
    cursor = conn.cursor()

    if request.method == "POST":
        details = request.form
        number_of_items_available = details['number_of_items_available']
        total_number_of_items = details['total_number_of_items']
        weapon_ID = details['weapon_ID']
        weapon_type = details['weapon_type']
        data = (number_of_items_available, total_number_of_items, weapon_ID, weapon_type)
        cursor.execute("INSERT INTO Stock (number_of_items_available, total_number_of_items, weapon_ID, weapon_type) "
                       "VALUES (%s, %s, %s, %s)", data)
        conn.commit()
        return render_template('Stock.html')

# displays customer page
@webapp.route('/customer/')
def customer():
    conn = db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT name, address, customer_ID FROM Customer;")
    r = cursor.fetchall()
    print(r)
    return render_template('Customer.html', rows=r)

# displays customer request form
@webapp.route('/customer', methods=['POST', 'GET'])
def customer_results():
    conn = db_conn()
    cursor = conn.cursor()

    if request.method == "POST":
        details = request.form
        name = details['name']
        address = details['address']
        data = (name, address)
        cursor.execute("INSERT INTO Customer (name, address) VALUES (%s, %s)", data)
        conn.commit()
        return render_template('Customer.html')

# Original customer functionality

# @webapp.route('/customer/<int:id>', methods=['POST', 'GET'])
# def customer_update(id):
#     conn = db_conn()
#     cursor = conn.cursor()
#
#     if request.method == "GET":
#         cursor.execute('SELECT name, address, customer_ID from Customer WHERE id = %s'
#                        % id)
#         customer_result = cursor.fetchone()
#
#         if customer_result is None:
#             return "No such person found!"
#
#         return render_template('Customer.html', customer=customer_result)
#
#     if request.method == "POST":
#         details = request.form
#         customer_ID = details['customer_ID']
#         name = details['name']
#         address = details['address']
#         data = (name, address, customer_ID)
#         cursor.execute("UPDATE Customer SET (name, address) VALUES "
#                        "(%s, %s) WHERE id = %s", data)
#         conn.commit()
#         return render_template('Customer.html')
#
# @webapp.route('/customer/<int:id>')
# def customer_delete(id):
#     conn = db_conn()
#     cursor = conn.cursor()
#
#     details = request.form
#     customer_ID = details['customer_ID']
#     data = (customer_ID)
#     cursor.execute("DELETE FROM Customer WHERE customer_ID = %s", data)
#     conn.commit()
#     return render_template('Customer.html')


if __name__ == '__main__':
    webapp.run()
