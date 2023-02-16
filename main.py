from flask_mysqldb import MySQL
from datetime import datetime
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "0000"
app.config["MYSQL_DB"] = "system"

my_sql = MySQL(app)


@app.route("/api/customers/<int:id>")
@cross_origin()
def get_Customer(id):
    cur = my_sql.connection.cursor()
    # buscamos el usuario por el id
    cur.execute(f"SELECT *  FROM customers where customers.id = {id};")
    # get the data
    consult = cur.fetchall()

    # reset the data for convert in json
    consult_json = {
        "id": consult[0][0],
        "firstname": consult[0][1],
        "lastname": consult[0][2],
        "email": consult[0][3],
        "phone": consult[0][4],
        "address": consult[0][5],
        "date_created": consult[0][6],
    }

    my_sql.connection.commit()
    return jsonify(consult_json)


@app.route("/api/customers")
@cross_origin()
def get_AllCustomers():
    cur = my_sql.connection.cursor()
    cur.execute("SELECT * FROM customers;")
    consult = cur.fetchall()
    list_json = []
    # iteramos en los usuarios de la base de datos para
    # guardarlos en el dict_consult y pasarlo a formato JSON
    for i in consult:
        consult_json = {
            "id": i[0],
            "firstname": i[1],
            "lastname": i[2],
            "email": i[3],
            "phone": i[4],
            "address": i[5],
            "date_created": i[6],
        }
        list_json.append(consult_json)

    # lista que adentro tiene enumerados los usuarios y sus valores

    my_sql.connection.commit()

    return jsonify(list_json)


@app.route("/api/customers", methods=["POST"])
def create_customer():
    if "id" in request.json:
        edit_customer()
        return "client edit"
    else:
        save_customer()
        return "Done"


def edit_customer():
    # create a actually day with datetime and get the format
    # 2022-07-19 21:00:27
    today = datetime.now()
    User_data = {
        "id": request.json["id"],
        "firstname": request.json["firstname"],
        "lastname": request.json["lastname"],
        "email": request.json["email"],
        "phone": request.json["phone"],
        "address": request.json["address"],
        "date_created": today,
    }
    cur = my_sql.connection.cursor()
    cur.execute(
        f"UPDATE `customers` SET `id` = '{User_data['id']}',`firstname` = '{User_data['firstname']}',`lastname` = '{User_data['lastname']}',`email` = '{User_data['email']}',`phone` = '{User_data['phone']}',`address` = '{User_data['address']}',`date_created` = '{User_data['date_created']}' WHERE `id` = '{User_data['id']}';"
    )

    my_sql.connection.commit()
    return "cliente guardado"


def save_customer():
    # create a actually day with datetime and get the format
    # 2022-07-19 21:00:27
    today = datetime.now()
    cur = my_sql.connection.cursor()
    cur.execute(
        f"INSERT INTO `customers` (`id`, `firstname`, `lastname`, `email`, `phone`, `address`, `date_created`)"
        + f"VALUES (Null, '{request.json['firstname']}', '{request.json['lastname']}', '{request.json['email']}', '{request.json['phone']}', '{request.json['address']}', '{today}');"
    )

    my_sql.connection.commit()

    return "cliente guardado"


@app.route("/api/customers/<int:id>", methods=["DELETE"])
@cross_origin()
def remove_customer(id):
    cur = my_sql.connection.cursor()
    cur.execute(f"DELETE FROM customers WHERE customers.id = {id};")

    my_sql.connection.commit()

    return f"cliente eliminado {id} "


@app.route("/")
@cross_origin()
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(None, 3000, True)
