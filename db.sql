-- Create Database
CREATE DATABASE skincare;

-- Use Database
USE skincare;

-- Create Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    create_dt DATETIME,
    update_dt DATETIME
);

-- Create Admin Table
CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    create_dt DATETIME,
    update_dt DATETIME
);

-- Create Product Table
CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    product_description TEXT,
    product_type VARCHAR(100),
    price DECIMAL(10, 2),
    brand VARCHAR(100),
    rating FLOAT,
    image VARCHAR(255)
);

-- Create Skin Assessments Table
CREATE TABLE skin_assessments (
    assessment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    skin_type VARCHAR(100),
    skin_texture VARCHAR(100),
    skin_condition VARCHAR(100),
    assessment_date DATETIME,
    analysis_results JSON
);

-- Create Product Review Table
CREATE TABLE product_review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    rating FLOAT,
    review_text TEXT,
    review_date DATETIME
);

-- Insert Admin Data
INSERT INTO admin (username, email, password, create_dt, update_dt)
VALUES
('Admin', 'admin@gmail.com', SHA2('admin123', 256), NOW(), NOW());

-- Insert Sample Users
INSERT INTO users (username, email, password, create_dt, update_dt)
VALUES
('Riddhish', 'user1@gmail.com', SHA2('user123', 256), NOW(), NOW()),
('sakshi21', 'user2@gmail.com', SHA2('user456', 256), NOW(), NOW());

-- Insert Product Data
INSERT INTO product (product_name, product_description, product_type, price, brand, rating, image)
VALUES
('Acne Treatment Serum', 'Effective acne treatment with salicylic acid', 'Serum', 799.00, 'Derma Co', 4.7, 'Acne TreatmentSerum.jpg'),
('Anti-Aging Night Cream', 'Reduces wrinkles and fine lines overnight', 'Moisturizer', 999.00, 'Olay', 4.8, 'Anti-Aging NightCream.jpg'),
('Brightening Peel', 'Exfoliating peel for bright and glowing skin', 'Exfoliant', 1200.00, 'Minimalist', 4.6, 'BrighteningPeel.webp'),
('Brightening Vitamin C Serum', 'Boosts collagen and brightens skin', 'Serum', 899.00, 'Plum', 4.8, 'Brightening VitaminCSerum.jpg'),
('Collagen Boosting Face Mask', 'Nourishing face mask with collagen', 'Mask', 600.00, 'The Face Shop', 4.7, 'Collagen BoostingFaceMask.web'),
('Deep Hydration Serum', 'Intense hydration with hyaluronic acid', 'Serum', 850.00, 'Neutrogena', 4.5, 'DeepHydrationSerum.jpg'),
('Exfoliating Scrub', 'Gentle scrub for removing dead skin cells', 'Exfoliant', 550.00, 'Biotique', 4.4, 'ExfoliatingScrub.jpg'),
('Hydrating Facial Cleanser', 'Deep cleansing with hydration', 'Cleanser', 450.00, 'Cetaphil', 4.6, 'Hydrating Facial Cleanser.jpg'),
('Moisturizing Sunscreen SPF50', 'Protects skin from UV rays', 'Moisturizer', 799.00, 'Lotus', 4.8, 'Moisturizing Sunscreen SPF50.jpg'),
('Soothing Aloe Vera Gel', 'Calms and hydrates skin', 'Treatment', 350.00, 'Patanjali', 4.3, 'SoothingAloeVeraGel.jpg');

-- Insert Product Reviews
INSERT INTO product_review (user_id, product_id, rating, review_text, review_date)
VALUES
(1, 1, 5, 'Great serum! Highly recommended.', NOW()),
(2, 2, 4, 'Good cleanser, but a bit drying.', NOW());

-- Check All Tables
SELECT * FROM users;
SELECT * FROM admin;
SELECT * FROM product;
SELECT * FROM product_review;
SELECT * FROM skin_assessments;
