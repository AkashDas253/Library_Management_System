# Library Management System

## Overview

The **Library Management System** is a Django-based web application designed to manage books, authors, members, and borrowed books in a library. It allows librarians to manage books and authors, track member activities, and handle borrowing/returning books efficiently. The project is built with **Django Rest Framework (DRF)** to provide RESTful APIs for easy integration and frontend access.

## Features

- **Author Management**: Create, read, and update author details.
- **Book Management**: Add, update, and delete books in the system.
- **Member Management**: Add, update, and manage library members.
- **Book Borrowing and Returning**: Track the borrowing and returning of books by members.
- **API Endpoints**: Full CRUD operations exposed via RESTful APIs.
- **Authentication**: Token-based authentication to secure endpoints.
- **Unit Testing**: Includes test cases to ensure the stability and correctness of the system.

---

## Technologies Used

- **Django**: A high-level Python web framework.
- **Django Rest Framework (DRF)**: For building the API layer.
- **SQLite**: Default database for development and testing (easily replaceable with other databases like PostgreSQL).
- **Python 3.x**: Programming language.
- **pytest / unittest**: For running test cases and ensuring application quality.

---

## Getting Started

### Prerequisites

Before you begin, ensure that you have the following installed on your machine:

- **Python 3.x**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package installer.

### Installation

Follow these steps to set up the project on your local machine:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:

   Ensure that your database is set up by running the following:

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for Django admin)**:

   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to create the admin user.

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

   Now, your application should be running on `http://127.0.0.1:8000/`.

---

## API Endpoints

The following API endpoints are available for interacting with the system:

### Author Endpoints

- `GET /api/authors/`: List all authors.
- `POST /api/authors/`: Create a new author.
- `GET /api/authors/{id}/`: Retrieve details of a specific author.
- `PUT /api/authors/{id}/`: Update an author's details.
- `DELETE /api/authors/{id}/`: Delete an author.

### Book Endpoints

- `GET /api/books/`: List all books.
- `POST /api/books/`: Create a new book.
- `GET /api/books/{id}/`: Retrieve details of a specific book.
- `PUT /api/books/{id}/`: Update a book's details.
- `DELETE /api/books/{id}/`: Delete a book.

### Member Endpoints

- `GET /api/members/`: List all members.
- `POST /api/members/`: Create a new member.
- `GET /api/members/{id}/`: Retrieve details of a specific member.
- `PUT /api/members/{id}/`: Update a member's details.
- `DELETE /api/members/{id}/`: Delete a member.

### Borrowed Book Endpoints

- `GET /api/borrowed-books/`: List all borrowed books.
- `POST /api/borrowed-books/`: Create a new borrowed book record.
- `GET /api/borrowed-books/{id}/`: Retrieve details of a borrowed book.
- `PUT /api/borrowed-books/{id}/`: Update a borrowed book's details.
- `DELETE /api/borrowed-books/{id}/`: Delete a borrowed book record.

---

## Running Tests

To run the test suite and ensure the system is working as expected, use the following command:

```bash
python manage.py test
```

Tests are located in the `library/tests/test_api.py` file and include:

- Author creation and retrieval tests.
- Book creation and retrieval tests.
- Member management and borrowing book tests.

---

## Project Structure

```plaintext
library_management/
├── library/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests/
│   │   └── test_api.py
├── db.sqlite3
├── manage.py
└── requirements.txt
```

- **models.py**: Contains the data models for authors, books, members, and borrowed books.
- **views.py**: Contains API views that handle requests for different resources.
- **serializers.py**: Serializes model data into JSON format for API responses.
- **urls.py**: Maps API endpoints to views.
- **tests/test_api.py**: Contains unit tests to ensure the application behaves as expected.

---
<!-- 
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

--- -->

## Contributing

Feel free to fork this repository and submit pull requests for new features, improvements, or bug fixes.

1. Fork the project
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a pull request

---
