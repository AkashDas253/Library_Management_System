# Project Structure

A high-level overview of the Library Management System project structure:

```
Library_Management_System/
├── design/
│   ├── api_endpoints.md
│   ├── INSTALL.md
│   ├── PROJECT_DESCRIPTION.md
│   └── project_structure.md  # (this file)
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
- **library_management/library_management/**: Django project settings and root URLs.
- **requirements.txt**: Python dependencies.
- **README.md**: Project intro and links to design docs.
