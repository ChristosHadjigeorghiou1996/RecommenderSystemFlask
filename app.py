# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:18:23 2019

@author: hadjis
"""

# References:
#Lecture notes
#Generating recommendations with Pandas: https://stackabuse.com/creating-asimple-recommender-system-in-python-using-pandas/
#Matrix factorization with Pandas: https://beckernick.github.io/matrix-factorizationrecommender/
#Wes McKinney, Python for Data Analysis, O'Reilly, 2018.
#Flask: https://www.makeuseof.com/tag/python-javascript-communicate-json/
# code taken for css mostly is referenced as much as possible to my best understanding.

from flask import Flask, render_template, redirect, url_for, request, jsonify, g
from hashlib import md5 
import sqlite3
import pandas as pd
import numpy as np 


    
app = Flask(__name__)
DATABASE = "database.db"
app.debug = True


def get_db() :
	db = getattr(g, '_database', None)
	if db is None :
		db = g._database = sqlite3.connect(DATABASE)
		db.row_factory = dict_factory
	return db


def dict_factory(cursor, row) :
	d = {}
	for idx, col in enumerate(cursor.description) :
		d[col[0]] = row[idx]
	return d

@app.teardown_appcontext
def close_connection(exception) :
	database = getattr(g, '_database', None)
	if database is not None :
		database.close()

# url_for() is the endpoint name thus url_for('login') returns /login 

def get_forename() :
	cur = get_db().execute("SELECT * FROM book_data")
	forename = cur.fetchall()
	return forename


def get_book_table():
    cur = get_db().execute("SELECT * FROM book_data")
    book_data = cur.fetchall()
    book_data_table = pd.DataFrame(book_data).values.tolist()
#    print(book_data_table)
    return book_data_table

def get_user_data_table():
    cur = get_db().execute("SELECT * FROM user_profiles")
    user_data = cur.fetchall()
    print(user_data)
    user_data_table = pd.DataFrame(user_data).values.tolist()
#    print(book_data_table)
    return user_data_table

# get all user book ratings
def get_user_book_ratings():
    cur = get_db().execute("SELECT * FROM ratings")
    user_book_rating = cur.fetchall()
    print(user_book_rating)
    user_data_table = pd.DataFrame(user_book_rating).values.tolist()
#    print(book_data_table)
    return user_data_table



def get_credentials(username):
    query = "SELECT * FROM `user_details` WHERE Name='{}'".format(username)
    print(query)
    cur = get_db().execute(query)
    user_credentials = cur.fetchone()
    if user_credentials is not None:
        user_name = user_credentials['Name']
        print(user_name)
        user_id = user_credentials['user_ID']
        print(user_id)
        return user_id, user_name
    else:
        print('Username does not exist.')


@app.route('/get_user_book_rating', methods=['POST'])
def all_book_ratings():
    a = get_user_book_ratings()
    return jsonify(a)

#************************** Try to get routes from other file ******************************
    
# check if username is valid
def register_user(user_name):
    cur = get_db().execute("SELECT MAX(user_ID) AS M FROM `user_details`")
    user_id = cur.fetchone()['M']
    new_user_id = int(user_id) + 1
    query = "INSERT INTO user_details (user_ID, Name) VALUES ({},'{}')".format(int(new_user_id), user_name)
    get_db().execute(query)
    get_db().commit()
    print('Successful registration')
    return user_id, user_name
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    print('Removing any leading or trailing spaces')
    username = request.form.get('username')
    try:
        username = username.strip()
    except AttributeError:
        raise AttributeError("Nonetype object. Please try again")
    print('username:{}'.format(username))
    if username is None or username == "":
        raise Exception('Empty username')
    
    user_id, user_name = register_user(username)
    string_user_id_for_avatar  = str(user_id)
    # md5 works on bytes and not on string so encode
    digest = md5(string_user_id_for_avatar.lower().encode('utf-8')).hexdigest()
    digest_image = "https://www.gravatar.com/avatar/"+digest+"?d=identicon&s="+'20'  
    
    
#    print(username)
    return render_template('index.html', digest_image = digest_image, user_id=user_id, user_name=user_name)



# check if username is valid
def login_user(id):
    inputed_id = id
    try:
        inputed_id = int(inputed_id)
    except ValueError:
       print("That's not an int!")
       raise ValueError("id must be integer")

    cur = get_db().execute("SELECT user_id,Name FROM `user_details` WHERE user_id={}".format(inputed_id))
    data = cur.fetchone()
    print('data:',data)
    print('eeeeem:',cur)
    try:
        user_id = data['user_ID']
    except TypeError:
        raise TypeError("You chose a wrong ID. If you don't remember your own, create a new account.")
    print('user_id:',user_id)
    user_name =data['Name']
    print('user_name: ',user_name)
    return user_id, user_name
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    id = request.form.get('username')
    print('id: {} and has type {}'.format(id, type(id)))
    if isinstance(id, int) == False:
        print('ID must be integer.')
    user_id, user_name = login_user(id)
    print('user_id: ' , user_id)
    print('user_name:',user_name)
    string_user_id_for_avatar  = str(user_id)
    # md5 works on bytes and not on string so encode
    digest = md5(string_user_id_for_avatar.lower().encode('utf-8')).hexdigest()
    digest_image = "https://www.gravatar.com/avatar/"+digest+"?d=identicon&s="+'20'  
      
    
#    print(username)
    return render_template('index.html', digest_image = digest_image, user_id=user_id, user_name=user_name)





        
@app.route('/', methods=['GET','POST'])

@app.route('/index', methods=['GET','POST'])
def index():


#    print(username)
    return render_template('login_2.html')



@app.route('/logout')
def logout():
    return redirect(url_for('index'))
#

#   
#
    
    
def edit_user(user_id,user_name):
    inputed_id = int(user_id)
    get_db().execute("UPDATE user_details SET Name = '{}' WHERE user_ID = {}".format(user_name, inputed_id))
    get_db().commit()
    print('Successful Change of data')
    return user_id, user_name
   
@app.route('/editUser', methods=['GET', 'POST'])
def editUser():
    new_username = request.form['new_username']
    user_id = request.form['user_id']
    if new_username is None:
        raise Exception('Empty username')
    user_id, user_name = edit_user(user_id, new_username)
    string_user_id_for_avatar  = str(user_id)
    # md5 works on bytes and not on string so encode
    digest = md5(string_user_id_for_avatar.lower().encode('utf-8')).hexdigest()
    digest_image = "https://www.gravatar.com/avatar/"+digest+"?d=identicon&s="+'20'  

    return render_template('index.html', digest_image = digest_image, user_id=user_id, user_name=user_name)


def get_ratings_of_user(user_id):
    cur = get_db().execute("SELECT * FROM `book_ratings` WHERE user_ID = {}".format(user_id))
    data = cur.fetchall()
    return data
    
@app.route('/get_user_ratings', methods=['GET', 'POST'])
def get_user_ratings():
    user_id = request.form.get('user_id')
    int_user_id = int(user_id)
    data_received = get_ratings_of_user(int_user_id)
    data_to_be_sent = jsonify(data_received)
    print('data_to_be_sent:{}',data_to_be_sent)
    
    return data_to_be_sent

def user_rated_books(user_id):
    cur = get_db().execute("SELECT book_data.book_title FROM (`book_ratings` INNER JOIN `book_data` ON book_ratings.ISBN = book_data.ISBN) WHERE book_ratings.user_ID ={}".format(user_id))
    data = cur.fetchall()
    return data
    
@app.route('/get_user_rated_books', methods=['GET', 'POST'])
def get_user_rated_books():
    user_id = request.form.get('user_id')
    int_user_id = int(user_id)
    rated_books_received = user_rated_books(int_user_id)
    rated_books_sent = jsonify(rated_books_received)
    print('rated_books_sent:{}',rated_books_sent)
    
    return rated_books_sent


def update_book_rating(user_id, book_title, new_rating):
#    print('*'*10,' Update Book rating values','*'*10)
    inputed_id = int(user_id)
    cur = get_db().execute("SELECT book_data.ISBN FROM (`book_ratings` INNER JOIN `book_data` ON book_ratings.ISBN = book_data.ISBN) WHERE book_ratings.user_ID ={} AND book_data.book_title = '{}'".format(inputed_id, book_title))    
    data = cur.fetchone()
#    print('data1: {}'.format(data))
    ISBN_chosen = data['ISBN']
#    print('ISBN_chosen: {}'.format(ISBN_chosen))
#    print('Id to search: {}'.format(inputed_id))
#    print('Update to: {}'.format(new_rating))
    get_db().execute("UPDATE book_ratings SET book_rating = {} WHERE user_ID = {} and ISBN = '{}'".format(new_rating, inputed_id, ISBN_chosen))
    get_db().commit()
    cur = get_db().execute("SELECT * from book_ratings where user_ID = {} and ISBN = '{}'".format(inputed_id,ISBN_chosen))
    data = cur.fetchone()
#    print('de dame: {}'.format(data))
    return data

@app.route('/update_rating', methods=['GET', 'POST'])
def update_rating():
    print('received from html: {}'.format(request.form))
    user_id = request.form.get('user_id')
#    print("USER ID: " , user_id)
    int_user_id = int(user_id)
    book_title = request.form.get('book_title')
#    print('BOOOOK TITLE  : ' , book_title)
    rating = request.form.get('rating')
#    print('RATINGGGG : ' , rating)
    data = update_book_rating(int_user_id, book_title, rating)
#    print('data received from inner function: {}'.format(data))
    book_rating_verification = data['book_rating']
#    print('book_rating_verification: {}'.format(book_rating_verification))
    ISBN_verification = data['ISBN']
#    print('ISBN_verification: {}'.format(ISBN_verification))
    
    return 'Successful Update of rating'  

def delete_book_rating(user_id, book_title):
#    print('*'*10,' Delete Book rating values','*'*10)
    inputed_id = int(user_id)
    cur = get_db().execute("SELECT book_data.ISBN FROM (`book_ratings` INNER JOIN `book_data` ON book_ratings.ISBN = book_data.ISBN) WHERE book_ratings.user_ID ={} AND book_data.book_title = '{}'".format(inputed_id, book_title))    
    data = cur.fetchone()
#    print('data1: {}'.format(data))
    ISBN_chosen = data['ISBN']
#    print('ISBN_chosen: {}'.format(ISBN_chosen))
#    print('Id to search: {}'.format(inputed_id))
    get_db().execute("DELETE FROM book_ratings WHERE user_ID = {} and ISBN = '{}'".format(inputed_id, ISBN_chosen))
    get_db().commit()
    cur = get_db().execute("SELECT * from book_ratings where user_ID = {} ".format(inputed_id))
    data = cur.fetchone()
#    print('de dame: {}'.format(data))

@app.route('/delete_rating', methods=['GET', 'POST'])
def delete_rating():
#    print('received from html: {}'.format(request.form))
    user_id = request.form.get('user_id')
#    print("USER ID: " , user_id)
    int_user_id = int(user_id)
    book_title = request.form.get('book_title')
#    print('BOOOOK TITLE  : ' , book_title)
    delete_book_rating(int_user_id, book_title)
    
    return 'Successful Delete of rating'  











def user_unrated_books(user_id):
    cur = get_db().execute("SELECT DISTINCT book_data.book_title FROM `book_data` WHERE book_data.book_title NOT IN ( SELECT book_data.book_title FROM (`book_ratings` INNER JOIN `book_data` ON book_ratings.ISBN = book_data.ISBN) WHERE user_ID = {})".format(user_id))
    data = cur.fetchall()
    return data
    
@app.route('/get_unrated_books', methods=['GET', 'POST'])
def get_unrated_books():
    user_id = request.form.get('user_id')
    int_user_id = int(user_id)
    unrated_books_received = user_unrated_books(int_user_id)
    unrated_books_sent = jsonify(unrated_books_received)
#    print('unrated_books_sent:{}',unrated_books_sent)

    return unrated_books_sent

#emina dame 

def add_book_rating(user_id, book_title, new_rating):
#    print('*'*10,' Add Book rating values','*'*10)
    inputed_id = int(user_id)
#    print('user_id: ',user_id)
#    print('BOOOOK TITLE 2 : ' , book_title)
#    print('RATINGGGG  2 : ' , new_rating)
    
    cur = get_db().execute("SELECT book_data.ISBN FROM `book_data` WHERE book_data.book_title ='{}'".format(book_title))    
    data = cur.fetchone()
#    print('data1: {}'.format(data))
    ISBN_chosen = data['ISBN']
#    print('ISBN_chosen: {}'.format(ISBN_chosen))
#    print('Id to add: {}'.format(inputed_id))
#    print('Value to add : {}'.format(new_rating))
    get_db().execute("INSERT INTO book_ratings VALUES ({}, '{}', {})".format(inputed_id, ISBN_chosen, new_rating))
    get_db().commit()
    
    cur = get_db().execute("SELECT * from book_ratings where user_ID = {} and ISBN = '{}'".format(inputed_id,ISBN_chosen))
    data = cur.fetchone()
#    print('de dame: {}'.format(data))
    return data

@app.route('/add_new_rating', methods=['GET', 'POST'])
def add_new_rating():
#    print('received from html: {}'.format(request.form))
    user_id = request.form.get('user_id')
#    print("USER ID: " , user_id)
    int_user_id = int(user_id)
    book_title = request.form.get('book_title')
#    print('BOOOOK TITLE 2 : ' , book_title)
    rating = request.form.get('rating')
#    print('RATINGGGG : ' , rating)
    data = add_book_rating(int_user_id, book_title, rating)
#    print('data received from inner function: {}'.format(data))
    book_rating_verification = data['book_rating']
#    print('book_rating_verification: {}'.format(book_rating_verification))
    ISBN_verification = data['ISBN']
#    print('ISBN_verification: {}'.format(ISBN_verification))
    
    return 'Successful Addition of rating' 

def helper_function(predictions_df, userID, movies_df, original_ratings_df, num_recommendations=5):
    
    # Get and sort the user's predictions
    user_row_number = userID - 1 # UserID starts at 1, not 0
    try :
        sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)
    except IndexError:
        raise IndexError('Must have at least one rating to use recommendation system.')
    
    # Get the user's data and merge in the movie information.
    user_data = original_ratings_df[original_ratings_df.user_ID == (userID)]
    user_full = (user_data.merge(movies_df, how = 'left', left_on = 'ISBN', right_on = 'ISBN').
                     sort_values(['book_rating'], ascending=False)
                 )

#    print ('User {0} has already rated {1} movies.'.format(userID, user_full.shape[0]))
#    print ('Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations))
    
    # Recommend the highest predicted rating movies that the user hasn't seen yet.
    recommendations = (movies_df[~movies_df['ISBN'].isin(user_full['ISBN'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'ISBN',
               right_on = 'ISBN').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).
                       iloc[:num_recommendations, :-1]
                      )

    return user_full, recommendations

# get the two tables
def recommend_books(num_recommendations = 2):
#    print('received from html: {}'.format(request.form))
    user_id = request.form.get('user_id')
#    print("USER ID: " , user_id)
    user_id = int(user_id)
    
    # user_id = request.form.get('user_id')
#    print("USER ID: " , user_id)
    # combine tables on ISBN
#    cur = get_db().execute("SELECT * FROM (`book_ratings` INNER JOIN `book_data` ON book_ratings.ISBN = book_data.ISBN)")
    cur = get_db().execute("SELECT * FROM book_data")
    data_books = cur.fetchall()
    books_df = pd.DataFrame(data_books)
#    print('books_df', books_df)
    cur = get_db().execute("SELECT * FROM book_ratings")
    data_ratings = cur.fetchall()
    book_rating_df = pd.DataFrame(data_ratings)
#    print('book_rating_df:',book_rating_df)

    # perform SVD

    from scipy.sparse.linalg import svds
    R_df = book_rating_df.pivot(index = 'user_ID', columns ='ISBN', values = 'book_rating').fillna(0)
    R = R_df.as_matrix()
    user_ratings_mean = np.mean(R, axis = 1)
    R_demeaned = R - user_ratings_mean.reshape(-1, 1)
    U, sigma, Vt = svds(R_demeaned, k=4)
    # need matrix multiplication for predictions 
    sigma = np.diag(sigma)
    
    all_user_predicted_ratings_df = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    preds_df = pd.DataFrame(all_user_predicted_ratings_df, columns= R_df.columns)
    
#    print('preds_df:\n')
#    print(preds_df.head())  
    already_rated, predictions = helper_function(preds_df, user_id, books_df, book_rating_df, num_recommendations)
#    print('ALREADY RATED: ' ,already_rated.values.tolist())
#    print('RECOMMEND: ' , predictions.values.tolist())
    list_to_return_already_rated = []
    for i in already_rated.values.tolist():
        print(i)
        dict1 = {}
        dict1['ISBN'] = i[0]
        dict1['rating'] = i[1]
        dict1['user_ID'] = i[2]
        dict1['book_author'] = i[3]
        dict1['genre'] = i[4]
        dict1['book_title'] = i[5]
        list_to_return_already_rated.append(dict1)
        
    list_to_return_predictions = []
    for j in predictions.values.tolist():
        print(j)
        dict2 = {}
        dict2['ISBN'] = j[0]
        dict2['book_author'] = j[1]
        dict2['book_genre'] = j[2]
        dict2['book_title'] = j[3]
        list_to_return_predictions.append(dict2)
    
        
#    print('list_to_return_already_rated: ' , list_to_return_already_rated)
#    print('list_to_return_predictions:', list_to_return_predictions)
    return list_to_return_already_rated, list_to_return_predictions
    # get user ratings in descending order
    
    
 # recommend only top 2 books if available else, whatever is available in chosen category
@app.route('/get_rec', methods=['GET', 'POST'])
def get_rec():
    return jsonify(recommend_books())
    
@app.route('/get_genre_rec', methods=['GET','POST'])
def get_gentre_rec():
    return jsonify(recommend_books())
    
    
    
    
    
# already_rated, predictions= recommend_books(preds_df, 2, book_data_df, user_book_rating_df, num_recommendations = 3)

    
    

if  __name__ == "__main__" :
	app.run()