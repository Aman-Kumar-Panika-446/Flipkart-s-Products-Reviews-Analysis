from flask import Flask, render_template, request, redirect
from review_scrapper import get_product_details, get_data

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route("/get_reviews", methods=['POST', 'GET'])
def review():
    if request.method == 'POST':
        product_link = request.form["product_link"]
        product_image, product_name = get_product_details(product_link)

        all_reviews = get_data(product_link)
        return render_template(
            "review.html",
            product_image = product_image,
            product_name = product_name,
            reviews = all_reviews
        )

    return render_template("review.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)