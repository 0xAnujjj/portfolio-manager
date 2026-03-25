# Django Learning Reference
> Personal reference guide — built while learning Django from scratch

---

## Mental Models

### Data Science Python vs Django Python
| Data Science | Django (Web Backend) |
|---|---|
| Python as a calculator | Python as a waiter |
| Feed data → get output | Listen for requests → talk to DB → send response |
| Scripts run once | Server runs forever, waiting |

### The Django Request Cycle
```
Browser Request → URLs → View → Model → Template → Response
```
Every single webpage in Django follows this cycle. Always.

### Your OOP Knowledge → Django
| C++ / What you know | How Django uses it |
|---|---|
| `class Student { }` | `class Project(models.Model):` |
| Constructor | `__init__(self)` — runs automatically on object creation |
| `this->name` | `self.name` |
| Inheritance `class Dog : public Animal` | `class Project(models.Model):` |
| Methods | Views, form validation, `__str__` |

---

## Project Structure

```
taskkk/                     ← your root project folder
│
├── manage.py               ← command center, use this for everything
├── db.sqlite3              ← your database file (auto created)
├── venv/                   ← virtual environment box (don't touch)
│
├── portfolio/              ← project settings folder
│   ├── settings.py         ← configuration (installed apps, database, secret key)
│   ├── urls.py             ← master URL router for the whole project
│   ├── wsgi.py             ← server entry point (ignore for now)
│   └── asgi.py             ← async server entry point (ignore for now)
│
└── projects/               ← your app (one feature = one app)
    ├── models.py           ← define database tables as Python classes
    ├── views.py            ← handle requests, fetch data, return pages
    ├── urls.py             ← URL routes for this app (you create this file)
    ├── admin.py            ← register models to manage in admin panel
    ├── apps.py             ← app config (rarely touched)
    ├── tests.py            ← write tests (ignore for now)
    └── migrations/         ← auto-generated DB instructions (don't edit manually)
```

---

## Key Files Explained

### manage.py
Your command center. You never edit this file — you just run commands with it.
```bash
python manage.py runserver        # start the development server
python manage.py makemigrations   # create DB instructions from models.py
python manage.py migrate          # apply those instructions to the database
python manage.py createsuperuser  # create an admin account
python manage.py startapp <name>  # create a new app
```

### portfolio/settings.py
The brain of your project. Key things to know:
- `INSTALLED_APPS` — list of all apps Django knows about. Every new app you create must be added here.
- `DATABASES` — database config (SQLite by default, PostgreSQL later)
- `DEBUG = True` — shows detailed errors during development. Set to False in production.
- `SECRET_KEY` — never share this publicly

### projects/models.py
Where you define your database tables as Python classes.
```python
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)      # short text
    description = models.TextField()              # long text
    created_at = models.DateTimeField(auto_now_add=True)  # auto timestamp

    def __str__(self):
        return self.title   # what shows in admin panel
```
Every time you change this file → run `makemigrations` → run `migrate`.

### projects/views.py
Where you handle requests and return pages.
```python
from django.shortcuts import render
from .models import Project

def project_list(request):
    projects = Project.objects.all()   # fetch all projects from DB
    return render(request, 'projects/project_list.html', {'projects': projects})
```

### projects/admin.py
Register your models here so they appear in the admin panel.
```python
from django.contrib import admin
from .models import Project

admin.site.register(Project)
```

---

## Common Field Types (models.py)

| Field | Use for |
|---|---|
| `CharField(max_length=200)` | Short text (titles, names) |
| `TextField()` | Long text (descriptions, content) |
| `IntegerField()` | Numbers |
| `BooleanField()` | True/False |
| `DateTimeField(auto_now_add=True)` | Timestamp, auto-set on creation |
| `DateTimeField(auto_now=True)` | Timestamp, auto-updates on every save |
| `ImageField()` | Image uploads |
| `ForeignKey()` | Link to another model (relationship) |

---

## Commands Cheat Sheet

