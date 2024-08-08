BOOK LAND


Welcome to the Social Media E-commerce Web App! This project integrates social media features with e-commerce functionality, providing users with a seamless experience to shop, share, and connect.

Table of Contents
Introduction
Features
Technologies Used
Installation
Usage
API Documentation
Contributing
License
Contact
Introduction
This web application is designed to combine the best aspects of social media and e-commerce for book lovers. Users can browse products, make purchases, and share their favorite items with friends and followers.

Features
User authentication and authorization
Product listings and detailed views
Shopping cart and checkout process
Social media integration (Wishlist, Comments)
Admin dashboard for product and order management
Technologies Used
Frontend:

HTML, CSS, JavaScript
DTL (JINJA)
Bootstrap
Backend:

Python
Django
SQLite
Database:

PostgreSQL
Installation
Prerequisites
Python 3.8+
Django
Steps
Set up a virtual environment:

python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
Install backend dependencies:

pip install -r requirements.txt
Set up the database:

python manage.py makemigrations accounts
python manage.py migrate accounts

python manage.py makemigrations admins
python manage.py migrate admins

python manage.py makemigrations website
python manage.py migrate website

python manage.py migrate
Create a superuser for admin access:

python manage.py createsuperuser
Run the development servers:

python manage.py runserver
Usage
Navigate to http://localhost:8000 to access the backend admin panel.
Navigate to http://localhost:3000 to access the frontend user interface.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Developed By Exarth
For details on this project and more visit out site exarth.com



Contact
For any inquiries, please contact hesham.fractured@gmail.com.

