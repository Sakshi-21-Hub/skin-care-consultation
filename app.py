from flask import Flask, render_template, request, redirect, url_for, session,flash
import mysql.connector
from mysql.connector import Error
import hashlib
import secrets
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)

# Set the secret key for sessions
app.secret_key = secrets.token_hex(16)  # Set your secret key here
UPLOAD_FOLDER = "static/img/product"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Database connection function
def create_connection():
    return mysql.connector.connect(
        host="localhost",  # host
        user="root",  # MySQL username
        password="",  # MySQL password
        database="skincare"  # database name
    )

# Password hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Route for Home (Login page)
@app.route('/')
def home():
    return render_template('login.html')

# Route for Dashboard (after login)
@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user' not in session or 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect to login if not logged in

    username = session['user']  # Get the logged-in user's username
    return render_template('dashboard.html', username=username)

@app.route('/admindash')
def admindash():
    if 'user' not in session:
        return redirect(url_for('home'))  # Redirect to login if not logged in
    if 'user' not in session or 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in as admin

    username = session['user']  # Get the logged-in user's username
    return render_template('admindash.html', username=username)



@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user_type = request.form['user_type']

    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Determine the correct table and password handling based on user type
        if user_type == 'user':
            table = 'users'
            query = f"SELECT * FROM {table} WHERE email = %s AND password = %s"
            hashed_password = hash_password(password)
            credentials = (email, hashed_password)
        elif user_type == 'admin':
            table = 'admin'
            query = f"SELECT * FROM {table} WHERE email = %s AND password = %s"
            hashed_password = hash_password(password)
            credentials = (email, hashed_password)
        else:
            return "Invalid user type."


        # Execute the query
        cursor.execute(query, credentials)
        result = cursor.fetchone()

        if result:
            session['user'] = result['username']
            session['user_id'] = result['user_id']  # to store the user_id in the session

            # Redirect based on user type
            if user_type == 'admin':
                return redirect(url_for('admindash'))  # Redirect to admin dashboard
            else:
                return redirect(url_for('dashboard'))  # Redirect to general dashboard
        else:
            flash("Login failed. Invalid email or password.", "error")
            return redirect(url_for('home'))
    except Error as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for('home'))
    finally:
        # error handling
        try:
            cursor.fetchall()
        except mysql.connector.errors.InterfaceError:
            pass
        finally:
            cursor.close()
            connection.close()


# Route for Signup (Registration page)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle form submission (sign up the user)
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            connection = create_connection()
            cursor = connection.cursor()
            hashed_password = hash_password(password)
            cursor.execute("""INSERT INTO users (username, email, password, create_dt, update_dt)
                              VALUES (%s, %s, %s, NOW(), NOW())""",
                           (username, email, hashed_password))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('home'))  # Redirect to login page after successful sign-up
        except Error as e:
            return f"An error occurred: {e}"

    return render_template('signup.html')  # Show the sign-up form if GET request

# Route for Logout (Clear session)
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))  # Redirect to home (login page) after logout


# Route for Assessment Page
@app.route('/assessment')
def assessment():
    if 'user' not in session or 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in as admin
    return render_template('assessment.html')


# admin view of reviews
@app.route('/admin/reviews')
def admin_reviews():
    if 'user' not in session or 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in as admin

    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch all reviews
        cursor.execute("SELECT * FROM product_review ORDER BY review_date DESC")
        reviews = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('admin_reviews.html', reviews=reviews)
    except Error as e:
        return f"An error occurred: {e}"

# admin review delete
@app.route('/admin/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    if 'user' not in session or 'user_id' not in session:
        return redirect(url_for('home'))  # Ensure only logged-in admins can delete reviews

    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Delete the review with the given review_id
        cursor.execute("DELETE FROM product_review WHERE review_id = %s", (review_id,))
        connection.commit()

        flash('Review deleted successfully!', 'success')
    except Exception as e:
        flash(f"Error deleting review: {e}", "danger")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('admin_reviews'))


