# 🧴 Skin Care Consultation Web App

A Flask-based **Skin Care Consultation System** that helps users analyze their skin type, texture, and condition to recommend suitable skincare products.  
It also includes **admin management**, **product management**, and **review moderation** features.

---

## 🚀 Features

### 👤 User Features
- User **signup/login** with password hashing (SHA-256)
- **Skin assessment form** to analyze and get personalized product recommendations
- **View recommended remedies and skincare products**
- **Write product reviews** and view all reviews
- Logout functionality

### 🧑‍💼 Admin Features
- Admin **login/dashboard**
- **Manage products** (Add, Edit, Delete)
- **Manage reviews** (View/Delete)
- **View user assessments**

---

### 3. Database Setup (Using XAMPP)

**Install XAMPP**  
- Download from [https://www.apachefriends.org/download.html](https://www.apachefriends.org/download.html)  
- Install on your local machine.

**Start Apache and MySQL**  
- Open the XAMPP Control Panel and start **Apache** and **MySQL**.

**Open phpMyAdmin**  
- Go to [http://localhost/phpmyadmin](http://localhost/phpmyadmin)

**Create Database**  
- Click **New**.  
- Enter database name: `skincare`  
- Click **Create**.

**Import `db.sql` File**  
- Select the `skincare` database.  
- Go to the **Import** tab.  
- Upload the `db.sql` file from the repository.  
- Click **Go** to import tables and data.

**Database Connection**  
The app uses the following connection details:

```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # default for XAMPP
    database="skincare"
)
```

### ⚙️ Installation Guide

### 1. Clone the repository
```powershell
git clone https://github.com/Sakshi-21-Hub/skin-care-consultation.git
cd skin-care-consultation
```
### 2. Set up a virtual environment (recommended)
```powershell
python -m venv venv
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate         # On Windows
```
### 3. Install dependencies
```powershell
pip install -r requirements.txt
```
### 4. Configure MySQL Connection
```powershell
Update your MySQL credentials in app.py (inside create_connection()):

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_mysql_password",
        database="skincare"
    )
```
### 5. Run the application
```powershell
python app.py
```
Then open in your browser:

http://localhost:8000

🧠 How It Works
---
- The user signs up and logs in.

- The skin assessment form captures: Skin texture,Skin type,Skin condition

- The system uses TF-IDF vectorization and weighted scores (rating + price) to recommend top skincare products.

- Results are stored in the skin_assessments table and displayed to the user.

💡 Future Enhancements
---
- AI-based image analysis for skin condition detection

- Email notifications for new recommendations

- Admin analytics dashboard (review and user activity insights)

- User profile management

🧑‍💻 Author
---
Developed by Sakshi Khanvilkar

🪪 License
---
This project is licensed under the MIT License.

## Acknowledgments

Thanks to all contributors who have helped with the development

