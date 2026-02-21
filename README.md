# 💰 Personal Finance Tracker

Personal Finance Tracker is a web-based expense management application built using Django. It helps users track their expenses, manage categories, monitor spending habits, and maintain financial records efficiently through a secure and user-friendly interface.

---

## 📖 About

A Django-based web application that allows users to track expenses, manage categories, and monitor personal finances with secure authentication and organized data storage.

---

## 🚀 Features

### 🔐 User Authentication
- Secure user registration and login
- User-specific expense tracking
- Profile management

### 💸 Expense Management
- Add new expenses
- Edit and delete expenses
- Categorize expenses
- Track expense history

### 📂 Category Management
- Create and manage expense categories
- Organize spending efficiently

### 🗄️ Database Integration
- SQLite database support
- Stores user data, expenses, and categories securely

### 📊 Organized Financial Tracking
- View all expenses in structured format
- Monitor spending patterns
- Maintain financial records

---

## 🏗️ Architecture Overview

```
Personal_Finance_Tracker/
│
├── expenseswebsite/        # Main Django project settings
├── expenses/               # Expense management app
├── authentication/         # User authentication app
├── Profile/                # User profile management
├── home/                   # Home and dashboard views
│
├── static/                 # Static files (CSS, JS, images)
├── db.sqlite3              # SQLite database
├── manage.py               # Django management script
│
├── categories.txt         # Default categories
├── currencies.json       # Currency data
└── requiredpip.txt       # Required dependencies
```

---

## 🛠️ Tech Stack

### Backend
- Python
- Django

### Database
- SQLite3

### Frontend
- HTML
- CSS
- JavaScript

### Authentication
- Django Authentication System

---

## ⚙️ Installation and Setup

### 1. Clone the repository

```
git clone https://github.com/YOUR_USERNAME/Personal_Finance_Tracker.git
```

### 2. Navigate to project folder

```
cd Personal_Finance_Tracker
```

### 3. Install dependencies

```
pip install -r requiredpip.txt
```

### 4. Run migrations

```
python manage.py migrate
```

### 5. Run the server

```
python manage.py runserver
```

### 6. Open in browser

```
http://127.0.0.1:8000
```

---

## 📊 Application Workflow

```
User registers/logs in
        ↓
User creates expense categories
        ↓
User adds expenses
        ↓
Expenses stored in database
        ↓
User views and manages expenses
```

---

## 🔑 Core Capabilities

- Secure authentication
- Expense tracking and management
- Category-based organization
- Persistent database storage
- Scalable Django architecture

---

## 🎯 Use Cases

- Personal expense tracking
- Budget management
- Financial record keeping
- Learning Django web development

---

## 🚀 Future Improvements

- Expense analytics and charts
- Monthly reports
- Export to CSV/PDF
- Multi-currency support
- REST API integration
- Docker deployment

---

## 👨‍💻 Author

Utkarsh Mhatre

---

## 📜 License

This project is for educational and portfolio purposes.

---

## ⭐ Summary

Personal Finance Tracker is a secure and scalable Django web application designed to help users manage expenses, organize financial data, and track spending efficiently.
