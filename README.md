# **MASS**: _Medical Appointment Scheduling System_

> A full-stack medical scheduling web application built with [Flask](https://flask.palletsprojects.com/en/stable/), containerized with [Docker](https://www.docker.com/), and served via [Gunicorn](https://gunicorn.org/) and [Nginx](https://nginx.org/en/).

## Table of Contents

- [Preview](#preview)
- [File Structure](#file-structure)
- [About the Project](#about-the-project)
- [Environment Variables](#environment-variables)
- [Manual Setup](#manual-setup)
- [Docker Setup](#docker-setup)

## Preview

> For the previews I used horror movie characters as sample users.

### Home

![image](https://github.com/user-attachments/assets/a3d7ae71-91aa-4a65-a310-f9f66c68f8be)

### Admin Panel

![image](https://github.com/user-attachments/assets/0c4e1215-c33b-4574-8832-2e6f899a062d)

### Appointments (Admin)

![image](https://github.com/user-attachments/assets/5b9dc803-9996-4d64-b7f7-b4147099bd19)

### Appointments (Patient)

![image](https://github.com/user-attachments/assets/9c512f22-c7b5-4175-8831-cce08723da5a)

### New Appointment

![image](https://github.com/user-attachments/assets/42bb0c84-5b1b-4fea-9a8d-14bcf38eef79)

## File Structure

```bash
MASS
├── app
│   ├── admin/
│   ├── appointments/
│   ├── auth/
│   ├── models/
│   ├── static/
│   └── templates/
├── docker-compose.yml
├── Dockerfile
├── gen-certs.sh
├── LICENSE
├── main.py
├── nginx/default.conf
├── pyproject.toml
└── README.md
```

## About the Project

MASS was my final project for **COMP-2052** and the most ambitious app I've developed so far. It enables users to register, log in, and schedule appointments, with roles for Admins, Doctors, and Patients. Now I'm going to keep developing it as a full app.

## Environment Variables

After cloning the repo, `cd` into it. Then, create a `.env` file in the project root with the following:

```env
SECRET_KEY='your_secret_key_here'

# Default Admin Credentials (change these!)
ADMIN_FIRSTNAME='Default'
ADMIN_LASTNAME='Admin'
ADMIN_EMAIL='admin@example.com'
ADMIN_PASSWORD='changeme123'

# Email settings — required for password reset functionality
# Use valid SMTP credentials (e.g., Gmail with App Passwords)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password   # Use a Gmail App Password
MAIL_DEFAULT_SENDER=your_email@gmail.com
```

To generate a secure `SECRET_KEY`:

```bash
python -c 'import secrets; print(secrets.token_hex(16))'
```

## Manual Setup

> Instead of the usual pip and venv setup, I'll use uv to take care of this.

Make sure to have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

First, clone the repo and `cd` into it (if you haven't already):

```bash
git clone https://github.com/arosario513/MASS.git
cd MASS
```

Then make sure `start.sh` is executable

```bash
chmod +x start.sh
```

## Running the App (Manually)

Now you can run it with the bash script which will set up everything and start up the app:

```bash
./start.sh
```

You may change the port and number of workers if needed inside `start.sh`.

## Docker Setup

> **Preferred method** – easier, isolated, and more secure.

Ensure you have Docker and OpenSSL installed.

1. Clone the repo and create your `.env` file.
2. Generate self-signed SSL certs:

```bash
./gen-certs.sh
```

Example output:

```
[+] Generating root CA...
[+] Issuing cert for mass-server...
Certificate request self-signature ok
subject=C=US, ST=PR, O=MASS, OU=MASS, CN=mass-server
```

3. Verify certificates were created in `nginx/certs/`.

4. Build and run the app:

```bash
docker-compose up -d --build
```

after that, you can run it with:

```bash
docker-compose up -d
```

After running it, visit:

- [https://127.0.0.1](https://127.0.0.1)
- [https://mass.localhost](https://mass.localhost)

**Note**: Browsers will warn you about the self-signed certs. For production, replace them with real certificates and update `nginx/default.conf` accordingly.

5. To stop the app just run:

```bash
docker-compose down
```
