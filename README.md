# 📷 PhotoVault — Photo Album Management System

A production-ready **Photo Album Management** web application built with Django, Cloudinary, and PostgreSQL. Deployed on **Render**.

---

## 🌐 Live Application

**Live URL:** `https://github.com/Wylton15/Production-Ready-Django-Photo-Album-Management-System`

---

## 🗂️ Repository

**GitHub:** `https://github.com/your-username/cloud-render`
_(Replace with your actual repository URL)_

---

## 📋 Project Overview

PhotoVault is a full-featured, production-grade Photo Album Management System that allows users to organize photos into albums, upload images to Cloudinary, and enforces role-based access so that only administrators can manage albums while regular users manage their own photos.

---

## ✅ Features

### Core Functionality

- **Photo Gallery** — Browse all uploaded photos in a responsive dark-mode grid
- **Album Management** — Group photos into named, described albums with cover images
- **Photo Upload** — Upload images directly to Cloudinary cloud storage
- **Search** — Filter photos and albums by title or description
- **Pagination** — Efficient browsing of large photo/album collections

### Architecture

| Requirement                   | Implementation                                                                    |
| ----------------------------- | --------------------------------------------------------------------------------- |
| **Class-Based Views**         | `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView` for all CRUD   |
| **Role-Based Access Control** | 3-tier RBAC via Django auth + custom mixins                                       |
| **Cloudinary Storage**        | `CloudinaryField` + `MediaCloudinaryStorage` — no local media files in production |
| **PostgreSQL**                | `dj-database-url` parses `DATABASE_URL`; SQLite fallback for local dev            |
| **Deployed on Render**        | `build.sh` automates install, migrate, collectstatic, and superuser creation      |

---

## 🔐 Role-Based Access Control (RBAC)

| Role                   | Permissions                                    |
| ---------------------- | ---------------------------------------------- |
| **Anonymous**          | View gallery, browse albums, view album photos |
| **Authenticated User** | + Upload photos, edit/delete their own photos  |
| **Staff / Admin**      | + Create/Edit/Delete albums, manage all photos |

**Mixins used:**

- `AdminRequiredMixin(UserPassesTestMixin)` — checks `is_staff or is_superuser`
- `LoginRequiredMixin` — redirects unauthenticated users to `/login/`
- `UserPassesTestMixin` — enforces ownership on photo edit/delete

---

## 🏗️ Project Structure

```
cloud-render/
├── recipe_project/          # Django project configuration
│   ├── settings.py          # Environment-driven settings
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py
├── gallery/                 # Core application
│   ├── models.py            # Album + RecipePhoto models
│   ├── views.py             # All CBVs + RBAC mixins
│   ├── forms.py             # AlbumForm, RecipePhotoForm, RegisterForm
│   ├── admin.py             # Django admin configuration
│   ├── urls.py              # App URL patterns
│   ├── migrations/          # Database migrations
│   └── templates/
│       ├── gallery/
│       │   ├── base.html              ← Master layout (dark-mode)
│       │   ├── home.html              ← Photo wall
│       │   ├── album_list.html        ← Albums listing
│       │   ├── album_detail.html      ← Photos within an album
│       │   ├── album_form.html        ← Create/Edit album
│       │   ├── album_confirm_delete.html
│       │   ├── photo_form.html        ← Upload/Edit photo
│       │   └── delete.html            ← Delete photo confirmation
│       └── registration/
│           ├── login.html
│           └── register.html
├── build.sh                 # Render build script
├── requirements.txt         # Python dependencies
├── manage.py
└── .gitignore
```

---

## ⚙️ Tech Stack

| Layer                 | Technology          |
| --------------------- | ------------------- |
| Framework             | Django 6.0.5        |
| Language              | Python 3.14         |
| Database (Production) | PostgreSQL (Render) |
| Database (Local Dev)  | SQLite              |
| Media Storage         | Cloudinary          |
| Static Files          | WhiteNoise          |
| WSGI Server           | Gunicorn            |
| Deployment            | Render              |

---

## 🚀 Deployment (Render)

### Step 1 — Push to GitHub

```bash
git add .
git commit -m "feat: production-ready photo album management system"
git push origin main
```

