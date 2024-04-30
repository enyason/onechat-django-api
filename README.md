## OneChat - Real-time Messaging App (Django)

OneChat is a real-time messaging application built with Django that allows users to connect instantly and stay close with friends, family, or communities.

**Features:**

* **Real-time Messaging:** Messages are delivered instantly, fostering a seamless communication experience.
* **Group Chats:** Connect with multiple people in a single chat room
* **Community Focus:** You don't have to be alone, you can be a part of any community group that brings you joy'

**Getting Started:**

1. **Prerequisites:**
    * Python 3.12+
    * pip (package installer for Python)
2. **Clone the repository:**

```bash
git clone https://github.com/enyason/onechat-django-api.git
```

3. **Create a virtual environment (recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Create a database:**

   OneChat uses Django's ORM for data persistence. Refer to the Django documentation for setting up a database backend: [https://docs.djangoproject.com/en/5.0/](https://docs.djangoproject.com/en/5.0/)

6. **Run database migrations:**

   ```bash
   python manage.py migrate
   ```

7. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server:**

    OneChat uses Django Channels for asynchronous websocket communication.

   ```bash
   gunicorn --bind 0.0.0.0:8000 onechat_api.asgi:application -k uvicorn.workers.UvicornWorker --access-logfile '-' --error-logfile '-'
   ```

   This will start the server, usually accessible at http://127.0.0.1:8000/ in your web browser.

**Configuration:**

You can configure various aspects of OneChat by modifying settings in `onechat/settings.py`.