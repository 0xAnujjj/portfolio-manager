# Django Complete Learning Reference
> Built while learning Django from scratch — Phase 0 to Deployment
> Project: Student Portfolio Manager
> Stack: Django 6.0.3 · Python 3.13.5 · PostgreSQL · Bootstrap 5 · Railway

---

## Table of Contents
1. [Mental Models](#mental-models)
2. [Phase 0 — Python OOP](#phase-0--python-oop)
3. [Phase 1 — Django Fundamentals](#phase-1--django-fundamentals)
4. [Phase 2 — Forms and Authentication](#phase-2--forms-and-authentication)
5. [Phase 3 — Bootstrap UI](#phase-3--bootstrap-ui)
6. [Phase 4 — Deployment](#phase-4--deployment)
7. [Project Structure](#project-structure)
8. [All Key Files Explained](#all-key-files-explained)
9. [Commands Cheat Sheet](#commands-cheat-sheet)
10. [Django ORM Reference](#django-orm-reference)
11. [Template Syntax Reference](#template-syntax-reference)
12. [Error Messages Guide](#error-messages-guide)
13. [Roadmap and Progress](#roadmap-and-progress)
14. [Resources](#resources)

---

## Mental Models

### Data Science Python vs Django Python
You came from a data science background. Here's how to think about the shift:

| Data Science Python | Django (Web Backend) Python |
|---|---|
| Python as a calculator | Python as a waiter in a restaurant |
| You feed it data, it outputs results | It listens for requests, talks to a database, sends back responses |
| Scripts run once and finish | Server runs forever, waiting for requests |
| You call the code | The browser calls the code |

### The Django Request Cycle
This is the most important mental model in Django. Every single webpage follows this cycle:

```
Browser sends Request
        ↓
URLs (urls.py) — which view handles this?
        ↓
View (views.py) — fetch data, process logic
        ↓
Model (models.py) — talk to the database
        ↓
Template (.html) — fill data into HTML
        ↓
Response sent back to browser
```

Every page you ever build in Django follows this exact cycle. Always.

### Project vs App
Django has two levels:
- **Project** — the whole website (your `portfolio` folder with `settings.py`)
- **App** — one feature/module inside the project (your `projects` app)

Think of it like a restaurant:
- Project = the whole restaurant
- Apps = departments (kitchen, billing, front desk)

One project can have many apps. Each app handles one specific feature.

### GitHub vs Deployment
| Tool | What it does |
|---|---|
| GitHub | Stores your code — hard drive in the cloud |
| Railway / Render | Runs your code on a real server 24/7 |

Railway watches your GitHub repo. When you push code → Railway automatically pulls and redeploys.

---

## Phase 0 — Python OOP

### Why OOP matters for Django
Django is built entirely on classes. Every database table is a class, every form is a class, every view can be a class. Without understanding OOP, Django code looks like magic.

### Classes — The Blueprint Concept
A class is a blueprint. An object is what you build from that blueprint.

```python
class Project:
    def __init__(self, title, description):
        self.title = title
        self.description = description
```

- `class Project` — defines the blueprint
- `__init__` — runs automatically the moment you create a new object. It's the "setup crew"
- `self` — refers to the specific object being created. Like `this` in C++

Creating an object from the blueprint:
```python
my_project = Project("Django Blog", "A blog app built with Django")
print(my_project.title)        # Django Blog
print(my_project.description)  # A blog app built with Django
```

### C++ to Python Translation
You already knew OOP from C++. Here's the direct translation:

| C++ | Python |
|---|---|
| `class Student { };` | `class Student:` |
| Constructor `Student()` | `__init__(self)` |
| `this->name` | `self.name` |
| `public:` / `private:` | everything public by default, `_name` convention for private |
| `void introduce()` | `def introduce(self):` |
| `class Dog : public Animal` | `class Dog(Animal):` |
| Semicolons and curly braces | Indentation only |

### Methods
A method is a function that belongs to a class:

```python
class Student:
    def __init__(self, name, university):
        self.name = name
        self.university = university

    def introduce(self):
        print(f"Hi, I'm {self.name} from {self.university}")

my_student = Student("Anuj", "Tribhuvan")
my_student.introduce()   # Hi, I'm Anuj from Tribhuvan
```

### Inheritance
One class can extend another, inheriting all its features:

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("Some sound")

class Dog(Animal):       # Dog inherits from Animal
    def speak(self):     # overrides the parent method
        print("Woof!")

my_dog = Dog("Rex")
my_dog.speak()   # Woof!
```

### How Django Uses Inheritance
In Django, you always inherit from Django's built-in classes:

```python
# Your Project model inherits from Django's Model class
class Project(models.Model):
    title = models.CharField(max_length=200)

# Your form inherits from Django's ModelForm class
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
```

Django's parent classes do all the heavy lifting. You just extend them with your specific needs.

---

## Phase 1 — Django Fundamentals

### Virtual Environments
Before any Django project, always create a virtual environment. It's an isolated Python box for each project.

**Why it exists:**
| Without venv | With venv |
|---|---|
| All projects share one Python installation | Each project has its own isolated Python |
| Installing a package for one project affects all others | Packages are isolated per project |
| Version conflicts break things | Each project has its own versions |
| Hard to deploy reliably | `requirements.txt` captures exact versions |

**The 3-command ritual for every new project:**
```bash
python -m venv venv          # create the box
venv\Scripts\activate        # activate it (Windows)
pip install django pillow    # install packages inside the box
```

VS Code auto-activates venv in new terminals once set up.

### Starting a Django Project
```bash
django-admin startproject portfolio .
```
The `.` at the end means "create in current folder" — without it Django creates an extra nested folder.

### Running the Development Server
```bash
python manage.py runserver
```
Then visit `http://127.0.0.1:8000` in your browser. The rocket page means it's working.

### Creating an App
```bash
python manage.py startapp projects
```
Then register it in `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'projects',   # add your app here
]
```

### Models — Database Tables as Classes
`models.py` is where you define your database structure. Each class = one database table. Each attribute = one column.

```python
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    tech_stack = models.CharField(max_length=200, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

**Field types:**
| Field | Use for |
|---|---|
| `CharField(max_length=N)` | Short text — titles, names |
| `TextField()` | Long text — descriptions, content |
| `URLField()` | URLs — validates format automatically |
| `IntegerField()` | Whole numbers |
| `BooleanField()` | True/False |
| `DateTimeField(auto_now_add=True)` | Timestamp, auto-set when object is created |
| `DateTimeField(auto_now=True)` | Timestamp, updates every time object is saved |
| `ImageField(upload_to='folder/')` | Image file uploads — requires Pillow package |
| `ForeignKey(Model, on_delete=CASCADE)` | Link to another model (relationship) |

`blank=True` — makes the field optional in forms.

### Migrations — Applying Model Changes to Database
Every time you change `models.py`, you must run these two commands:

```bash
python manage.py makemigrations   # creates instructions (the recipe)
python manage.py migrate          # applies them to database (the cooking)
```

- `makemigrations` — Django reads your models and creates a migration file describing what changed
- `migrate` — Django executes those migration files on the actual database

Think of migrations as a version history of your database structure.

### Admin Panel
Django gives you a free admin dashboard at `/admin`. Register your models to manage them there:

```python
# projects/admin.py
from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'tech_stack', 'created_at']   # columns shown in list
    search_fields = ['title', 'tech_stack']                 # adds search bar
```

Create a superuser to log in:
```bash
python manage.py createsuperuser
```

Then visit `http://127.0.0.1:8000/admin`

### Views — Handling Requests
Views are functions that receive a request and return a response. This is where your logic lives.

```python
# projects/views.py
from django.shortcuts import render, get_object_or_404
from .models import Project

def project_list(request):
    projects = Project.objects.all()    # fetch all from database
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)   # fetch one or show 404
    return render(request, 'projects/project_detail.html', {'project': project})
```

- `request` — contains everything about the incoming browser request
- `Project.objects.all()` — Django ORM fetching all projects (like pandas but for databases)
- `render()` — takes data and fills it into an HTML template
- `get_object_or_404()` — safer than `.get()` — shows a clean 404 page if not found instead of crashing
- `{'projects': projects}` — passes data to the template under the key name `projects`

### URLs — Routing Requests to Views
Two levels of URL routing:

**`portfolio/urls.py`** — master router for the whole project:
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # built-in auth
    path('', include('projects.urls')),                      # your app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(...) serves uploaded images during development
```

**`projects/urls.py`** — app-level router (you create this file):
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/update/', views.project_update, name='project_update'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('register/', views.project_register, name='project_register'),
]
```

**Important URL rules:**
- Put specific paths (`create/`) BEFORE dynamic ones (`<int:pk>/`) — Django reads top to bottom and stops at the first match
- `<int:pk>` captures a number from the URL and passes it to the view as `pk`
- `name=` lets you reference URLs in templates with `{% url 'name' %}` instead of hardcoding paths

### Templates — Displaying Data as HTML
Templates live in `projects/templates/projects/`. Django looks for templates in this specific structure.

Basic template:
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

**Template syntax:**
| Syntax | Meaning |
|---|---|
| `{{ variable }}` | Display a variable |
| `{{ project.title }}` | Display a field from an object |
| `{{ description\|truncatewords:20 }}` | Template filter — cut to 20 words |
| `{% for x in list %}...{% endfor %}` | Loop |
| `{% if condition %}...{% endif %}` | Conditional |
| `{% url 'name' %}` | Generate a URL by its name |
| `{% url 'project_detail' project.pk %}` | URL with a parameter |
| `{% csrf_token %}` | Security token — required in every POST form |
| `{% extends 'base.html' %}` | Inherit from a base template |
| `{% block content %}...{% endblock %}` | Define a replaceable section |

### Image Handling
To serve uploaded images, add to `settings.py`:
```python
import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Display in templates:
```html
{% if project.thumbnail %}
    <img src="{{ project.thumbnail.url }}" alt="{{ project.title }}">
{% endif %}
```

Requires `Pillow` package: `pip install pillow`

---

## Phase 2 — Forms and Authentication

### Django Forms — ModelForm
`ModelForm` automatically generates a form from your model. No need to write each field manually.

```python
# projects/forms.py
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_link', 'live_link', 'tech_stack', 'thumbnail']
```

The `Meta` class (a class inside a class) tells Django which model and which fields to use.

### Bound vs Unbound Forms
| State | Meaning |
|---|---|
| Unbound form | Empty form — user hasn't submitted anything yet |
| Bound form | Form has data — user just submitted it |

### Full CRUD Views Pattern
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm

# READ — list all
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

# READ — single item
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})

# CREATE
@login_required
def project_create(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    return render(request, 'projects/project_form.html', {'form': form})

# UPDATE
@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(instance=project)         # prefill with existing data
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    return render(request, 'projects/project_form.html', {'form': form})

# DELETE
@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})
```

**Key concepts:**
- `request.method == 'POST'` — checks if the form was submitted or just opened
- `request.FILES` — required when form handles file/image uploads
- `form.is_valid()` — runs all validation rules
- `instance=project` — prefills the form with existing data for editing
- `redirect()` — sends user to a different page after saving
- `@login_required` — decorator that blocks access unless user is logged in

### Form Template
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
```
`enctype="multipart/form-data"` is required for file/image uploads — without it images won't upload.

### CRUD Summary Table
| Operation | View function | URL pattern | Template |
|---|---|---|---|
| List all | `project_list` | `/` | `project_list.html` |
| View one | `project_detail` | `/<int:pk>/` | `project_detail.html` |
| Create | `project_create` | `/create/` | `project_form.html` |
| Update | `project_update` | `/<int:pk>/update/` | `project_form.html` |
| Delete | `project_delete` | `/<int:pk>/delete/` | `project_confirm_delete.html` |

### User Authentication
Django has a complete auth system built in. Just include its URLs:

```python
# portfolio/urls.py
path('accounts/', include('django.contrib.auth.urls')),
```

This gives you these free URLs:
| URL | What it does |
|---|---|
| `/accounts/login/` | Login page |
| `/accounts/logout/` | Logout (requires POST request) |
| `/accounts/password-change/` | Change password |

Add to `settings.py`:
```python
LOGIN_REDIRECT_URL = '/'        # where to go after login
LOGOUT_REDIRECT_URL = '/'       # where to go after logout
LOGIN_URL = '/accounts/login/'  # where to redirect if not logged in
```

### Login Template
Django expects the login template at `registration/login.html`:
```html
{% extends 'base.html' %}
{% block content %}
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
</form>
{% endblock %}
```

### Logout Button
In newer Django versions, logout requires a POST request (security reason):
```html
<form method="post" action="{% url 'logout' %}">
    {% csrf_token %}
    <button type="submit">Logout</button>
</form>
```

### login_required Decorator
Protects views from unauthenticated access:
```python
from django.contrib.auth.decorators import login_required

@login_required
def project_create(request):
    ...
```

If user is not logged in, they're automatically redirected to the login page.

### User Registration
Django has a built-in `UserCreationForm`:
```python
from django.contrib.auth.forms import UserCreationForm

def project_register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'registration/register.html', {'form': form})
```

### Checking Auth State in Templates
```html
{% if user.is_authenticated %}
    <a href="/create/">Add Project</a>
    <form method="post" action="{% url 'logout' %}">
        {% csrf_token %}
        <button type="submit">Logout</button>
    </form>
{% else %}
    <a href="{% url 'login' %}">Login</a>
    <a href="{% url 'project_register' %}">Register</a>
{% endif %}
```

---

## Phase 3 — Bootstrap UI

### Base Template — Write Once, Use Everywhere
Instead of copying navbar and Bootstrap link to every template, write it once in `base.html` and all other templates inherit from it.

`projects/templates/base.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
    <a class="navbar-brand" href="/">My Portfolio</a>
    <div class="ms-auto">
        {% if user.is_authenticated %}
            <a href="/create/" class="btn btn-outline-light btn-sm me-2">+ Add Project</a>
            <form method="post" action="{% url 'logout' %}" class="d-inline">
                {% csrf_token %}
                <button type="submit" class="btn btn-outline-danger btn-sm">Logout</button>
            </form>
        {% else %}
            <a href="{% url 'login' %}" class="btn btn-outline-light btn-sm me-2">Login</a>
            <a href="{% url 'project_register' %}" class="btn btn-outline-success btn-sm">Register</a>
        {% endif %}
    </div>
</nav>

<div class="container mt-4">
    {% block content %}
    {% endblock %}
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Template Inheritance Pattern
Every other template extends base.html:
```html
{% extends 'base.html' %}

{% block content %}
    <!-- your page content here -->
{% endblock %}
```

The `{% block content %}` in base.html is a placeholder. Each child template fills it in.

### Useful Bootstrap Classes
| Class | What it does |
|---|---|
| `container` | Centers content with padding |
| `row` | Creates a row for columns |
| `col-md-4` | Column takes 4/12 of width on medium screens |
| `card` | Styled box/card component |
| `card-body` | Padding inside a card |
| `btn btn-primary` | Blue button |
| `btn btn-danger` | Red button |
| `btn btn-success` | Green button |
| `btn btn-outline-secondary` | Outlined gray button |
| `badge bg-secondary` | Small gray label/tag |
| `text-muted` | Gray text |
| `shadow-sm` | Subtle shadow on a card |
| `img-fluid` | Makes image responsive |
| `d-flex` | Flexbox container |
| `justify-content-between` | Space between flex items |
| `ms-auto` | Push element to the right |
| `mb-4` | Margin bottom 4 units |
| `mt-4` | Margin top 4 units |
| `me-2` | Margin right 2 units |

---

## Phase 4 — Deployment

### Preparing Django for Production

**Install required packages:**
```bash
pip install gunicorn whitenoise python-decouple dj-database-url psycopg2-binary
pip freeze > requirements.txt
```

| Package | Purpose |
|---|---|
| `gunicorn` | Production web server (replaces `runserver`) |
| `whitenoise` | Serves static files (CSS/JS) in production |
| `python-decouple` | Manages secret keys via `.env` file |
| `dj-database-url` | Parses database URLs (for PostgreSQL) |
| `psycopg2-binary` | PostgreSQL adapter for Python |

**Create `.env` file** (never commit this to GitHub):
```
SECRET_KEY=your-actual-secret-key
DEBUG=True
```

**Update `settings.py`:**
```python
from decouple import config
import dj_database_url
import os

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = ['your-app.up.railway.app', 'localhost', '127.0.0.1']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # add after SecurityMiddleware
    ...
]

# At the bottom
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

CSRF_TRUSTED_ORIGINS = ['https://your-app.up.railway.app']

# Database (uses PostgreSQL in production, SQLite locally)
DATABASE_URL = config('DATABASE_URL', default='')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config(default=DATABASE_URL)
```

**Create `Procfile`** (no extension) in root folder:
```
web: gunicorn portfolio.wsgi
```

**Collect static files:**
```bash
python manage.py collectstatic
```

### Deploying to Railway

1. Go to railway.app → sign in with GitHub
2. Click `New Project` → `Deploy from GitHub repo`
3. Select your `portfolio-manager` repo
4. Click `+ New` → `Database` → `PostgreSQL`
5. In your app → `Variables` tab → add:
   - `SECRET_KEY` = your secret key
   - `DEBUG` = False
   - `DATABASE_URL` = copy from PostgreSQL service
6. In `Settings` → `Deploy` → `Start Command`:
   ```
   python manage.py migrate && gunicorn portfolio.wsgi
   ```
7. In `Settings` → `Networking` → `Generate Domain`

### Railway Workflow After Setup
Every time you push to GitHub, Railway auto-redeploys:
```bash
git add .
git commit -m "your change description"
git push
```

### Common Deployment Errors
| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'decouple'` | Package not in requirements.txt | Run `pip freeze > requirements.txt` and push |
| `WhitenoiseMiddleware not found` | Wrong capitalization | Use `WhiteNoiseMiddleware` (capital N) |
| `CSRF verification failed` | Domain not trusted | Add to `CSRF_TRUSTED_ORIGINS` in settings |
| `DisallowedHost` | Domain not in ALLOWED_HOSTS | Add Railway URL to `ALLOWED_HOSTS` |
| App crashes after going Online | Migrations not run | Add `python manage.py migrate &&` to start command |

---

## Project Structure

```
taskkk/                              ← root project folder
│
├── manage.py                        ← command center
├── db.sqlite3                       ← local SQLite database
├── requirements.txt                 ← all installed packages
├── Procfile                         ← tells Railway how to start app
├── .env                             ← secret keys (never commit)
├── .gitignore                       ← what Git should ignore
├── venv/                            ← virtual environment (don't touch)
│
├── portfolio/                       ← Django project settings folder
│   ├── settings.py                  ← all configuration
│   ├── urls.py                      ← master URL router
│   ├── wsgi.py                      ← production server entry point
│   └── asgi.py                      ← async server entry point
│
├── projects/                        ← your Django app
│   ├── models.py                    ← database table definitions
│   ├── views.py                     ← request handlers
│   ├── urls.py                      ← app URL routes (you created this)
│   ├── forms.py                     ← Django forms (you created this)
│   ├── admin.py                     ← admin panel configuration
│   ├── apps.py                      ← app config (rarely touched)
│   ├── tests.py                     ← automated tests (future)
│   ├── migrations/                  ← auto-generated DB instructions
│   └── templates/
│       ├── base.html                ← master layout template
│       ├── registration/
│       │   ├── login.html
│       │   └── register.html
│       └── projects/
│           ├── project_list.html
│           ├── project_detail.html
│           ├── project_form.html
│           └── project_confirm_delete.html
│
├── media/                           ← uploaded images (auto created)
│   └── thumbnails/
│
└── staticfiles/                     ← collected static files for production
```

---

## All Key Files Explained

### manage.py
Your command center. Never edit this — just run commands with it.

### portfolio/settings.py
The brain of the project. Key sections:
- `SECRET_KEY` — cryptographic key, never share publicly
- `DEBUG` — True locally, False in production
- `ALLOWED_HOSTS` — which domains can access the site
- `INSTALLED_APPS` — every app must be registered here
- `MIDDLEWARE` — list of processing layers every request passes through
- `DATABASES` — database configuration
- `STATIC_URL` / `STATIC_ROOT` — where CSS/JS files live
- `MEDIA_URL` / `MEDIA_ROOT` — where uploaded files live

### projects/models.py
Database table definitions as Python classes. Change this → always run makemigrations + migrate.

### projects/views.py
Request handlers. Each function receives a request, does something, returns a response.

### projects/urls.py
Maps URL patterns to view functions. You created this file — Django doesn't generate it.

### projects/forms.py
Form definitions. `ModelForm` auto-generates forms from models. You created this file.

### projects/admin.py
Registers models in the admin dashboard with display options.

### Procfile
Tells Railway (and other platforms) how to start your app:
```
web: gunicorn portfolio.wsgi
```

### requirements.txt
Lists all Python packages your project needs. Generated with `pip freeze > requirements.txt`. Anyone can recreate your exact environment with `pip install -r requirements.txt`.

### .gitignore
Tells Git what not to track:
```
venv/           # huge, recreated from requirements.txt
db.sqlite3      # local test data
__pycache__/    # auto-generated
*.pyc           # compiled Python
.vscode/        # editor settings
.env            # secret keys — NEVER commit
media/          # uploaded files
```

---

## Commands Cheat Sheet

### New Project from Scratch
```bash
mkdir myproject && cd myproject
python -m venv venv
venv\Scripts\activate
pip install django pillow
django-admin startproject projectname .
python manage.py runserver
pip freeze > requirements.txt
```

### Resume Existing Project
```bash
cd d:/PROJECTS/taskkk
venv\Scripts\activate
python manage.py runserver
```

### Database
```bash
python manage.py makemigrations   # create migration files from model changes
python manage.py migrate          # apply migrations to database
python manage.py createsuperuser  # create admin account
```

### Apps
```bash
python manage.py startapp appname
# Then add 'appname' to INSTALLED_APPS in settings.py
```

### Static Files (for deployment)
```bash
python manage.py collectstatic
```

### Git Workflow
```bash
# First time
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main

# Every time after
git add .
git commit -m "describe your change"
git push
```

### Save/Restore Dependencies
```bash
pip freeze > requirements.txt          # save
pip install -r requirements.txt        # restore on new machine
```

---

## Django ORM Reference

The ORM (Object Relational Mapper) lets you talk to the database using Python instead of SQL.

```python
# Fetch all records
Project.objects.all()

# Filter records
Project.objects.filter(tech_stack='Django')
Project.objects.filter(title__contains='blog')   # contains search
Project.objects.filter(created_at__year=2026)    # filter by year

# Get one record
Project.objects.get(id=1)                        # crashes if not found
get_object_or_404(Project, pk=pk)                # shows 404 if not found (safer)

# Create
Project.objects.create(title='My Project', description='...')

# Update
project = Project.objects.get(id=1)
project.title = 'New Title'
project.save()

# Delete
project.delete()

# Count
Project.objects.count()

# Order
Project.objects.all().order_by('-created_at')    # newest first
Project.objects.all().order_by('title')          # alphabetical
```

---

## Template Syntax Reference

```html
<!-- Variables -->
{{ variable }}
{{ project.title }}
{{ project.description|truncatewords:20 }}
{{ project.created_at|date:"M d, Y" }}

<!-- Loops -->
{% for project in projects %}
    {{ project.title }}
{% empty %}
    No projects yet.
{% endfor %}

<!-- Conditionals -->
{% if user.is_authenticated %}
    Logged in
{% elif condition %}
    Something else
{% else %}
    Not logged in
{% endif %}

<!-- URLs -->
{% url 'project_list' %}
{% url 'project_detail' project.pk %}

<!-- Template inheritance -->
{% extends 'base.html' %}
{% block content %}
    Page content here
{% endblock %}

<!-- Include another template -->
{% include 'partials/navbar.html' %}

<!-- CSRF token — required in every POST form -->
{% csrf_token %}

<!-- Static files -->
{% load static %}
<img src="{% static 'images/logo.png' %}">
```

---

## Error Messages Guide

| Error | What it means | How to fix |
|---|---|---|
| `TemplateDoesNotExist` | Wrong template path | Check spelling — `projects` not `project` |
| `Page not found (404)` | URL doesn't match any pattern | Check `urls.py` order and spelling |
| `no such table` | Migration not applied | Run `makemigrations` then `migrate` |
| `Method Not Allowed (405)` | Wrong HTTP method | Use POST form for logout, not a link |
| `CSRF verification failed` | Missing token or untrusted origin | Add `{% csrf_token %}` or update `CSRF_TRUSTED_ORIGINS` |
| `ModuleNotFoundError` | Package not installed | `pip install packagename` |
| `ImproperlyConfigured` | Settings misconfiguration | Check `settings.py` for typos |
| `Pylance warnings` | VS Code type checker — not real errors | Usually safe to ignore or minor fix |
| `DisallowedHost` | Domain not in ALLOWED_HOSTS | Add domain to `ALLOWED_HOSTS` in settings |
| `WhitenoiseMiddleware not found` | Wrong capitalization | Use `WhiteNoiseMiddleware` with capital N |

### How to Read Error Messages
1. **Read the last line first** — that's usually the actual error
2. **Look for your file names** in the traceback — that's where your code caused it
3. **Google the exact error message** — someone has had the same problem
4. **Check spelling** — most errors are typos (`projects` vs `project`, capital letters)

---

## Roadmap and Progress

| Phase | Topics | Status |
|---|---|---|
| Phase 0 | Python OOP, virtual environments | ✅ Complete |
| Phase 1 | Models, views, URLs, templates, admin | ✅ Complete |
| Phase 2 | Forms, CRUD, authentication, login/register | ✅ Complete |
| Phase 3 | Bootstrap UI, base template, template inheritance | ✅ Complete |
| Phase 4 | Production deployment to Railway, PostgreSQL | ✅ Complete |

### Everything Built So Far
- ✅ Django project set up with virtual environment
- ✅ Project model with title, description, github link, live link, tech stack, thumbnail, timestamp
- ✅ Database migrations
- ✅ Admin panel with search and column display
- ✅ Image uploads with Pillow
- ✅ Project list page
- ✅ Project detail page
- ✅ Create project form
- ✅ Edit project form (prefilled)
- ✅ Delete project with confirmation page
- ✅ User login and logout
- ✅ User registration
- ✅ Login required for create/edit/delete
- ✅ Bootstrap UI with navbar
- ✅ Base template with inheritance
- ✅ Pushed to GitHub — portfolio-manager repo
- ✅ PostgreSQL database on Railway
- ✅ Live deployment at portfolio-manager-production-fe20.up.railway.app

### What's Next (optional improvements)
- ⬜ Improve UI to match Figma design
- ⬜ Add search and filter by tech stack
- ⬜ Link projects to specific users (ForeignKey)
- ⬜ Add a contact form
- ⬜ Resume/CV upload
- ⬜ REST API with Django REST Framework
- ⬜ Automated tests

---

## How to Use Django Docs

Docs are a **dictionary, not a novel.** Nobody reads them front to back.

- Go there when you have a **specific question**, not to study
- The trigger is always a **problem you're trying to solve**
- **Read the code example first**, explanation second
- **Type examples yourself** — don't copy paste
- **Break things on purpose** to understand them deeper

**Useful Django docs pages to bookmark:**
| Page | When to use it |
|---|---|
| Model field reference | When you need a field type you haven't used |
| QuerySet API | When your database query isn't returning what you expect |
| Forms reference | When you need custom form validation |
| URL dispatcher | When your URLs aren't routing correctly |
| Template language | When a template tag isn't working |
| Authentication | When building login/permission features |

---

## Resources

| Resource | URL | Cost | Best for |
|---|---|---|---|
| Official Django docs | djangoproject.com/start | Free | Reference when stuck |
| CS50 Web (Harvard) | cs50.harvard.edu/web | Free | Video + project based |
| Corey Schafer Django series | YouTube | Free | Code-along style |
| Real Python | realpython.com | Free + Paid | Detailed articles |
| Django for Beginners (book) | William Vincent | Paid | Project-based learning |
| Python OOP | realpython.com/python3-object-oriented-programming | Free | OOP reference |
| Bootstrap docs | getbootstrap.com/docs | Free | UI components |
| Railway | railway.app | Free tier | Deployment |
| Neon (PostgreSQL) | neon.tech | Free forever | Alternative database |

---

## Live Project
- **GitHub:** github.com/YOUR_USERNAME/portfolio-manager
- **Live site:** portfolio-manager-production-fe20.up.railway.app
- **Local:** http://127.0.0.1:8000
- **Admin:** http://127.0.0.1:8000/admin (local) or live-url/admin

---

*Built with Django 6.0.3 · Python 3.13.5 · Pillow 12.1.1 · PostgreSQL · Bootstrap 5.3 · Railway · Windows · VS Code*
