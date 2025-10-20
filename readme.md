# Library Management System

A modular, testable Django backend for managing library books, users, memberships, borrow requests/approvals, and book locations.

## Features
- Modular Django REST API
- Membership-based borrow limits
- Borrow request/approval flow (with location support)
- Book location tracking
- Comprehensive test suite
- **Auto-accept for virtual books at virtual locations** (see below)

## Core Concepts
- **Membership Types:** Each user has a membership type that determines their borrow limit.
- **Borrow/Request/Approval:** Members request books for a location; librarians approve/reject; status is tracked.
- **Location:** Books and borrow requests are always tied to a specific location.
- **Auto-Accept Virtual:** If `config.ini` has `auto_accept_virtual = true`, and both the book and the selected location are virtual, borrow requests are auto-accepted (status set to "accepted") as long as the user's borrow limit is not exceeded. For all other cases, requests remain pending until approved by a librarian. **You must restart the server after changing the config or code.**

## User Roles & Permissions
- **Admin:** Full access to all features and data.
- **Librarian:** Manage books and approve/reject borrow requests at their location.
- **Member:** Can request/return books, view activity, and manage their membership.

## Quick Start
1. Clone the repo
2. Install requirements: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Run tests: `python manage.py test`
5. Start server: `python manage.py runserver`

## Documentation
- **Project structure, models, and flows:** See [`design/project_structure.md`](design/project_structure.md)
- **API endpoints:** See [`design/api_endpoints.md`](design/api_endpoints.md)
- **Design docs:** All detailed docs are in the [`design/`](design/) folder
- **Setup & environment:** See [`design/project_setup.md`](design/project_setup.md)

## Test Coverage
All business logic, permissions, and flows are covered by tests. See the `tests/` folder for details.

---
For detailed onboarding, extension, or maintenance, always refer to the `design/` folder.
