# Library Management System – Sequence Diagrams

This document contains sequence diagrams for the main endpoints/processes identified from the DFD. Diagrams are written in Mermaid syntax for easy integration and visualization.

## 1. Login/Register (Authentication)

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant APIView
    participant AuthSystem
    participant UserProfileDB
    User->>Frontend: Fill and submit login/register form
    Frontend->>APIView: Send login/register request (JSON)
    APIView->>AuthSystem: Validate credentials/data
    alt Register
        AuthSystem->>UserProfileDB: Create new user profile
        UserProfileDB-->>AuthSystem: Success/failure
    else Login
        AuthSystem->>UserProfileDB: Fetch user profile
        UserProfileDB-->>AuthSystem: User data
        AuthSystem->>AuthSystem: Check password
    end
    AuthSystem-->>APIView: Auth result (token/session or error)
    APIView-->>Frontend: Return JSON response (token or error)
    Frontend-->>User: Show dashboard or error
```

---

## 2. Search/Add/Update Book (Book Management)

```mermaid
sequenceDiagram
    participant Member
    participant Librarian
    participant Admin
    participant Frontend
    participant APIView
    participant BookDB
    Member->>Frontend: Request search book
    Librarian->>Frontend: Request search/add/update book
    Admin->>Frontend: Request search book
    Frontend->>APIView: Send API request (JSON)
    alt Search Book
        APIView->>BookDB: Query books
        BookDB-->>APIView: Return book list/details
        APIView-->>Frontend: Return JSON results
        Frontend-->>Member: Show results
        Frontend-->>Librarian: Show results
        Frontend-->>Admin: Show results
    else Add Book (Librarian only)
        APIView->>BookDB: Insert new book
        BookDB-->>APIView: Success/failure
        APIView-->>Frontend: Return JSON result
        Frontend-->>Librarian: Show confirmation/error
    else Update Book (Librarian only)
        APIView->>BookDB: Update book record
        BookDB-->>APIView: Success/failure
        APIView-->>Frontend: Return JSON result
        Frontend-->>Librarian: Show confirmation/error
    end
```

---

## 3. Borrow/Return Book (Borrowing Process)

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant APIView
    participant BorrowDB
    participant BookDB
    User->>Frontend: Request borrow/return book
    Frontend->>APIView: Send API request (JSON)
    alt Borrow Book
        APIView->>BookDB: Check book availability
        BookDB-->>APIView: Available/unavailable
        alt Available
            APIView->>BorrowDB: Create borrow record
            BorrowDB-->>APIView: Success/failure
            APIView-->>Frontend: Return JSON result
            Frontend-->>User: Show confirmation/error
        else Unavailable
            APIView-->>Frontend: Return not available
            Frontend-->>User: Show not available
        end
    else Return Book
        APIView->>BorrowDB: Update borrow record (return)
        BorrowDB-->>APIView: Success/failure
        APIView-->>Frontend: Return JSON result
        Frontend-->>User: Show confirmation/error
    end
```

---

## 4. View/Log Activity (Activity Tracking)

```mermaid
sequenceDiagram
    participant Member as "User (Member role)"
    participant Frontend
    participant APIView
    participant UserProfileDB
    participant ActivityDB
    Note over Member,APIView: Only users with 'member' role can perform activity actions
    Member->>Frontend: Request to view/log activity
    Frontend->>APIView: Send API request (JSON)
    APIView->>UserProfileDB: Get user profile for member
    alt View Activity
        APIView->>ActivityDB: Query activity logs for user profile
        ActivityDB-->>APIView: Return activity data
        APIView-->>Frontend: Return JSON data
        Frontend-->>Member: Show activity log
    else Log Activity
        APIView->>ActivityDB: Insert new activity record (with user profile)
        ActivityDB-->>APIView: Success/failure
        APIView-->>Frontend: Return JSON result
        Frontend-->>Member: Show confirmation/error
    end
```

---

## 5. View/Update Membership (Membership Management)

```mermaid
sequenceDiagram
    participant Member as "User (Member role)"
    participant Frontend
    participant APIView
    participant UserProfileDB
    participant MembershipDB
    Note over Member,APIView: Only users with 'member' role can view/update membership
    Member->>Frontend: Request to view/update membership
    Frontend->>APIView: Send API request (JSON)
    APIView->>UserProfileDB: Get user profile for member
    alt View Membership
        APIView->>MembershipDB: Query membership details (with user profile)
        MembershipDB-->>APIView: Return membership data
        APIView-->>Frontend: Return JSON data
        Frontend-->>Member: Show membership info
    else Update Membership
        APIView->>MembershipDB: Update membership record (with user profile)
        MembershipDB-->>APIView: Success/failure
        APIView-->>Frontend: Return JSON result
        Frontend-->>Member: Show confirmation/error
    end
```

---
