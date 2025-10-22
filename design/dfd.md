
# Library Management System DFD (Level 1)

## Summary
- Modular Django REST API for library management
- Membership-based borrow limits (enforced per user)
- Borrow/request/approval flow: Members request books for a location, librarians approve/reject, status tracked
- Book location tracking: Each book is assigned to a location; borrow/return is location-aware

```mermaid
graph LR
    Member["Member (UserProfile)"]
    Librarian["Librarian (UserProfile)"]
    Admin["Admin (UserProfile)"]
    Auth["Authentication System"]

    BookDB["Book (Book)"]
    LocationDB["Location (Location)"]
    BorrowDB["BorrowedBook (BorrowedBook)"]
    ActivityDB["BookActivity (BookActivity)"]
    MembershipDB["MembershipType (MembershipType)"]

    Member -- "Login/Register" --> Auth
    Librarian -- "Login/Register" --> Auth
    Admin -- "Login/Register" --> Auth
    Auth -- "Authenticated User" --> Member
    Auth -- "Authenticated User" --> Librarian
    Auth -- "Authenticated User" --> Admin

    Member -- "Search/Add/Update Book" --> BookDB
    Librarian -- "Add/Update Book" --> BookDB
    Admin -- "Manage Books" --> BookDB
    BookDB -- "Book Info" --> Member
    BookDB -- "Book Info" --> Librarian
    BookDB -- "Book Info" --> Admin
    BookDB -- "Location Info" --> LocationDB
    LocationDB -- "Location Info" --> BookDB

    Member -- "Request Borrow (with Location)" --> BorrowDB
    Librarian -- "Approve/Reject Borrow (at Location)" --> BorrowDB
    Member -- "Return Book" --> BorrowDB
    BorrowDB -- "Borrowing Status" --> Member
    BorrowDB -- "Borrowing Status" --> Librarian
    BorrowDB -- "Location Info" --> LocationDB
    LocationDB -- "Location Info" --> BorrowDB

    Member -- "View/Log Activity" --> ActivityDB
    Librarian -- "View/Log Activity" --> ActivityDB
    Admin -- "View/Log Activity" --> ActivityDB
    ActivityDB -- "Activity Log" --> Member
    ActivityDB -- "Activity Log" --> Librarian
    ActivityDB -- "Activity Log" --> Admin

    Member -- "View/Update Membership" --> MembershipDB
    MembershipDB -- "Membership Info" --> Member
```
