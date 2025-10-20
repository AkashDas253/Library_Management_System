# API Endpoints

- **POST /api/register/** — Register a new user (returns token, requires membership_type_id)
- **POST /api/login/** — Login with username and password (returns token)
- **GET /api/books/** — List all books
- **POST /api/books/** — Add a new book (librarian only)
- **GET /api/books/{id}/** — Get details of a specific book
- **PATCH /api/books/{id}/** — Update a book (librarian only)
- **DELETE /api/books/{id}/** — Delete a book (librarian only)
- **POST /api/borrowedbooks/borrow/** — Request to borrow a book (member/librarian, requires book, location, due_date)
- **POST /api/borrowedbooks/{id}/approve/** — Approve a borrow request (librarian at location only)
- **POST /api/borrowedbooks/{id}/reject/** — Reject a borrow request (librarian at location only)
- **POST /api/borrowedbooks/{id}/return/** — Return a borrowed book (member/librarian)
- **GET /api/activities/my-activity/** — View your own activity log (member only)
- **POST /api/activities/log/** — Log a book activity (member only)
- **GET /api/membership/{id}/** — View your membership details (member only)
- **PATCH /api/membership/{id}/** — Update your membership (member only, only if no active borrows)
