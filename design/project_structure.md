# Project Structure & Design (Library Management System)

## Summary (Quick Onboarding)
- **Modular Django REST API** for library management
- **Membership-based borrow limits** (enforced per user)
- **Borrow/request/approval flow**: Members request books for a location, librarians approve/reject, status tracked
- **Book location tracking**: Each book is assigned to a location; borrow/return is location-aware
- **Comprehensive test suite**: All business logic and permissions are tested
- **All detailed docs are in this `design/` folder**

---

## Models
- **Book**: title, author, location, etc.
- **Author**: name, bio
- **UserProfile**: user, membership_type, etc.
- **MembershipType**: name, borrow_limit
- **BorrowedBook**: user, book, status (requested/approved/rejected/returned), location, due_date, timestamps
- **Location**: name, address, etc.

## Borrow/Request/Approval Flow
- **Request**: Member requests a book for a specific location and due date
- **Approval**: Librarian at that location approves/rejects the request
- **Status**: BorrowedBook tracks status (requested, approved, rejected, returned)
- **Return**: Member or librarian marks as returned
- **Membership enforcement**: Members cannot exceed their borrow limit (active borrows only)
- **Location enforcement**: Only librarians at the book's location can approve/reject

## API Structure
- Modular views: auth, book, borrow/request, activity, membership
- See [`api_endpoints.md`](api_endpoints.md) for full endpoint list

## Test Coverage
- All business rules, permissions, and flows are covered by tests in `tests/`

## Extension & Maintenance
- All new features must be documented here and tested
- See `readme.md` for high-level overview and onboarding

# Project Structure

A high-level overview of the Library Management System project structure:

```
Library_Management_System/
├── design/
│   ├── api_endpoints.md
│   ├── project_setup.md
│   ├── project_structure.md  # (this file)
│   ├── schema.md
│   ├── sequence_diagrams.md
│   ├── dfd.md
│   ├── testing.md
├── library_management/
│   ├── library/
│   │   ├── api_views/
│   │   ├── migrations/
│   │   ├── tests/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── library_management/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── db.sqlite3
│   └── manage.py
├── requirements.txt
└── README.md
```

- **design/**: Documentation, API, and project description files.
- **library_management/library/**: Main Django app with all models, views, serializers, API logic, and tests.
- **library_management/library/models.py**: Includes Book, Author, UserProfile, MembershipType, BorrowedBook (with request/approval flow), and Location models.
- **library_management/library/api_views/**: Modular API logic for auth, book, borrow/request, activity, membership, etc.
- **library_management/library/tests/**: Unit and integration tests for all major features.
- **requirements.txt**: Python dependencies.
- **README.md**: Project intro and links to design docs.
