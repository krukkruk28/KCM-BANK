# KCM Bank

A simple banking application built with Python Flask, featuring user authentication, basic CRUD operations, and a clean web interface.

## 📋 Description

KCM Bank is a lightweight banking application that demonstrates fundamental web development concepts. It provides a simulated banking environment with login functionality and basic account management operations.

## ✨ Features

- **User Authentication**: Secure login system with session management
- **CRUD Operations**: Create, Read, Update, and Delete banking records
- **Database Integration**: Uses SQLite for data storage and management
- **Responsive UI**: Clean and intuitive user interface
- **Flask Backend**: Lightweight Python web framework for efficient backend logic

## 🛠️ Tech Stack

| Language | Usage |
|----------|-------|
| Python | Backend & Core Logic 
| SQLLite3 | Database Management
| HTML | Frontend Markup 
| CSS | Styling & Layout
| JavaScript | Client-side Interactivity

**Core Framework**: Flask (Python)

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/krukkruk28/KCM-BANK.git
cd KCM-BANK
```

2. **Create a virtual environment**:
```bash
python -m venv venv
# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python kcmbank_db.py
```

The application will be accessible at: `http://localhost:5000`

## 📖 Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Dashboard**: View your account information
3. **Manage Accounts**: 
   - Create new accounts
   - View account details
   - Update account information
   - Delete accounts

4. **Logout**: Securely logout from your session
5. **Future enhancements will include**:
- *Fund transfers
- *Transaction history
- *Notifications (text/email) for account activities
- *Fraud detection mechanisms
- *Visualization of data (e.g., charts for transactions)
- *Mobile-friendly version of the application

## 📁 Project Structure

```
KCM-BANK/
├── kcmbank_db.py          # Main Flask application entry point with sqlite3 integration
├── kcmbank.py             # Original Flask application (without sqlite3) - Sample only
├── db.py                  # Database connection and operations
├── test.py                # Test cases for application functionality
├── usersdb.json           # Simulated user database (for demonstration)
├── requirements.txt       # Python dependencies
├── .Dockerfiles           # Docker configuration files (if applicable)
├── .yaml                  # Kubernetes orchestration configuration files (if applicable)
├── templates/             # HTML templates for views
│   ├── login.html
│   ├── login_interface.html
│   └── signup.html
├── static/              # Static files (CSS, JS, images)
│   └── style.css
│   └── login.css
│   └── signup.css
│   └── js/
│   └── img/
├── kcmbank/            # Virtual environment (local only)
└── README.md           # This file
└── instructions_db.txt # Instructions for running the database version
└── instructions.txt    # Instructions for running the original version
└── KCM BANK FLOWCHART.pdf # Flowchart of application logic
└── Snapshots/           # Screenshots of the application in action
```

## 🔧 Configuration

Update configuration settings in `app.py` or create a `.env` file for:
- Database connection strings
- Secret keys
- Flask environment settings

## 📝 Notes

- Due to complexity and domain-specific requirements, this project focuses on demonstrating basic concepts rather than implementing a fully functional banking system
- The application is too simple for real-world banking use and should not be used in production
- Login credentials are simulated
- Creating a full stack application requires guidance from a cybersecurity expert and banking professionals to ensure security and compliance with regulations

## ⚠️ Security Considerations
- Passwords are hashed using bcrypt for security
- SQL queries should be parameterized to prevent SQL injection (not fully implemented in this demo)
- Session management is basic and should be enhanced for production use

## 📊 Future Works and Enhancements
- Implement balance management and transaction history
- Add more robust error handling and input validation especially for database operations
- Enhance UI/UX with better design and responsiveness
- To add more features like fund transfers, account statements, etc.
- To add visualization of data (e.g., charts for transactions)
- To add notifications for account activities
- To add fraud detection mechanisms (e.g., flagging suspicious transactions)
- To create a mobile-friendly version of the application
- To demonstrate deployment in a web hosting environment (e.g., Heroku, AWS)
- To use django instead of flask for better scalability and security features

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available.

## 👤 Author

**krukkruk28**

Feel free to reach out with questions or suggestions!

---

**Last Updated**: 2026-04-12