### Step 2 — Create Render Web Service

1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn recipe_project.wsgi:application`

### Step 3 — Add Environment Variables in Render Dashboard

| Variable                    | Description                                       |
| --------------------------- | ------------------------------------------------- |
| `SECRET_KEY`                | Django secret key (generate a new secure one)     |
| `DEBUG`                     | `False`                                           |
| `DATABASE_URL`              | Internal URL from your Render PostgreSQL instance |
| `CLOUDINARY_CLOUD_NAME`     | Your Cloudinary cloud name                        |
| `CLOUDINARY_API_KEY`        | Your Cloudinary API key                           |
| `CLOUDINARY_API_SECRET`     | Your Cloudinary API secret                        |
| `DJANGO_SUPERUSER_USERNAME` | Initial admin username                            |
| `DJANGO_SUPERUSER_EMAIL`    | Initial admin email                               |
| `DJANGO_SUPERUSER_PASSWORD` | Initial admin password (use a strong one!)        |
| `RENDER_EXTERNAL_HOSTNAME`  | `your-app-name.onrender.com`                      |

### Step 4 — Add PostgreSQL

1. Render → **New → PostgreSQL**
2. Copy the **Internal Database URL** → paste as `DATABASE_URL`

> **The `build.sh` script automatically:**
>
> - Installs all dependencies
> - Collects static files
> - Runs database migrations
> - Creates the initial superuser

---

## 💻 Local Development

### Prerequisites

- Python 3.x
- Git

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-username/cloud-render.git
cd cloud-render

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up local environment
# Create a .env file (copy from .env.example or configure manually)
# DATABASE_URL should be commented out to use SQLite locally

# 4. Apply migrations
python manage.py migrate

# 5. Create a local admin account
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## 🔑 Default Admin Credentials (Local)

| Field     | Value                        |
| --------- | ---------------------------- |
| Username  | `admin`                      |
| Password  | Set during `createsuperuser` |
| Admin URL | http://127.0.0.1:8000/admin/ |

> ⚠️ **Never use weak passwords in production.** Always set `DJANGO_SUPERUSER_PASSWORD` to a strong value in Render environment variables.

---

## 📡 API / URL Reference

| URL                    | View                      | Access          |
| ---------------------- | ------------------------- | --------------- |
| `/`                    | Gallery home (all photos) | Public          |
| `/albums/`             | Album list                | Public          |
| `/albums/new/`         | Create album              | Admin only      |
| `/albums/<pk>/`        | Album detail              | Public          |
| `/albums/<pk>/edit/`   | Edit album                | Admin only      |
| `/albums/<pk>/delete/` | Delete album              | Admin only      |
| `/photos/upload/`      | Upload photo              | Logged-in users |
| `/photos/<pk>/edit/`   | Edit photo                | Owner or Admin  |
| `/photos/<pk>/delete/` | Delete photo              | Owner or Admin  |
| `/login/`              | Login                     | Public          |
| `/logout/`             | Logout                    | Authenticated   |
| `/register/`           | Register                  | Public          |
| `/admin/`              | Django Admin              | Staff/Superuser |

---

## 🔒 Security

- `SECRET_KEY` — loaded from environment variable, never hardcoded
- `DEBUG=False` — enforced in production
- `.env` — gitignored, secrets never committed to repository
- CSRF protection on all POST forms
- `LoginRequiredMixin` on all write operations
- `UserPassesTestMixin` enforces ownership checks
- Cloudinary credentials stored in environment variables only
- `ALLOWED_HOSTS` dynamically includes Render hostname

---

## 📦 Dependencies

See [`requirements.txt`](./requirements.txt) for the complete pinned list.

Key packages:

- `Django==6.0.5`
- `cloudinary==1.44.2`
- `django-cloudinary-storage==0.3.0`
- `dj-database-url==3.1.2`
- `psycopg2-binary==2.9.12`
- `gunicorn==26.0.0`
- `whitenoise==6.12.0`
- `python-dotenv==1.2.2`

---

## 👥 Author

**Course:** IT 383 — Cloud Computing  
**Project:** Production-Ready Photo Album Management System

---

## 📄 License

This project is submitted as coursework for IT 383.
