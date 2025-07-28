# Skillern – E-Learning Platform

**Skillern** is a modern e-learning platform designed to provide users with a smooth and intuitive experience for online learning. It supports course enrollment, video-based lessons, certification, and more – all built with Django.

---

## 🚀 Features

### 🎓 Courses
- Browse a variety of online courses.
- Each course includes multiple video lessons.

### 📹 Video-Based Learning
- Embedded course videos.
- Manual progress tracking: users can mark videos as completed.

### 📜 Certification System
- Automatically generate and download a certificate upon completing all videos in a course.

### 🧑‍💻 User Authentication
- Secure login and registration system.
- Users can view their enrolled courses and completed certifications.

### 💰 Payment Integration
- Razorpay integration for secure course purchases.

### 🖼️ Admin Panel
- Django admin interface for managing users, courses, and content.

---

## 🔧 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap, Jinja2
- **Database:** SQLite (default)
- **Payment Gateway:** Razorpay
- **Version Control:** Git + GitHub

---

## 🛠️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/Hitenshu/Skillern-E-learning-platform.git
cd Skillern-E-learning-platform

# Create and activate virtual environment
python -m venv myenv
myenv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Set up the database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver
