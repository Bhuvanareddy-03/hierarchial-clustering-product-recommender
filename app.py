from flask import Flask, render_template, request
from model_utils import load_and_cluster, recommend_products

app = Flask(__name__)

# Load and cluster once at startup
user_product_matrix, reduced_data, hc_labels = load_and_cluster("rating_short.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = None
    user_ids = user_product_matrix.index.tolist()

    if request.method == "POST":
        user_id = int(request.form["user_id"])
        recommendation = recommend_products(user_id, user_product_matrix)

    return render_template("index.html", user_ids=user_ids, recommendation=recommendation)

if __name__ == "__main__":
    app.run(debug=True)
