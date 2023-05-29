# Recommender System Book Rating with Flask

## Description
Recommendation system made enables users to register with their name and log in with their corresponding id. Once logged, they can change their name on their first page, as well as their profile image which is a generated avatar. To personalize the system, editing book ratings methods are provided such as viewing all their ratings, modify their existing ratings by clicking on specific book and, choosing a rating between 1 and 5 from the dropdown list and submit their input, adding a new rating and deleting their existing ones in similar manners. Recommendation of books is also included but because of the limited amount of custom dataset created, I have limited the recommendations to two books. Another recommendation feature is to specify a preferred genre of book and the system will return you those books if available. In both cases, the recommendations prioritize the most popular books or the ones the user really wants. Users with id 1-10 are valid users consisting of existing ratings and by editing their ratings, recommendation results are altered accordingly. 4 Genres were included, Fiction, History Biography and Action with 3 books each and ISBN is considered the book ID.

## Requirements

To run my recommendation system, the following libraries are required
* numpy==1.16.4
* scipy==1.3.1
* Flask==1.1.1
* pandas==0.24.2

Then, open a terminal in the directory containing these files and type “pip install –user -r requirements.txt” or type pip install for each library in case an error comes up. Subsequently, type “ python app.py” to initialize the server and then launch a browser and connect to http://127.0.0.1:5000/ and finally press “control” and “c” simultaneously on the prompt window to shut down the server.  
