import MySQLdb
from flask import render_template
import flask
import configparser


# def read_mysql_config(mysql_config_file_name: str):
#     config = configparser.ConfigParser()
#     config.read(mysql_config_file_name)
#     return dict(config['client'])
#
#
# config_info = read_mysql_config("../.my.cnf")
#
# db_conn = MySQLdb.connect(config_info['host'],
#                           config_info['user'],
#                           config_info['password'],
#                           config_info['database'])

webapp = flask.Flask(__name__, static_url_path='/static')

@webapp.route('/')
def home():
    return render_template('Home.html')

@webapp.route('/product')
def product():
    return render_template('Product.html')

@webapp.route('/order')
def order():
    return render_template('Order.html')

@webapp.route('/stock')
def stock():
    return render_template('Stock.html')

@webapp.route('/customer')
def customer():
    return render_template('Customer.html')


if __name__ == '__main__':
    webapp.run()