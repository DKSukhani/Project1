# Project1
Project1 CS Python and JS


This is a project, pretty much build from scratch for the Project 1 assignment of the  EDx Course of CS50 Python and JS [Link](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript)

For the project I did use some template HTML, CSS and JS available on the internet.  

Credits given to Colorlib for their [Five Star Template](https://colorlib.com/wp/template/five-star/)

The application is hosted on the free tier provided by [Heroku](https://www.heroku.com).  The link to the application is [this](http://dipesh-book-app.herokuapp.com)
Since it is on the free version, please spare sometime for Heroku to load it up.

What does the App do?
1. You can sign-up or Login (if already signed-up)
2. You can search for a book based on its: 
   - ISBN
   - Author
   - Title and
   - Year of Publishing
  
The DB is maintained using POSTGRES SQL, again on the free tier of Heroku.

A readymade DB was provided by CS50 of 5000 books, so we have limited inventory over there.

The features that I have put in the app are as follows (nothing great, but well for a first timer, it took me sometime):
- Only the index page is available if you are not logged in
- Sessions are maintained
- The results are called from the DB and rendered in a table

Things that I need to do:
- Create Models.py
- ORM
- Ability for user to comment on the books (which means a DB for all the comments)
- Work with GoodReads API for the following:
  - Call the cover of each book in the results page (I somewhat achieved this)
  - Call for the existing comments on the books
- Logout feature
