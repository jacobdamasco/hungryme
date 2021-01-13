from flask import (
    Flask, redirect, request, render_template, url_for
)
import recipe_info


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_search = request.form["food"]
        return redirect(url_for("results", searched_food = user_search))
    else:
        return render_template("index.html")


@app.route("/result/<searched_food>")
def results(searched_food):
    try:
        recipe = recipe_info.get_recipe_info(searched_food)
        name = recipe[0]
        img = recipe[1]
        cals = recipe[2]
        ingredients = recipe[3]
        link = recipe[4]
    except KeyError:
        return render_template("result_error.html")
    else: 
        return render_template(
            "result.html", 
            name=name,
            img=img,
            cals=cals,
            ingredients=ingredients,
            link=link,
            searched_food=searched_food
        )

if __name__ == "__main__":
    app.run()