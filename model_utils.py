import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering

def load_and_cluster(filepath):
    df = pd.read_csv(filepath, usecols=[0, 1, 2] , header=None)
    df.columns = ['userId', 'productId', 'rating']
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df.dropna(inplace=True)

    df_sample = df.sample(n=3000, random_state=42)
    matrix = df_sample.pivot_table(index='userId', columns='productId', values='rating').fillna(0)

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(matrix)

    pca = PCA(n_components=30, random_state=42)
    reduced_data = pca.fit_transform(scaled_data)

    hc = AgglomerativeClustering(n_clusters=5, linkage='ward')
    hc_labels = hc.fit_predict(reduced_data)
    matrix['Cluster_HC'] = hc_labels

    return matrix, reduced_data, hc_labels

def recommend_products(user_id, matrix, cluster_label_col='Cluster_HC'):
    if user_id not in matrix.index:
        return ["User ID not found."]

    user_cluster = matrix.loc[user_id, cluster_label_col]
    cluster_users = matrix[matrix[cluster_label_col] == user_cluster]
    cluster_users = cluster_users.drop(columns=['Cluster_HC'], errors='ignore')
    cluster_users = cluster_users.apply(pd.to_numeric, errors='coerce')
    cluster_users = cluster_users.dropna(axis=1, how='all')

    if cluster_users.empty:
        return ["No product ratings in this cluster."]

    mean_ratings = cluster_users.mean().sort_values(ascending=False)
    return mean_ratings.head(5).to_dict()
