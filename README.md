# StudyBud
Developed a responsive full featured Discord like web application with register login, logout, and some CRUD operations on chat rooms, and search option to assist the users in finding their study partners for discussion purposes.

* This project is learnt from an epic 7hr [youtube video](https://www.youtube.com/watch?v=PtQiiknWUcI&t=23154s). I learnt a lot from this project and a big thanks to him.

### APP Preview
**Home Page**
![home page](https://github.com/AI-kartheek/StudyBud/blob/main/pics/home.png)

**Room Page**
![room page](https://github.com/AI-kartheek/StudyBud/blob/main/pics/room.png)

**Profile Page**
![profile page](https://github.com/AI-kartheek/StudyBud/blob/main/pics/profile.png)

### Functionality and Features
* Register, login, logout
* Create new room
* Join a chat room and start conversation
* Search rooms by topic name, room name, room description.
* Delete message
* Interactive user profile page shows all the rooms created and rooms joined by him.
* Upload profile picture
* responsive on almost all devices.

### Tools And Technology
* Python
* Django
* SQLite Database
* HTML
* CSS
* JavaScript

### Cloning the repository
* **STEP-1:** Clone the repository using the command below :
```bash
git clone https://github.com/AI-kartheek/StudyBud.git

```

* **STEP-2:** Move into the directory where we have the project files : 
```bash
cd StudyBud

```

* **STEP-3:** Create a virtual environment :
```bash
# Let's install virtualenv first
pip install virtualenv

# Then we create our virtual environment
virtualenv env_name

```

* **STEP-4:** Activate the virtual environment :
```bash
env_name\scripts\activate

```

* **STEP-5:** Install the requirements :
```bash
pip install -r requirements.txt

```

* **STEP-6:** locate to the folder containing `manage.py` file and run the App with below command - 
```bash
python manage.py runserver

```

> Then, the development server will be started at http://127.0.0.1:8000/
