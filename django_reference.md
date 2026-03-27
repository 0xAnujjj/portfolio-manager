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

### GitHub vs Deployment
| Tool | What it does |
|---|---|
| GitHub | Stores your code (hard drive in the cloud) |
| Railway / Render | Runs your code on a real server 24/7 |

### Bound vs Unbound Forms
| State | Meaning |
|---|---|
| Unbound form | Empty form, waiting for user input |
| Bound form | Form has data — user just submitted it |

---

## Project Structure

```
taskkk/                          ← your root project folder
│
├── manage.py                    ← command center, use this for everything
├── db.sqlite3                   ← your database file (auto created)
├── requirements.txt             ← list of installed packages
├── .gitignore                   ← files Git should not upload
├── venv/                        ← virtual environment box (don't touch)
│
├── portfolio/                   ← project settings folder
│   ├── settings.py              ← configuration (installed apps, database, secret key)
│   ├── urls.py                  ← master URL router for the whole project
│   ├── wsgi.py                  ← server entry point (ignore for now)
│   └── asgi.py                  ← async server entry point (ignore for now)
│
├── projects/                    ← your app (one feature = one app)
│   ├── models.py                ← define database tables as Python classes
│   ├── views.py                 ← handle requests, fetch data, return pages
│   ├── urls.py                  ← URL routes for this app (you created this)
│   ├── forms.py                 ← Django forms (you created this)
│   ├── admin.py                 ← register models to manage in admin panel
│   ├── apps.py                  ← app config (rarely touched)
│   ├── tests.py                 ← write tests (ignore for now)
│   ├── migrations/              ← auto-generated DB instructions (don't edit manually)
│   └── templates/
│       └── projects/
│           ├── project_list.html
│           ├── project_detail.html
│           ├── project_form.html        ← used for both create and update
│           └── project_confirm_delete.html
│
└── media/                       ← uploaded images saved here (auto created)
    └── thumbnails/
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
python manage.py startapp name    # create a new app
```

### portfolio/settings.py
The brain of your project. Key things to know:
- `INSTALLED_APPS` — list of all apps Django knows about. Every new app you create must be added here.
- `DATABASES` — database config (SQLite by default, PostgreSQL later)
- `DEBUG = True` — shows detailed errors during development. Set to False in production.
- `SECRET_KEY` — never share this publicly
- `MEDIA_URL` and `MEDIA_ROOT` — where uploaded files are served from and stored

```python
# Add at bottom of settings.py for image uploads
import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### projects/models.py
Where you define your database tables as Python classes.
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
        return self.title   # what shows in admin panel
```
Every time you change this file → run `makemigrations` → run `migrate`.

### projects/views.py
Where you handle requests and return pages. Full CRUD example:
```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm

# READ — list all projects
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

# READ — single project detail
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})

# CREATE — add new project
def project_create(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    return render(request, 'projects/project_form.html', {'form': form})

# UPDATE — edit existing project
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(instance=project)        # prefill form with existing data
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    return render(request, 'projects/project_form.html', {'form': form})

# DELETE — remove a project
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})
```

### projects/forms.py
Django automatically builds a form from your model.
```python
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_link', 'live_link', 'tech_stack', 'thumbnail']
```

### projects/admin.py
Register your models here with extra options.
```python
from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'tech_stack', 'created_at']   # columns in admin list
    search_fields = ['title', 'tech_stack']                 # search bar
```

---

## Common Field Types (models.py)

| Field | Use for |
|---|---|
| `CharField(max_length=200)` | Short text (titles, names) |
| `TextField()` | Long text (descriptions, content) |
| `URLField()` | URLs — validates format automatically |
| `IntegerField()` | Numbers |
| `BooleanField()` | True/False |
| `DateTimeField(auto_now_add=True)` | Timestamp, auto-set on creation |
| `DateTimeField(auto_now=True)` | Timestamp, auto-updates on every save |
| `ImageField(upload_to='folder/')` | Image uploads — requires Pillow |
| `ForeignKey()` | Link to another model (relationship) |

`blank=True` — makes any field optional in forms.

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

# 4. Install Django and Pillow
pip install django pillow

# 5. Create Django project (the dot keeps it in current folder)
django-admin startproject projectname .

# 6. Run the server to verify
python manage.py runserver

# 7. Save dependencies
pip freeze > requirements.txt
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

### Git workflow
```bash
# First time connecting to GitHub
git init
git add .
git commit -m "your message"
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main

# Every time after that
git add .
git commit -m "describe what you changed"
git push
```

---

## .gitignore — What Not to Upload

Create this file in your root folder:
```
venv/           # huge folder, recreated from requirements.txt
db.sqlite3      # local database with test data
__pycache__/    # auto-generated Python files
*.pyc           # compiled Python files
.vscode/        # VS Code personal settings
.env            # secret keys — NEVER upload
media/          # uploaded files (optional, depends on project)
```

---

## Virtual Environment — Why It Exists

Each project gets its own isolated Python box so packages don't conflict between projects.

| Without venv | With venv |
|---|---|
| All projects share one Python | Each project has its own |
| Package versions conflict | Each project has its own versions |
| Hard to deploy | `pip freeze > requirements.txt` saves exact versions |

### Save and restore dependencies
```bash
pip freeze > requirements.txt          # save all installed packages
pip install -r requirements.txt        # restore on new machine
```

---

## Django Admin Panel

Visit `http://127.0.0.1:8000/admin` after creating a superuser.

