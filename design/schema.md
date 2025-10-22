
# Library Management System Schema (Refined)

## Summary (Quick Reference)
- Modular Django REST API for library management
- Membership-based borrow limits (enforced per user)
- Borrow/request/approval flow: Members request books for a location, librarians approve/reject, status tracked
- Book location tracking: Each book is assigned to a location; borrow/return is location-aware
- All detailed docs are in the `design/` folder


```mermaid
erDiagram
    USER ||--|| USERPROFILE : has
    USERPROFILE }o--|| MEMBERSHIPTYPE : has
    USERPROFILE ||--o{ BOOKACTIVITY : logs
    USERPROFILE ||--o{ BORROWEDBOOK : transacts
    AUTHOR ||--o{ BOOK : writes
    BOOK ||--o{ BORROWEDBOOK : is_borrowed
    BOOK ||--o{ BOOKACTIVITY : has_activity
    BOOK }o--|| LOCATION : at
    BORROWEDBOOK }o--|| LOCATION : for

    BOOK {
        string title
        string book_type
        int available_copies
        string status
        date published_date
        string isbn_number
        string locationId
    }

    AUTHOR {
        string name
        string bio
    }

    USER {
        string username
        string password
        string email
    }

    USERPROFILE {
        string role
        string phone
        string address
        decimal pay
        string library_branch
        string region
        string membership_typeId
    }

    MEMBERSHIPTYPE {
        string name
        decimal monthly_price
        int max_books
    }

    BORROWEDBOOK {
        string bookId
        string user_profileId
        string locationId
        string status
        date borrowed_date
        date due_date
        date return_date
    }

    LOCATION {
        string name
        string address
    }

    BOOKACTIVITY {
        string bookId
        string userId
        string activity_type
        datetime timestamp
        string details
    }
```

## User & Roles
- **User** (Django built-in)
- **UserProfile** (one-to-one with User)
  - role: CharField (choices: 'admin', 'librarian', 'member', 'self_checkout')
  - phone, address, etc.
  - membership_type: ForeignKey(MembershipType, null=True, blank=True) (for members)

## MembershipType
- name: CharField
- monthly_price: DecimalField
- max_books: PositiveIntegerField
- ...

## Author
- name: CharField
- bio: TextField

## Book
- title: CharField
- author: ForeignKey(Author)
- published_date: DateField
- isbn_number: CharField (unique)
- book_type: CharField (choices: 'physical', 'virtual')
- available_copies: PositiveIntegerField (for physical books)
- status: CharField (choices: 'available', 'racked', 'discarded', 'purchased')

## BorrowedBook
- book: ForeignKey(Book)
- user_profile: ForeignKey(UserProfile)
- location: ForeignKey(Location)
- status: CharField (choices: 'requested', 'approved', 'rejected', 'returned')
- borrowed_date: DateField
- due_date: DateField
- return_date: DateField (nullable)
- transacted_by: ForeignKey(UserProfile or null for self_checkout)
## Location
- name: CharField
- address: TextField


## BookActivity
- book: ForeignKey(Book)
- user: ForeignKey(UserProfile or null for self_checkout)
- activity_type: CharField (choices: 'borrow', 'return', 'rack', 'purchase', 'discard')
- timestamp: DateTimeField
- details: TextField (optional)

---
- All actions (borrow, return, rack, purchase, discard) are logged in BookActivity with the user (admin/librarian/member/self_checkout) who performed them.
- Virtual books ignore available_copies (treated as unlimited).
- Membership type and borrowing limits are managed in MembershipType and referenced in UserProfile.
- Borrow/request/approval flow: Members request books for a location, librarians at that location approve/reject, status tracked in BorrowedBook.
- Membership enforcement: Members cannot exceed their borrow limit (active borrows only).
- Location enforcement: Only librarians at the book's location can approve/reject requests.
