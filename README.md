# KCM Bank

A simple banking application built with Python Flask, featuring user authentication, basic CRUD operations, and a clean web interface.

## 📋 Description

KCM Bank is a lightweight banking application that demonstrates fundamental web development concepts. It provides a simulated banking environment with login functionality and basic account management operations.

## ✨ Features

- **User Authentication**: Secure login system with session management
- **CRUD Operations**: Create, Read, Update, and Delete banking records
- **Responsive UI**: Clean and intuitive user interface
- **Flask Backend**: Lightweight Python web framework for efficient backend logic

## 🛠️ Tech Stack

| Language | Usage | Percentage |
|----------|-------|-----------|
| Python | Backend & Core Logic | 96.1% |
| HTML | Frontend Markup | 0.5% |
| CSS | Styling & Layout | 0.4% |
| JavaScript | Client-side Interactivity | 0.5% |
| C / Cython | Performance Optimization | 2.0% |

**Core Framework**: Flask (Python)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
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
python kcmbank.py
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

## 📁 Project Structure

```
KCM-BANK/
├── kcmbank.py                 # Main Flask application entry point
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates for views
│   ├── login.html
│   ├── dashboard.html
│   └── ...
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   └── img/
├── venv/                # Virtual environment (local only)
└── README.md           # This file
```

## 🔧 Configuration

Update configuration settings in `app.py` or create a `.env` file for:
- Database connection strings
- Secret keys
- Flask environment settings

## 📝 Notes

- This is a demonstration/educational project
- Login credentials are simulated
- Not intended for production use

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**krukkruk28**

Feel free to reach out with questions or suggestions!

---

**Last Updated**: 2026-04-02
