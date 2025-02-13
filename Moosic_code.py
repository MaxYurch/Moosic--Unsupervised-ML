# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13PnITO7_icptFgI3hZIaNuvN8NYGIgK0
"""

import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.datasets import make_blobs

import plotly.graph_objects as go

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import set_config
set_config(transform_output="pandas")

# ID of the Google Sheet for student food preferences
sheet_id = "1jBC5MMLTTJJxLYNgTByNgZd25vSEK98xD2PHMRHWa3g"

# Title of the Google Sheet
sheet_name = "16261156"

# URL to download the Google Sheet as a CSV
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={sheet_name}"

# Create a Pandas DataFrame from the CSV data
songs_df = pd.read_csv(url, index_col="name")

to_drop = ['number','id', 'html', 'time_signature','mode','artist','type']
songs_df = songs_df.drop(columns=to_drop)

songs_df

songs_df.info()

names_to_drop = ['17', '110', '212', '911']

# Creating a boolean mask for the index
mask = (~songs_df.index.str.startswith(('?', '#', '+')) & ~songs_df.index.isin(names_to_drop) & ~songs_df.index.str.contains(r'^\d{1,2}:\d{2}$'))

# Applying the mask to the DataFrame
df_filtered = songs_df[mask]

print("\nFiltered DataFrame:")
df_filtered

df_filtered.duplicated().sum()

songs_df=df_filtered.drop_duplicates()

songs_df

songs_df.dropna(axis=0)

songs_df

#Scaling the data:

# Initialise the transformer (optionally, set parameters)
my_min_max = MinMaxScaler()

# Use the transformer to transform the data
scaled_features_df = my_min_max.fit_transform(songs_df)

scaled_features_df

#PCA

# Initialise the PCA object
pca = PCA()

# Fit the PCA object to the data
pca.fit(scaled_features_df)

# Transform scaled_features_df based on the fit calculations
pca_basic_df = pca.transform(scaled_features_df)

pca_basic_df

# Get the variance explained by each principal component
explained_variance_array = pca.explained_variance_ratio_

explained_variance_array

pd.DataFrame(explained_variance_array, columns=["Variance explained"])

# Create a Pandas DataFrame from the variance explained array
explained_variance_array_df = pd.DataFrame(explained_variance_array, columns=["Variance explained"])

(
  # Create a line chart with sns.relplot
  sns.relplot(
      kind = 'line',
      data = explained_variance_array_df,
      x = explained_variance_array_df.index,
      y = "Variance explained",
      marker = 'o',
      aspect = 1.3)
  # Set the title of the plot
  .set(title = "Proportion of variance explained by each principal component")
  # Set the axis labels
  .set_axis_labels("Principal component number", "Proportion of variance")
);

elbow=4

# Create a PCA object with {elbow} principal components
# We add 1 as the principal components start at 0 and not 1
pca_elbow = PCA(n_components = elbow + 1)

# Fit the PCA object to the scaled features dataframe and transform it
pca_elbow_df = pca_elbow.fit_transform(scaled_features_df)

# The dataframe now contains the principal components of the scaled features dataframe
pca_elbow_df

#k-means
# 1. elbow and inertia

# Decide on a random_state to use
seed = 123

# Set the maximum number of clusters to try
max_k = 100

# Create an empty list to store the inertia scores
inertia_list = []

# Iterate over the range of cluster numbers
for i in range(1, max_k + 1):

    # Create a KMeans object with the specified number of clusters
    myKMeans = KMeans(n_clusters = i,
                      n_init = "auto",
                      random_state = seed)

    # Fit the KMeans model to the scaled data
    myKMeans.fit(pca_elbow_df)

    # Append the inertia score to the list
    inertia_list.append(myKMeans.inertia_)

# Set the Seaborn theme to darkgrid
sns.set_theme(style='darkgrid')

(
# Create a line plot of the inertia scores
sns.relplot(y = inertia_list,
            x = range(1, max_k + 1),
            kind = 'line',
            marker = 'o',
            height = 8,
            aspect = 2)
# Set the title of the plot
.set(title=f"Inertia score from 1 to {max_k} clusters")
# Set the axis labels
.set_axis_labels("Number of clusters", "Inertia score")
);

#elbow between 10 and 15 clusters

# 2. silhouette score

# Set the maximum number of clusters to try
max_k = 100

# Create an empty list to store the silhouette scores
sil_scores = []


for j in range(2, max_k +1):

    # Create a KMeans object with the specified number of clusters
    kmeans = KMeans(n_clusters = j,
                    n_init = "auto",
                    random_state = seed)

    # Fit the KMeans model to the scaled data
    kmeans.fit(pca_elbow_df)

    # Get the cluster labels
    labels = kmeans.labels_

    # Calculate the silhouette score
    score = silhouette_score(pca_elbow_df, labels)

    # Append the silhouette score to the list
    sil_scores.append(score)

(
sns.relplot(y = sil_scores,
            x = range(2, max_k+1),
            kind = 'line',
            marker = 'o',
            height = 8,
            aspect = 2)
.set(title=f"Silhouette score from 2 to {max_k - 1} clusters")
.set_axis_labels("Number of clusters", "Silhouette score")
);

# between 20 and 40

#exploring the cluster

# Initialise the model
my_kmeans = KMeans(n_clusters = 30, # you always choose the number of k here
                   random_state = 123)

# Fit the model to the data
my_kmeans.fit(pca_elbow_df)

# Obtain the cluster output
clusters = my_kmeans.labels_

# Attach the cluster output to our original DataFrame
pca_elbow_df["cluster"] = clusters

pca_elbow_df.groupby(by="cluster").mean()

# Attach the cluster labels to the original DataFrame
pca_elbow_df['cluster'] = clusters

# Create a dictionary to store song names in each cluster
clusters_dict = {}

# Store song names in the dictionary
for cluster_num, cluster_data in pca_elbow_df.groupby('cluster'):
    clusters_dict[cluster_num] = cluster_data.index.to_list()

# Print the song names in each cluster
for cluster_num, songs in clusters_dict.items():
    print(f"\nCluster {cluster_num}:")
    print(songs)

