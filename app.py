from flask import Flask, render_template, request
from model_utils import load_and_cluster, recommend_products

app = Flask(__name__)

# Load data and perform clustering
try:
    user_product_matrix, reduced_data, hc_labels, silhouette = load_and_cluster("ratings_short.csv")
    print(f"✅ Clustering completed. Silhouette Score: {silhouette:.3f}")
    print(f"📊 Data shape: {user_product_matrix.shape}")
    print(f"📦 Sample user IDs: {user_product_matrix.index[:5].tolist()}")
except Exception as e:
    print("❌ Error during clustering:", e)
    user_product_matrix = None
    silhouette = None

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = None
    user_ids = user_product_matrix.index.tolist() if user_product_matrix is not None else []

    if request.method == "POST":
        try:
            user_id = request.form["user_id"]  # ✅ Treat user ID as string
            recommendation = recommend_products(user_id, user_product_matrix)
        except Exception as e:
            print("❌ Error during recommendation:", e)
            recommendation = ["An error occurred while generating recommendations."]

    return render_template("index.html", user_ids=user_ids, recommendation=recommendation, silhouette=silhouette)

if __name__ == "__main__":
    app.run(debug=True)