- Free, built-in dashboard — no frontend code needed
- Add, edit, delete any model you register in `admin.py`
- Used in real production projects (news sites, e-commerce, etc.)
- `list_display` — controls which columns appear in the list view
- `search_fields` — adds a search bar to filter records

---

## URLs — How Django Routes Requests

Two levels of URL routing:

**portfolio/urls.py** (master router — whole project):
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# the + static(...) part serves uploaded images in development
```

**projects/urls.py** (app-level router):
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/update/', views.project_update, name='project_update'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
]
```

**Important:** Put specific paths (`create/`) before dynamic ones (`<int:pk>/`) — Django reads top to bottom and stops at the first match.

`<int:pk>` — captures the number from the URL and passes it to the view as `pk` (primary key).

---

## Templates — How Django Renders HTML

Templates live in: `projects/templates/projects/`

### Template syntax reference
| Django Template Syntax | Meaning |
|---|---|
| `{{ variable }}` | display a variable |
| `{{ project.title }}` | display a field from an object |
| `{% for x in list %}...{% endfor %}` | loop |
| `{% if condition %}...{% endif %}` | conditional |
| `{% url 'name' %}` | generate a URL by name |
| `{% url 'project_detail' project.pk %}` | URL with a parameter |
| `{% csrf_token %}` | security token — required in every form |
| `{% extends 'base.html' %}` | inherit from base template |
| `{% block content %}...{% endblock %}` | define a replaceable block |

### Image display in templates
```html
{% if project.thumbnail %}
    <img src="{{ project.thumbnail.url }}" alt="{{ project.title }}">
{% endif %}
```

### Form template with file upload
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
```
`enctype="multipart/form-data"` is required for image/file uploads.

---

## Django ORM — Talking to the Database

No SQL needed. Django translates Python into SQL for you.

```python
Project.objects.all()                        # get all projects
Project.objects.filter(tech_stack='Django')  # filter by field
Project.objects.get(id=1)                    # get exactly one (crashes if not found)
get_object_or_404(Project, pk=pk)            # get one or show 404 page (safer)
Project.objects.create(title='Y')            # create and save instantly
project.save()                               # save changes to existing object
project.delete()                             # delete an object
```

---

## Forms — Key Concepts

### ModelForm
Automatically generates form fields from a model:
```python
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', ...]  # which fields to include
```

### instance= parameter (for edit/update)
```python
form = ProjectForm(instance=project)  # prefills form with existing data
```

### request.FILES
Required when your form handles file/image uploads:
```python
form = ProjectForm(request.POST, request.FILES)
```

### View pattern for create/update
```python
form = ProjectForm()                          # empty form by default
if request.method == 'POST':                  # form was submitted
    form = ProjectForm(request.POST, request.FILES)
    if form.is_valid():                       # passes validation
        form.save()                           # save to database
        return redirect('project_list')       # go back to list
return render(request, 'template.html', {'form': form})
```

---

## CRUD Summary

| Operation | View function | URL pattern | Template |
|---|---|---|---|
| List all | `project_list` | `/` | `project_list.html` |
| View one | `project_detail` | `/<int:pk>/` | `project_detail.html` |
| Create | `project_create` | `/create/` | `project_form.html` |
| Update | `project_update` | `/<int:pk>/update/` | `project_form.html` |
| Delete | `project_delete` | `/<int:pk>/delete/` | `project_confirm_delete.html` |

---

## Error Messages — How to Read Them

| Error | What it means | Fix |
|---|---|---|
| `TemplateDoesNotExist` | Wrong template path in view | Check spelling, `projects` not `project` |
| `Page not found (404)` | URL doesn't match any pattern | Check `urls.py` order and spelling |
| `no such table` | Migration not applied | Run `makemigrations` then `migrate` |
| `Pylance reportPossiblyUnbound` | VS Code warning, not a real error | Define variable before the if block |

---

## How to Use Docs

- Docs are a **dictionary, not a novel** — look things up when you need them
- The trigger is always a problem you're trying to solve
- Read the code example first, explanation second
- Type examples yourself — don't copy paste
- Break things on purpose to understand them deeper

---

## Roadmap Summary

| Phase | Topics | Status |
|---|---|---|
| Phase 0 | Python OOP, virtual environments | ✅ Done |
| Phase 1 | URLs, views, templates, models, admin | ✅ Done |
| Phase 2 | Forms, user auth, PostgreSQL | 🔄 In progress |
| Phase 3 | Bootstrap UI, base template | ⬜ Next |
| Phase 4 | Deployment to Railway, REST API | ⬜ Later |

### What's built so far
- ✅ Django project and app set up
- ✅ Project model with title, description, github link, live link, tech stack, thumbnail
- ✅ Admin panel with search and list display
- ✅ Image uploads working
- ✅ Project list page
- ✅ Project detail page
- ✅ Create project form
- ✅ Edit project form
- ✅ Delete project with confirmation
- ✅ Pushed to GitHub — portfolio-manager repo
- ⬜ User authentication (login, register, logout)
- ⬜ Restrict edit/delete to logged in users only
- ⬜ Bootstrap UI with base template
- ⬜ Deploy to Railway

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
| Bootstrap docs | getbootstrap.com/docs | Free |
| Railway (deployment) | railway.app | Free tier |

---

*Built with Django 6.0.3 · Python 3.13.5 · Pillow 12.1.1 · Windows · VS Code*
