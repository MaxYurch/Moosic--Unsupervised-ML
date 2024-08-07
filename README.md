**Unsupervised Machine Learning Project**

*Moosic: Custom Playlist Generator*

Moosic is a Python project designed to create cohesive playlists using a dataset of songs and their various audio features. The project employs data cleaning, dimensionality reduction, and clustering techniques to group songs into distinct playlists based on their characteristics. The primary objective is to provide users with playlists that match their preferences and moods.

*Features*

Data Cleaning: Removal of duplicates and irrelevant information.
Dimensionality Reduction: Use of PCA to reduce features from 13 to 5.
Clustering: Implementation of K-Means clustering to create playlists.
Playlists: Generate 30-50 playlists based on song features.
Future Improvements: Explore advanced clustering techniques like K-Means++ and Gaussian Mixture Models.

*Data Processing and Analysis*

Data Cleaning: Removed unnecessary features and fixed incorrect HTML links using track-IDs.
Feature Scaling: Scaled features to a range of [0, 1].
Dimensionality Reduction: Applied PCA to reduce feature count, optimizing clustering efficiency.
Clustering: Utilized K-Means clustering to segment the dataset into meaningful playlists based on audio features like danceability, energy, and valence.
Future Improvements

Experiment with K-Means++ and Gaussian Mixture Models for improved clustering.
Integrate web scraping for automatic genre and language detection.
Explore hierarchical clustering for alternative clustering strategies.
Implement integration with Spotify's API to dynamically update playlists.

*Contributors*

Ana, Max, Rolf

*License*

This project is licensed under the MIT License - see the LICENSE file for details.
