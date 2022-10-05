
# Network(socialise)
This a social network type web application that is implemented with the python django framework ,html, css and javascript.This project was part of project to be submitted for the cs50W course. The web app gives allows users to make posts , like post and follow other users.
Generally the app servers up views templates for particular routes althogh some of the view functions serve as APIs, which handle AJAX calls from the front end (made with javascript).
These calls allow data manipulation or addition on the front end without the need to refresh the page.

On the other hand most operations such as liking posts, following users etc are handled by view functions for particular routes endpoints which perform database transactions such as writing or editing exiting data.


There are also certain routes that require user to be logged in or authenticated to access, like the profile and following page. Beside manually checking whether request is comming from authentcated user, such routes are protected with the `login_required` decorator from the `django.contrib.auth.decorators` module. view functions that handle AJAX calls are protected wit the `csrf_protect` decorator to make sure all calls are coming from within the application and not external by requiring the `csrf token`.

There are a total of 5 models defined for the application in the models.py file. Some models have defined relationships with each other. eg; the user model has a one to many relationship with the post model , this allows a particular user to have a number of post associated  with him or her.

This was overall a fun web app to make.


## How to use
* The only requirement to run the app is the django framework so make sure you have that installed then run the app with `python manage.py runserver` .


## App look


- register page
![home page look](/views/register.png)


- login page
![home page look](/views/login.png)

- home page
![home page look](/views/home1.png)


- profile page
![profile page look](/views/profile.png)

- home page
![home page look](/views/home2.png)