@app.route('/admin/dashboard', endpoint='admindashboard')
def admindash():
    if 'user' not in session or 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in as admin
    else:
        return render_template('admindash.html')

@app.route('/admin/product')
def adminproduct():
    if 'user' not in session or 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in as admin
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch all products from the database
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('adminproduct.html', products=products)
    except Error as e:
        return f"An error occurred: {e}"


# Function to check allowed file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/admin/product/add', methods=['GET', 'POST'])
def add_product():
    if 'user' not in session or 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in as admin

    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        if request.method == 'POST':
            # Get product details from the form
            product_name = request.form['product_name']
            product_description = request.form['product_description']
            product_type = request.form['product_type']
            price = request.form['price']
            brand = request.form['brand']
            rating = request.form['rating']

            # Handle image upload
            image_file = request.files['image']
            image_filename = None  # Default if no image uploaded

            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)  # Secure the filename
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)  # Full path
                image_file.save(image_path)  # Save the image in static folder
                image_filename = filename  # Store only the filename in DB

            # Insert the new product into the database
            insert_query = """
            INSERT INTO product (product_name, product_description, product_type, price, brand, rating, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query,
                           (product_name, product_description, product_type, price, brand, rating, image_filename))
            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for('adminproduct'))  # Redirect to product management page

        return render_template('addproduct.html')
    except Error as e:
        return f"An error occurred: {e}"

# admin edit product
@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'user' not in session or 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in as admin

    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch current product details
        cursor.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            return "Product not found!", 404  # Handle case where product doesn't exist

        if request.method == 'POST':
            # Get updated product details from the form
            product_name = request.form['product_name']
            product_description = request.form['product_description']
            product_type = request.form['product_type']
            price = request.form['price']
            brand = request.form['brand']
            rating = request.form['rating']

            # Handle optional image upload
            image_file = request.files['image']
            image_filename = product['image']  # Keep old image if no new one is uploaded

            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)  # Secure the filename
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)  # Full path
                image_file.save(image_path)  # Save the new image
                image_filename = filename  # Update the image filename

            # Update the product in the database
            update_query = """
            UPDATE product
            SET product_name = %s, product_description = %s, product_type = %s, price = %s, brand = %s, rating = %s, image = %s
            WHERE product_id = %s
            """
            cursor.execute(update_query, (
            product_name, product_description, product_type, price, brand, rating, image_filename, product_id))
            connection.commit()

            cursor.close()
            connection.close()

            return redirect(url_for('adminproduct'))  # Redirect back to the product management page

        cursor.close()
        connection.close()

        return render_template('editproduct.html', product=product)
    except Error as e:
        return f"An error occurred: {e}"

# Load product data from the database
def get_product_data():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace with your MySQL password
            database="skincare"
        )
        query = "SELECT product_id, product_name, product_description, product_type, price, brand, rating, image FROM product"
        product_df = pd.read_sql(query, connection)
        return product_df
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    finally:
        if connection.is_connected():
            connection.close()


# Skin condition to product type mapping
CONDITION_TO_TYPE = {
    "Acne": ["Treatment", "Cleanser", "Serum"],
    "Aging": ["Moisturizer", "Mask", "Serum"],
    "Pigmentation": ["Serum", "Exfoliant", "Treatment"],
    "Open Pores": ["Mask", "Cleanser", "Exfoliant"],
}


# Analyze skin and recommend products
def analyze_skin(skin_texture, skin_type, skin_condition):
    # Fetch product data
    product_data = get_product_data()
    if product_data.empty:
        return {"products": [], "remedy": "No products available."}

    # Filter products based on condition
    relevant_types = CONDITION_TO_TYPE.get(skin_condition, [])
    filtered_products = product_data[product_data["product_type"].isin(relevant_types)]

    if filtered_products.empty:
        return {"products": [], "remedy": "No suitable products found for this condition."}

    # Create a TF-IDF vectorizer to analyze descriptions
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(filtered_products["product_description"])

    # Add weights for ratings and prices to prioritize top-rated products
    filtered_products["rating_weight"] = filtered_products["rating"] / 5.0
    filtered_products["price_weight"] = 1 - (filtered_products["price"] / filtered_products["price"].max())

    # Combine TF-IDF similarity with weighted scores
    weighted_scores = (0.7 * filtered_products["rating_weight"] + 0.3 * filtered_products["price_weight"]).values

    # Sort by weighted scores
    filtered_products["final_score"] = weighted_scores
    recommended_products = filtered_products.sort_values(by="final_score", ascending=False)

    # Format output
    top_products = recommended_products.head(5)
    remedies = f"Recommended remedies for {skin_condition}: Use products like {', '.join(relevant_types)}"

    return {
        "products": top_products.to_dict(orient="records"),
        "remedy": remedies
    }


@app.route('/submit_assessment', methods=['POST'])
def submit_assessment():
    if 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect to login if not logged in

    user_id = session['user_id']
    skin_texture = request.form['skin_texture']
    skin_type = request.form['skin_type']
    skin_condition = request.form['skin_condition']

    # Analyze skin
    analysis_results = analyze_skin(skin_texture, skin_type, skin_condition)
    # Format the product details properly for display
    formatted_products = [
        {
            "name": product["product_name"],
            "description": product["product_description"],
            "brand": product["brand"],
            "price": f"₹{product['price']}",  # Format price properly
            "image": product["image"],
        }
        for product in analysis_results["products"]
    ]

    formatted_results = {
        "products": formatted_products,
        "remedy": analysis_results["remedy"],
    }

    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Insert the assessment into the database
        cursor.execute("""
               INSERT INTO skin_assessments (user_id, skin_type, skin_texture, skin_condition, assessment_date, analysis_results)
               VALUES (%s, %s, %s, %s, NOW(), %s)
           """, (user_id, skin_type, skin_texture, skin_condition, json.dumps(formatted_results)))

        connection.commit()
        cursor.close()
        connection.close()

        return render_template('assessment_results.html', results=formatted_results)  # Render the results page
    except Error as e:
        return f"An error occurred: {e}"


@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'user' not in session or 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in as admin
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Delete the product from the database
        cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('adminproduct'))  # Redirect back to the product management page
    except Error as e:
        return f"An error occurred: {e}"


# Route for Review Page
@app.route('/reviews')
def reviews():
    if 'user' not in session or 'user_id' not in session:
        return redirect(url_for('home'))
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch reviews from the product_review table
        query_reviews = """
        SELECT review_id, user_id, product_id, rating, review_text, review_date
        FROM product_review
        ORDER BY review_id ASC
        """
        cursor.execute(query_reviews)
        reviews = cursor.fetchall()

        # Fetch all products to populate the review form
        query_products = "SELECT product_id, product_name FROM product"
        cursor.execute(query_products)
        products = cursor.fetchall()

        cursor.close()
        connection.close()

        # Pass the reviews and products data to the template
        return render_template('review.html', reviews=reviews, products=products)
    except Error as e:
        return f"An error occurred: {e}"


@app.route('/product')
def product():
    if 'user' not in session or 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in as admin
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch all products from the product table
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template('product.html', products=products)  # Pass products to the template
    except Error as e:
        return f"An error occurred: {e}"


@app.route('/add_review', methods=['POST'])
def add_review():
    if 'user' not in session:
        print("User not in session")
        return redirect(url_for('home'))

    print("Session user_id:", session.get('user_id'))

    user_id = session['user_id']
    product_id = request.form['product_id']
    rating = request.form['rating']
    review_text = request.form['review_text']

    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Insert the new review into the database
        cursor.execute("""
             INSERT INTO product_review (user_id, product_id, rating, review_text, review_date)
             VALUES (%s, %s, %s, %s, NOW())
         """, (user_id, product_id, rating, review_text))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('reviews'))  # Redirect back to the reviews page
    except Error as e:
        return f"An error occurred: {e}"



if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)
