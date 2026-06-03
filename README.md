# AWS Flask Blog Portal 🚀

A full-stack cloud-based Blog Portal application built using Flask, AWS EC2, RDS MySQL, Gunicorn, Nginx, and Docker.

---

# 🌐 Live Project

http://13.127.255.145

---

# 📌 Features

- User Registration & Login
- Secure Password Hashing
- Create Blog Posts
- Edit/Delete Posts
- Like System ❤️
- Comment System 💬
- User Profile 👤
- Profile Picture Upload
- Search Posts 🔍
- Responsive UI
- Dockerized Application 🐳

---

# ☁️ AWS Services Used

- AWS EC2
- AWS RDS MySQL
- Security Groups
- VPC
- Internet Gateway

---

# 🛠️ Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- Gunicorn
- Nginx
- Docker
- Git & GitHub

---

# 📂 Project Structure

```bash
aws-flask-blog-portal/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
│
├── static/
│   ├── style.css
│   └── uploads/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create_post.html
│   ├── posts.html
│   ├── edit_post.html
│   └── profile.html
```

---

# ⚙️ Installation Steps

## Clone Repository

```bash
git clone https://github.com/gokulgireesh950-gif/aws-flask-blog-portal.git
```

## Move into Project

```bash
cd aws-flask-blog-portal
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Run Flask App

```bash
python3 app.py
```

---

# 🐳 Docker Setup

## Build Docker Image

```bash
sudo docker build -t flask-blog .
```

## Run Docker Container

```bash
sudo docker run -d -p 5000:5000 flask-blog
```

---

# 🔐 Authentication

Passwords are securely stored using Werkzeug password hashing.

---

# 🚀 Deployment

Deployed using:

- Gunicorn
- Nginx
- AWS EC2 Ubuntu Server

---

# 📸 Screenshots

(Add screenshots here)

---

# 🔮 Future Improvements

- HTTPS SSL
- Custom Domain
- CI/CD Pipeline
- AWS S3 Integration
- Notifications System
- Admin Dashboard

---

# 👨‍💻 Author

Jismon Jose

GitHub:
https://github.com/jismonjose271-hue
