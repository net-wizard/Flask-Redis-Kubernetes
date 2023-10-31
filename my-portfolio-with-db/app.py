import json
from flask import Flask, render_template, request, redirect
#from pymongo import MongoClient
import redis
import os

app = Flask(__name__)

# Configure the MongoDB connection with your actual service name

db_host = os.environ.get("DB_HOST")
db_pass = os.environ.get("DB_PASS")
db_port = int(os.environ.get("DB_PORT"))
db = int(os.environ.get("DB_NAME") ) # Use the name of your database, which is 'myappdb'
table = os.environ.get("DB_TABLE")  # Use the name of your collection, which is 'mycollection'
redis_conn = redis.StrictRedis(host=db_host, port=db_port, db=db,password=db_pass)

@app.route('/')
def home():
    return render_template("index.html", title="Shubham Thorat")

@app.route('/about')
def about():
    return render_template("about.html", title="Shubham Thorat")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission here
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Store the form data in the MongoDB collection
        form_data = {
            'name': name,
            'email': email,
            'message': message
        }
        # collection.insert_one(form_data)
        # Serialize the data to JSON before storing in Redis
        try:
            redis_conn.rpush('contact_forms', json.dumps(form_data))
        except redis.exceptions.ConnectionError as e:
            # Return the exact error message in the return statement
            return f"An error occurred while trying to submit the form: {e.message}"

        return "Thank you for submitting the form!"

    # For GET requests, render the contact.html template
    return render_template("contact.html", title="Shubham Thorat")

if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0")