### Starting a brand new project
```bash
# 1. Create and navigate to your project folder
mkdir myproject
cd myproject

# 2. Create virtual environment
python -m venv venv

# 3. Activate it (Windows)
venv\Scripts\activate

# 4. Install Django
pip install django

# 5. Create Django project (the dot keeps it in current folder)
django-admin startproject projectname .

# 6. Run the server to verify
python manage.py runserver
```

### Resuming work on an existing project (every time you return)
```bash
# 1. Navigate to your project folder
cd d:/PROJECTS/taskkk

# 2. Activate virtual environment (VS Code may do this automatically)
venv\Scripts\activate

# 3. Start the server
python manage.py runserver
```

### Creating a new app inside your project
```bash
python manage.py startapp appname

# Then add 'appname' to INSTALLED_APPS in portfolio/settings.py
```

### Database workflow (every time you change models.py)
```bash
python manage.py makemigrations   # step 1: create instructions
python manage.py migrate          # step 2: apply to database
```

### Admin panel
```bash
# Create superuser (only once)
python manage.py createsuperuser

# Then visit: http://127.0.0.1:8000/admin
```

---

## Virtual Environment — Why It Exists

Each project gets its own isolated Python box so packages don't conflict between projects.

| Without venv | With venv |
|---|---|
| All projects share one Python | Each project has its own |
| Package versions conflict | Each project has its own versions |
| Hard to deploy | `pip freeze > requirements.txt` saves exact versions |

### Save your dependencies
```bash
pip freeze > requirements.txt   # save all installed packages

# On a new machine or for teammates:
pip install -r requirements.txt  # recreate exact same environment
```

---

## Django Admin Panel

Visit `http://127.0.0.1:8000/admin` after creating a superuser.

- Free, built-in dashboard — no frontend code needed
- Add, edit, delete any model you register in `admin.py`
- Used in real production projects (news sites, e-commerce, etc.)

---

## URLs — How Django Routes Requests

Two levels of URL routing:

**portfolio/urls.py** (master router — whole project):
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls')),   # hand off to projects app
]
```

**projects/urls.py** (app-level router — you create this file):
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
]
```

---

## Templates — How Django Renders HTML

Templates live in: `projects/templates/projects/project_list.html`

Basic template that loops through projects:
```html
<!DOCTYPE html>
<html>
<body>
    <h1>My Projects</h1>
    {% for project in projects %}
        <h2>{{ project.title }}</h2>
        <p>{{ project.description }}</p>
    {% endfor %}
</body>
</html>
```

| Django Template Syntax | Meaning |
|---|---|
| `{{ variable }}` | display a variable |
| `{% for x in list %}` | loop |
| `{% if condition %}` | conditional |
| `{% url 'name' %}` | generate a URL |
| `{% extends 'base.html' %}` | inherit from base template |
| `{% block content %}` | define a replaceable block |

---

## Django ORM — Talking to the Database

No SQL needed. Django translates Python into SQL for you.

```python
Project.objects.all()              # get all projects
Project.objects.filter(title='X')  # get projects where title = X
Project.objects.get(id=1)          # get one specific project by id
Project.objects.create(title='Y')  # create a new project
project.save()                     # save changes to existing object
project.delete()                   # delete an object
```

---

## Roadmap Summary

| Phase | Topics | Status |
|---|---|---|
| Phase 0 | Python OOP, virtual environments | ✅ Done |
| Phase 1 | URLs, views, templates, models, admin | 🔄 In progress |
| Phase 2 | Forms, user auth, PostgreSQL | ⬜ Next |
| Phase 3 | Build portfolio manager fully | ⬜ Upcoming |
| Phase 4 | REST API, deployment, testing | ⬜ Later |

---

## Resources

| Resource | Link | Cost |
|---|---|---|
| Official Django tutorial | djangoproject.com/start | Free |
| CS50 Web (Harvard) | cs50.harvard.edu/web | Free |
| Corey Schafer Django series | YouTube | Free |
| Real Python | realpython.com | Free + Paid |
| Django for Beginners (book) | William Vincent | Paid |
| Python OOP reference | realpython.com/python3-object-oriented-programming | Free |

---

*Built with Django 6.0.3 · Python 3.13.5 · Windows · VS Code*
