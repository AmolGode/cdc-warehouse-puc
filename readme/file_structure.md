data_warehouse_puc/                    ← root folder, everything lives here
│
├── docker-compose.yml                 ← at the root, one level above both projects
│
├── source_project/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── orders/
│       ├── models.py
│       └── migrations/
│
└── warehouse_project/
    ├── Dockerfile
    ├── requirements.txt
    ├── manage.py
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── warehouse/
        ├── models.py
        ├── consumer.py
        └── migrations/