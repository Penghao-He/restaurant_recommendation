from flask import Flask, render_template, request, redirect
import main
import model

app = Flask(__name__)

@app.route("/")
def admin():
    return render_template("admin.html")

@app.route("/view")
def view():
    return render_template("view.html", entries=model.get_entries(), title=model.get_title())

@app.route("/add")
def addentry():
    return render_template("addentry.html")

@app.route("/rate_dist")
def show_rate_dist():
    rate = model.get_all_rate()
    title = model.get_title()
    main.plot_rate(rate, title)
    return redirect("/view")

@app.route("/price_dist")
def show_price_dist():
    price = model.get_all_price()
    title = model.get_title()
    main.plot_price(price, title)
    return redirect("/view")

@app.route("/show_top_rating")
def show_top_rating():
    pricerange = model.get_price_range()
    top_rate = model.get_top_rate(pricerange)
    location = main.find_out_location(top_rate)
    model.set_location(location)
    return render_template("top_rate.html", top_rate=top_rate)

@app.route('/show_top_loc')
def show_top_loc():
    location = model.get_location()
    title = model.get_title()
    main.plot_location(location[0], location[1], location[2], title)
    return redirect("/show_top_rating")

@app.route('/show_loc')
def show_loc():
    location = model.get_location()
    title = model.get_title()
    main.plot_location(location[0], location[1], location[2], title)
    return redirect("/view")

@app.route("/pricerange", methods=["POST"])
def pricerange():
    price = request.form["price"]
    model.add_pricerange(price)
    return redirect("/show_top_rating")

@app.route("/postentry", methods=["POST"])
def postentry():
    type = request.form["type"]
    city = request.form["city"]
    try:
        model.add_entry(type, city)
    except:
        main.make_new_search(type, city)
        model.add_entry(type, city)
    return redirect("/view")

@app.route("/review", methods=["GET"])
def review():
    name = request.args.get('name', default = "", type = str)
    reviews = model.get_reviews(name)
    processed_reviews = []
    for ii in reviews:
        if ii != None:
            processed_reviews.append(ii)
    return render_template("review.html", title="Review for {}".format(name), review=processed_reviews)

@app.route("/logout")
def logout():
    model.destroy()
    return redirect("/add")

if __name__=="__main__":
    model.init()
    app.run(debug=True)
