## Personal Portofolio Website - Arsya Khairunissa Budiman

| Information | Details |
|---|---|
| **Name** | Arsya Khairunissa Budiman |
| **NPM** | 2506544076 |
| **Class** | Pemrograman Berbasis Platform (PBP) E |
| **Faculty** | Faculty of Computer Science, Universitas Indonesia |
| **Lecturer** | Daya Adianto, S.Kom., M.Kom. |

## Deployment
[https://arsya-khairunissa-myportofolio.pws.cs.ui.ac.id/](https://arsya-khairunissa-myportofolio.pws.cs.ui.ac.id/)

## About the Project
This project is a personal portfolio website developed to showcase my profile, experiences, projects, and other relevant information in one place. The website is built using Django, HTML5, and CSS3, with project and experience data managed through Django models and displayed dynamically using templates.

## Weekly Progress

| Week | Progress |
|---|---|
| 1 | Set up the Django project, created the Git repository, and installed the required dependencies. |
| 2 | Designed and developed the initial portfolio website using HTML and CSS, including the About, Experience, Education, Projects, and Contact sections. |
| 3 | Implemented the Model-View-Template (MVT) architecture for the Experience and Projects sections, including models, views, URL routing, templates, and database integration. |
| 4 | Implemented complete CRUD functionality for the Experience and Projects sections using ModelForm, including Create, Update, and Delete features. Implemented JSON serialization and deserialization with JSON data delivery endpoints. Added search and category filtering for Experience, along with confirmation pop-ups for data deletion. |


## Documentation & AI Disclosure + Reflective Questions

| No. | Assigment | Answer |
|---|---|---|
| 1 | Static Web with HTML5 and CSS3 | [Tugas1.md](/reflection/TUGAS1.md) |
| 2 | Implementing Model-View-Template (MVT) in Django | [Tugas2.md](/reflection/TUGAS2.md) |
| 3 | Form & Data Delivery | [Tugas3.md](/reflection/TUGAS3.md) |

## Setup and Deployment

### Requirements

- Python 3.10+
- pip
- Git

### Local Preview

Clone this repository
```bash
git clone https://github.com/syakhrnss/myportofolio.git
cd myportofolio
```

Create a virtual environment
```bash
python -m venv env

# Windows (cmd/PowerShell)
env\Scripts\activate

# Unix (macOS/Linux)
source env/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```

Create a .env file in the project root for local configuration:
```
PRODUCTION=False
```

Run migrations and start the server
```bash
python manage.py migrate  # local development uses SQLite by default
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

### Deployment

Production uses PostgreSQL. Create a new project on PWS, then set the following environment variables under the Environs tab:

PRODUCTION=True
```
DB_NAME=<database-name>
DB_USER=<database-user>
DB_PASSWORD=<database-password>
DB_HOST=<database-host>
DB_PORT=<database-port>
SCHEMA=tutorial
```

Add the PWS deployment URL to ALLOWED_HOSTS in settings.py, and make sure WhiteNoiseMiddleware is enabled so static files are served correctly in production.

To push changes to GitHub and PWS:
```bash
git add .
git commit -m "chore: deploy to pws"
git push origin main
git push pws main
```