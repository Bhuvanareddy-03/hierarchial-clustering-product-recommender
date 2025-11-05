from flask import Flask, render_template, request
from model_utils import load_and_cluster, recommend_products
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

user_product_matrix = None
reduced_data = None
hc_labels = None
silhouette = None

@app.route("/", methods=["GET", "POST"])
def index():
    global user_product_matrix, reduced_data, hc_labels, silhouette
    recommendation = None
    user_ids = []

    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file.filename.endswith(".csv"):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                try:
                    user_product_matrix, reduced_data, hc_labels, silhouette = load_and_cluster(filepath)
                    user_ids = user_product_matrix.index.tolist()
                    print(f"✅ Clustering complete. Silhouette Score: {silhouette:.3f}")
                except Exception as e:
                    print("❌ Error during clustering:", e)
                    recommendation = ["Error during clustering."]
            else:
                recommendation = ["Please upload a valid CSV file."]
        elif "user_id" in request.form:
            user_id = request.form["user_id"]
            try:
                recommendation = recommend_products(user_id, user_product_matrix)
            except Exception as e:
                print("❌ Error during recommendation:", e)
                recommendation = ["Error during recommendation."]

    if user_product_matrix is not None:
        user_ids = user_product_matrix.index.tolist()

    return render_template("index.html", user_ids=user_ids, recommendation=recommendation, silhouette=silhouette)
