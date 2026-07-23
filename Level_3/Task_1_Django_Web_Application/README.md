# Codveda Auth System

A production-quality Django web application implementing secure, role-based
user authentication — built as a Python Internship submission for **Codveda
Technologies**.

The project uses Django's own battle-tested `django.contrib.auth` framework
for every security-sensitive operation (password hashing, session handling,
CSRF protection, password-reset tokens), and layers a custom **Admin / User**
role system and a Bootstrap 5 dark UI on top of it.

---

## ✨ Features

| Feature | Details |
|---|---|
| **User Registration** | Username, first/last name, email, password (with confirmation) |
| **User Login** | Django's `AuthenticationForm`, re-styled with Bootstrap 5 |
| **Logout** | One-click, CSRF-protected logout |
| **Password Reset** | Full 4-step email-based reset flow (request → email sent → confirm → complete) |
| **Dashboard** | Post-login landing page with content that adapts to the user's role |
| **User Roles** | `Admin` and `User` roles via a `Profile` model, editable from the Django admin |
| **Responsive UI** | Bootstrap 5 + custom dark/violet theme, mobile-first |
| **Security** | Hashed passwords, CSRF tokens, secure session cookies, Django's password validators |

### What Admins see vs. what Users see

- **Admin** dashboard: total user count, admin count, and a table of recently
  joined users, plus a link into the Django admin site to manage accounts.
- **User** dashboard: their own account details and a shortcut to reset their
  password.

New accounts are always created with the `User` role. To promote someone to
`Admin`, use the Django admin site (`/admin/` → *Users* → open the account →
edit the *Profile* section → set **Role = Admin**), or run
`createsuperuser`, which is automatically given the `Admin` role.

---

## 🧱 Tech stack

- **Backend:** Django 6.0 (Python 3.11+)
- **Database:** SQLite (zero-config, file-based — perfect for dev/demo)
- **Frontend:** Bootstrap 5.3, Bootstrap Icons, vanilla CSS (no build step)
- **Config:** `python-decouple` for environment-based settings (`.env`)

---

## 📁 Project structure

```
codveda_auth_system/
├── accounts/                  # Auth-related app (registration, dashboard, roles)
│   ├── admin.py               # Profile inline on the User admin page
│   ├── apps.py                # Registers the post_save signal on ready()
│   ├── forms.py                # RegistrationForm, LoginForm (Bootstrap-styled)
│   ├── migrations/
│   ├── models.py               # Profile model (role) + auto-create signal
│   ├── urls.py                 # /accounts/register/, /accounts/dashboard/
│   └── views.py                # register_view, dashboard_view
├── config/                    # Project settings & root URL config
│   ├── settings.py             # SQLite, static files, security, email backend
│   ├── urls.py                  # Wires up Django's built-in auth views
│   ├── asgi.py / wsgi.py
├── static/
│   └── css/style.css           # Custom dark/violet theme on top of Bootstrap 5
├── templates/
│   ├── base.html               # Shared layout, navbar, messages, footer
│   ├── accounts/dashboard.html
│   └── registration/           # login, register, and all password-reset pages
├── manage.py
├── requirements.txt
├── .env.example                # Copy to .env and fill in real values
├── .gitignore
├── LICENSE                     # MIT
└── README.md
```

---

## 🚀 Getting started

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd codveda_auth_system
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Generate a real secret key and paste it into `.env`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

By default, `EMAIL_BACKEND` is set to Django's **console backend** — password
reset emails are printed to your terminal instead of actually being sent, so
you can test the full flow with zero email setup. See the commented-out SMTP
section in `.env.example` to send real emails (e.g. via Gmail).

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create an admin account

```bash
python manage.py createsuperuser
```

This account is automatically given the **Admin** role.

### 7. Run the development server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** — you'll land on the login page. From there
you can:

- **Create account** → registers a new `User`-role account and logs you in
- **Sign in** as the superuser you created → see the Admin dashboard
- **Forgot password?** → triggers the reset flow (check your terminal for the
  email if using the console backend)
- **/admin/** → full Django admin, including per-user role management

---

## 🔒 Security notes

- Passwords are **never stored in plain text** — Django hashes them with
  PBKDF2 by default.
- All forms are protected by Django's **CSRF middleware**.
- Password strength is enforced by Django's built-in validators (minimum
  length, similarity to username, common-password check, not fully numeric).
- Session and CSRF cookies are marked `HttpOnly`, and `Secure`/HSTS are
  automatically enabled once `DEBUG=False`.
- Password-reset links use Django's signed, single-use tokens and expire
  automatically.

---

## 🧪 Manual test checklist

- [ ] Register a new account → redirected straight to the dashboard, logged in
- [ ] Log out → redirected to the login page
- [ ] Log back in with the same credentials → dashboard loads
- [ ] Request a password reset → email appears in the console (dev) or inbox (prod)
- [ ] Follow the reset link → set a new password → log in with it
- [ ] Log in as an Admin-role account → dashboard shows user stats + table
- [ ] Log in as a User-role account → dashboard shows personal account card only
- [ ] Resize the browser to mobile width → layout stays usable

---

## 📄 License

Released under the [MIT License](LICENSE).

---

*Built by Yaman for the Codveda Technologies Python Internship.*
