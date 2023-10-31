from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Configure the MongoDB connection with your actual service name
client = MongoClient('mongodb-service:27017')
db = client['myappdb']  # Use the name of your database, which is 'myappdb'
collection = db['mycollection']  # Use the name of your collection, which is 'mycollection'

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
        collection.insert_one(form_data)

        return "Thank you for submitting the form!"

    # For GET requests, render the contact.html template
    return render_template("contact.html", title="Shubham Thorat")

if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0")
