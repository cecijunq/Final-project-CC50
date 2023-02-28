import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash

# from functools import wraps


# Configure application
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///projeto.db")


@app.route("/", methods=["GET", "POST"])
def index():
    search = db.execute("SELECT DISTINCT(product) FROM products")
    if request.method == "POST":
        if not request.form.get("search"):
            print("you must provide a product name")
            return redirect("/")

        if request.form.get("search") == "all":
            all_items = db.execute("SELECT * FROM products")
            return render_template("index.html", products=all_items, items=search)

        db_products = db.execute("SELECT * FROM products WHERE product = ?;", request.form.get("search"))

        return render_template("index.html", products=db_products, items=search)
    else:
        return render_template("index.html", items=search)


@app.route("/all", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        if not request.form.get("product"):
            print("must provide a product name")
            return redirect("/all")
        elif not request.form.get("brand"):
            print("must provide a brand name")
            return redirect("/all")
        elif not request.form.get("market"):
            print("must provide the name of a market")
            return redirect("/all")
        elif not request.form.get("address"):
            print("must provide the address of the market")
            return redirect("/all")
        elif not request.form.get("price"):
            print("must provide the product's price")
            return redirect("/all")

        # db.execute("INSERT INTO products(product, brand, market, address, price) VALUES(?, ?, ?, ?, ?);", requst.form.get("name"), requst.form.get("brand"), requst.form.get("market"), requst.form.get("address"), requst.form.get("price"))
        on_db = db.execute("SELECT * FROM products WHERE product = ? AND brand = ?", request.form.get("product"), request.form.get("brand"))

        if len(on_db) == 0:
            db.execute("INSERT INTO products(product, brand, market, address, price) VALUES(?, ?, ?, ?, ?)", request.form.get("product"), request.form.get("brand"), request.form.get("market"), request.form.get("address"), request.form.get("price"))

        else:
            for this_db in on_db:
                print("!!!! entrou")
                print(this_db)
                if this_db["product"] == request.form.get("product") and this_db["brand"] == request.form.get("brand") and this_db["market"] == request.form.get("market") and this_db["address"] == request.form.get("address"):
                    print("!!! entrou no if")
                    db.execute("UPDATE products SET price = ? WHERE product = ? AND brand = ? AND market = ? AND address = ?", request.form.get("price"), request.form.get("product"), request.form.get("brand"), request.form.get("market"), request.form.get("address"))
                else:
                    print("!!! entrou no else")
                    id_p = db.execute("INSERT INTO products(product, brand, market, address, price) VALUES(?, ?, ?, ?, ?)", request.form.get("product"), request.form.get("brand"), request.form.get("market"), request.form.get("address"), request.form.get("price"))
                # elif this_db["name"] == requst.form.get("product") and this_db["brand"] == requst.form.get("brand") and this_db["market"] == request.form.get("market") and this_db["address"] != request.form.get("address"):
                #     db.execute("INSERT INTO products(name, brand, market, address, price) VALUES(?, ?, ?, ?, ?);", requst.form.get("name"), requst.form.get("brand"), requst.form.get("market"), requst.form.get("address"), requst.form.get("price"))
                # elif this_db["name"] == requst.form.get("product") and this_db["brand"] == requst.form.get("brand") and this_db["market"] != request.form.get("market")

            # print(id_p)
        return redirect("/")
    else:
        return render_template("all.html")



@app.route("/tobuy", methods=["GET", "POST"])
def tobuy():
    if request.method == "POST":
        if not request.form.get("tobuy"):
            print("must provide a product")
            return redirect("/tobuy")
        if not request.form.get("quantity"):
            print("must provide a quantity")
            return redirect("/tobuy")

        name = request.form.get("tobuy")
        qnty = request.form.get("quantity")

        prodtobuy = db.execute("SELECT product FROM tobuy;")
        n_before = db.execute("SELECT quantity FROM tobuy WHERE product = ?;", request.form.get("tobuy"))

        print(prodtobuy)
        print(prodtobuy[0])
        if len(prodtobuy) == 0:
            db.execute("INSERT INTO tobuy(product, quantity) VALUES(?, ?);", request.form.get("tobuy"), request.form.get("quantity"))

        else:
            if request.form.get("tobuy") in prodtobuy:
                db.execute("UPDATE tobuy SET quantity = ? WHERE product = ?;", n_before + request.form.get("quantity"), request.form.get("tobuy"))
            else:
                db.execute("INSERT INTO tobuy(product, quantity) VALUES(?, ?);", request.form.get("tobuy"), request.form.get("quantity"))

        updatedlist = db.execute("SELECT * FROM tobuy;")

        return render_template("tobuy.html", items=updatedlist)

    else:
        currentlist = db.execute("SELECT * FROM tobuy;")
        return render_template("tobuy.html", items=currentlist)


@app.route("/todelete", methods=["GET", "POST"])
def todelete():
    if request.method == "POST":
        if not request.form.get("todelete"):
            print("must provide a product name")
            return redirect("/todelete")

        onlist = db.execute("SELECT product FROM tobuy")
        for this_item_list in onlist:
            if this_item_list["product"] == request.form.get("todelete"):
                db.execute("DELETE FROM tobuy WHERE product = ?", request.form.get("todelete"))
        # if request.form.get("todelete") in onlist:
        #     db.execute("DELETE FROM tobuy WHERE product = ?", request.form.get("todelete"))
        #     db.execute("COMMIT")

        newlist = db.execute("SELECT * FROM tobuy;")

        return render_template("tobuy.html", items=newlist)

    else:
        currentlist2 = db.execute("SELECT * FROM tobuy;")
        return render_template("tobuy.html", items=currentlist2)