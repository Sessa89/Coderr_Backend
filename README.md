# Coderr Backend

![Coderr Logo](logo_coderr.svg)

This repository contains the Django REST Framework–based backend for **Coderr**, a simple freelancer platform connecting customers and businesses through offers, orders, and reviews.

---

## Getting Started

### Backend Setup

1. **Create a virtuel environment**
    ```bash
    python3 -m venv env
    ```
    ```bash
    source env/bin/activate   # macOS/Linux
    ```
    ### or
    ```bash
    .\env\Scripts\Activate.ps1  # Windows PowerShell
    ```

2. **Install Python dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Apply database migrations**
    ```bash
    python manage.py makemigrations
    ```
    ```bash
    python manage.py migrate
    ```

4. **Optional: Create a superuser**
    ```bash
    python manage.py createsuperuser
    ```

5. **Run the backend server**
    ```bash
    python manage.py runserver
    ```

    The API will be available at "http://127.0.0.1:8000"

---

### Frontend Setup ("https://github.com/Sessa89/Coderr_Frontend")

1. **Open the frontend folder**  
    In your code editor (e.g., VS Code), open the frontend directory.

2. **Start a local static server**
    - Right-click on index.html (inside frontend) and select "Open with Live Server" if you have VS Code Live Server installed
    - The frontend will run at "http://127.0.0.1:5500/"

---

## Features

- **User Registration & Login**  
  - Register a new account (username, email, password)
  - Obtain a DRF Token upon login

- **Profile Management**  
  - Customers & Business profiles  
  - View / update your profile  

- **Offers**  
  - Business users can create, list, retrieve, update & delete offers  
  - Each offer has multiple “details”: title, revisions, delivery time, price, features, type  
  - Filtering, sorting, pagination

- **Orders**  
  - Customers place orders on specific offer details  
  - Business users see & update their incoming orders (“in_progress” => “completed” / “cancelled”)  
  - Staff users and/or Admin can delete orders 

- **Reviews**  
  - Customers can leave one review per business user  
  - List, create, update & delete reviews  
  - Filter & sort by rating or date

- **Base Info**  
  - Public endpoint reporting total reviews, average rating, total businesses & offers

---