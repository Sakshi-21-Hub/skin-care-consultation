{% extends "base.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}








<!--        &lt;!&ndash; Skin Assessment Quiz Section &ndash;&gt;-->
<!--        <div class="row mb-5">-->
<!--            <div class="col-md-12">-->
<!--                <h4 class="text-center">Take Our Skin Assessment Quiz</h4>-->
<!--                <form action="{{ url_for('assessment') }}" method="get">-->
<!--                    <button type="submit" class="btn btn-primary">Take the Quiz</button>-->
<!--                </form>-->
<!--            </div>-->
<!--        </div>-->

        <!-- Blog Section -->

  <div class="row mb-8">
    <div class="col-md-12 text-center">
        <h2>Latest Skincare Tips</h2>
        <br>
        <div class="row justify-content-center">
            <div class="col-md-4 col-sm-6 mb-4">
                <div class="blog-post">
                    <h5>How to Manage Oily Skin</h5>
                    <p>Find out the best skincare routine to tackle oily skin and maintain balance...</p>
                </div>
            </div>
            <div class="col-md-4 col-sm-6 mb-4">
                <div class="blog-post">
                    <h5>Anti-Aging Tips You Should Know</h5>
                    <p>Get to know the most effective skincare tips and products for fighting wrinkles...</p>
                </div>
            </div>
            <div class="col-md-4 col-sm-6 mb-4">
                <div class="blog-post">
                    <h5>Understanding Sensitive Skin</h5>
                    <p>Learn how to create a safe skincare routine that works for your sensitive skin...</p>
                </div>
            </div>
        </div>
    </div>
</div>


<!--        &lt;!&ndash; Skin Care Product Catalog with Filters &ndash;&gt;-->
<!--        <div class="row mb-5">-->
<!--            <div class="col-md-12">-->
<!--                <h4 class="text-center">Our Skincare Products</h4>-->
<!--                <div class="product-filter">-->
<!--                    <label for="productCategory">Category:</label>-->
<!--                    <select name="productCategory" id="productCategory">-->
<!--                        <option value="anti-aging">Anti-Aging</option>-->
<!--                        <option value="acne-treatment">Acne Treatment</option>-->
<!--                        <option value="moisturizer">Moisturizers</option>-->
<!--                    </select>-->
 <!--                </div>-->
<!--                <div class="product-list">-->
<!--                    &lt;!&ndash; Loop through each product dynamically &ndash;&gt;-->
<!--                    {% for product in products %}-->
<!--                    <div class="product-item">-->
<!--                        <img src="{{ url_for('static', filename=product.image_path) }}" alt="{{ product.name }}">-->
<!--                        <h5>{{ product.name }}</h5>-->
<!--                        <p>{{ product.description }}</p>-->
<!--                        &lt;!&ndash; Review Form &ndash;&gt;-->
<!--                        <form action="{{ url_for('submit_review') }}" method="post">-->
<!--                            <input type="hidden" name="product_id" value="{{ product.id }}">-->
<!--                            <input type="hidden" name="user_id" value="{{ session['user_id'] }}">-->
<!--                            <textarea name="review_text" placeholder="Write your review here..." required></textarea>-->
<!--                            <button type="submit" class="btn btn-primary">Submit Review</button>-->
<!--                        </form>-->
<!--                    </div>-->
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
</div>

    <style>
      .side-buttons {
    position: fixed;
    right: 20px;
    bottom: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    z-index: 1000;
}

/* Individual side button styling */
.side-btn {
    width: 50px;
    height: 50px;
    background-color: #007bff; /* Default blue for the phone button */
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-decoration: none;
    transition: all 0.3s ease-in-out;
}

/* WhatsApp button specific style */
.side-btn:nth-child(2) {
    background-color: #25d366; /* WhatsApp green */
}



        /* Filter Section */
        .product-filter {
            text-align: center;
            margin-bottom: 20px;
        }

        .product-filter select {
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
            font-size: 1rem;
        }

        /* Centered Text Blocks */
        .text-center h4, .text-center h2 {
            color: #1d3557;
        }

        /* Footer Improvements */
        footer {
            background-color: #1d3557;
            color: #ffffff;
            text-align: center;
            padding: 20px 0;
        }
    </style>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">

{% endblock %}
<div class="side-buttons">
    <a href="tel:+919594451428" class="side-btn" target="_blank">
        <i class="fas fa-phone-alt"></i>
    </a>
    <a href="https://wa.me/9594451428?text=Hello" class="side-btn" target="_blank">
        <i class="fab fa-whatsapp"></i>
    </a>
</div>