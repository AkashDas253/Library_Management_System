# Project Setup & Installation Guide

Moved from the main README for clarity. This file contains all setup, installation, and environment instructions for the Library Management System.

## Prerequisites
- Python 3.x
- pip

## Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser (optional, for admin):
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

For API usage, testing, and endpoint details, see the main README.
