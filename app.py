import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, role TEXT, password TEXT)')
    print("Users Table created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS Products (id INTEGER PRIMARY KEY AUTOINCREMENT, products TEXT, type TEXT, quantity TEXT, prices TEXT)')
    print("Products Table created successfully")
    conn.close()


init_sqlite_db()

app = Flask(__name__)
CORS(app)
# ======================================================================================================================
                                        # =====ADDING NEW USERS RECORDS===== !!!


@app.route('/')
@app.route('/enter-new/')
def enter_new_user():
    return render_template('users.html')


@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    msg = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            user = post_data['user']
            role = post_data['role']
            password = post_data['password']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Users (user, role, password) VALUES (?, ?, ?)",
                            (user, role, password))
                con.commit()
                msg = "Record successfully added."

        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            con.close()
            return jsonify(msg)
# ======================================================================================================================

                                                    # =====LOGIN===== !!!
@app.route('/log/', methods=['GET'])
def login():
    records = {}
    if request.method == "GET":
        msg = None
        try:
            post_data = request.get_json()
            user = post_data['user']
            password = post_data['password']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                sql = "SELECT * FROM Users WHERE user = ? and password = ?"
                cur.execute(sql, [user, password])
                # records = cur.fetchall()

        except Exception as e:
            con.rollback()
            msg = "error occured while fetching data from db" + str(e)
        finally:
            con.close()
            return jsonify(msg=msg)
# ======================================================================================================================
                                                # =====SHOWING USERS RECORDS=====

@app.route('/show-records/', methods=['GET'])
def show_records():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            records = cur.fetchall()

    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database.")
    finally:
        con.close()
        return jsonify(records)
# ======================================================================================================================
                                    # =====DELETE THE USERS!!!=====


@app.route('/delete-users/<int:users_id>/', methods=["DELETE"])
def delete_users(users_id):
    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM users WHERE id=" + str(users_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return jsonify(msg)
# ----------------------------------------------------------------------------------------------------------------------
                                        # ===== ADDING NEW PRODUCTS!!!=====


@app.route('/')
@app.route('/show-product-form/')
def show_product_form():
    return render_template('tables.html')


@app.route('/add-new-products/', methods=['POST'])
def add_new_products():
    if request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()
            products = post_data['name']
            prod_type = post_data['type']
            quantity = post_data['quantity']
            prices = post_data['price']
            print(products, prices)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Products (products, type, quantity, prices) VALUES (?, ?, ?, ?)",
                            (products, prod_type, quantity, prices))
                con.commit()
                msg = "Product successfully added."

        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            con.close()
            return jsonify(msg)
# ======================================================================================================================
                                        # =====SHOW ALL PRODUCTS!!!=====


@app.route('/show-products/', methods=['GET'])
def show_products():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM products")
            records = cur.fetchall()

    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database.")
    finally:
        con.close()
        return jsonify(records)
# ======================================================================================================================

# ==                                    ===DELETE THE PRODUCTS!!!=====


@app.route('/delete-products/<int:products_id>/', methods=["DELETE"])
def delete_products(products_id):
    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM products WHERE id=" + str(products_id))
            con.commit()
            msg = "Product was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return jsonify(msg)
# ======================================================================================================================
                                            # ======GET PRODUCTS EACH======!!!


@app.route('/button-click/', methods=['GET', 'POST'])
def btn_click():
    products = {}
    if request.method == "POST" or request.method == "GET":
        msg = None
        try:
            # post_data = request.get_json()
            # prod_type = post_data['type']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                sql = "SELECT * FROM products"
                cur.execute(sql)
                products = cur.fetchall()

        except Exception as e:
            con.rollback()
            msg = "There was an error fetching results from the database." + str(e)
        finally:
            con.close()
            return jsonify(products)

# ======================================================================================================================
#                                     ========UPDATE ITEMS!!!========

@app.route('/edit-products/<int:product_id>/', methods=["PUT"])
def edit_items(product_id):
    post_data = request.get_json()

    records = {
        'id': product_id,
        'products': post_data['name'],
        'type': post_data['type'],
        'quantity': post_data['quantity'],
        'prices': post_data['price']
    }
    # LINKING DATABASE
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    sql = ("UPDATE Products SET products = ?, type = ?, quantity = ?, prices = ? WHERE id = ?")
    cur.execute(sql, (records['products'], records['type'], records['quantity'], records['prices'], records['id']))
    con.commit()
    return jsonify(records)
# ======================================================================================================================
#                                     ========UPDATE USERS!!!========


@app.route('/edit-users/<int:user_id>/', methods=["PUT"])
def edit_users(user_id):
    post_data = request.get_json()

    user_records = {
        'id': user_id,
        'user': post_data['user'],
        'role': post_data['role'],
        'password': post_data['password'],
    }
    # LINKING DATABASE
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    sql = ("UPDATE Products SET Users = ?, user = ?, role = ?, password = ? WHERE id = ?")
    cur.execute(sql, (user_records['user'], user_records['role'], user_records['password'], user_records['id']))
    con.commit()
    return jsonify(user_records)


if __name__ == "__main__":
    app.run(debug=True)
