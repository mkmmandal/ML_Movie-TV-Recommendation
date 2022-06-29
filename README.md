# ML_Movie-TV-Recommendation
This is an end-to-end Machine Learning Project from Defining problem to building an app working on the ML model.
Application is deployed to Heroku.(https://mkm-movieandtv-recommendation.herokuapp.com)

In this project I am finding the similar movies/tv to recommend based on bag of words and use of Cosine similarity.

Data is fetched from tmdb website api's.(https://www.themoviedb.org/documentation/api)

After basic Data cleaning, EDA; tags are created for each movie/tv which includes genres, language , plot, top 3 actors and director. Model is deployed and similar content is fetched using similarity matrix. Later sorting is done by web-scrapping imdb website for ratings and I deploying the app to heroku as well.

Description of files in this repository:

1.Movie-TVRecommendation_Notebook.ipynb -Main Jupyter notebook for this project. For data fetching, EDA and model deployment.

2.app.py -Application file for this project. App is build using Flask and basic html,css.

3.templates/index.html -HTML file for app. (I used inline-css for little styling, you can add static/styles.css file as well for styling)



