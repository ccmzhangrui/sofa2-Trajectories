import pandas as pd
from sklearn.cluster import KMeans


def fit_gbtm(df_scores, n_groups=3):
    """
    Simplified trajectory modeling using KMeans clustering.
    df_scores: rows = patients, columns = daily SOFA-2 scores from Day 1 to Day 14.
    """
    model = KMeans(n_clusters=n_groups, random_state=42)
    labels = model.fit_predict(df_scores)
    return labels
