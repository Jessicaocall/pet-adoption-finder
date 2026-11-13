# Pet Adoption Finder

**INFO8021 DevOps Strategy and Automation** – Jessica O'Callaghan (R00245879)

Pet Adoption Finder is a Flask web application that brings animals from rescue
shelters around Cork into one place. Adopters can browse and filter animals and
send an adoption enquiry to the shelter. The data is stored in a PostgreSQL database.

## Technologies
| Technology | Version |
|---|---|
| Python | 3.13 |
| Flask | 3.1.3 |
| Flask-WTF | 1.3.0 |
| psycopg2-binary | 2.9.13 |
| python-dotenv | 1.2.3 |
| PostgreSQL | 18 |

## Project structure
```
PetAdoptionFinder/
├── app/
│   ├── static/style.css
│   ├── templates/        (base, index, about, login)
│   ├── __init__.py
│   ├── db.py             (connects Flask to PostgreSQL)
│   ├── forms.py
│   └── routes.py
├── data/                 (CSV files used to populate the database)
├── config.py
├── initialise_db.py      (creates the database and tables)
├── populate_db.py        (fills the tables with data)
├── petfinder.py
├── requirements.txt
└── schema.sql            (SQL for the tables and relationships)
```

## How to run
1. Install PostgreSQL 18 (user `postgres`, password `postgres`, port `5432`).
2. Open a terminal in this folder and run:
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python initialise_db.py
python populate_db.py
flask run
```
3. Open http://127.0.0.1:5000

## Branches
| Branch | Contents |
|---|---|
| `main` | Initial website – Home and About Us pages (no database functionality) |
| `feature/browse-animals` | Browse Pets page – lists animals from the database with species and size filters |
| `feature/adoption-enquiry` | Adoption Enquiry page – saves enquiries to the database and shows recent enquiries |

## Database
Five tables: `shelters`, `users`, `animals`, `favourites` and `enquiries`.
The sample data in the `data` folder is fictional and was generated with AI for testing.
