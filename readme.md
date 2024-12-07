# Library Management System
This is a library management system(WIP).

## Use-case Diagram

```mermaid
usecaseDiagram
    actor Admin
    actor User

    Admin --> (Manage Books);
    Admin --> (Manage Members);
    Admin --> (Manage Borrowed Books);
    User --> (View Books);
    User --> (Borrow Books);
    User --> (Return Books);

    (Manage Books) --> (Add Book);
    (Manage Books) --> (Edit Book);
    (Manage Books) --> (Delete Book);
    (Manage Members) --> (Add Member);
    (Manage Members) --> (Edit Member);
    (Manage Members) --> (Delete Member);
    (Manage Borrowed Books) --> (Record Borrowing);
    (Manage Borrowed Books) --> (Record Returning);
    ```