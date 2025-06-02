
# PH-EBS using Django Rest Framework demo testing

Trying to display all the articles from PH_EBS MongoDB database using Django Rest Framework.





## Folder structure
```
ph_drf
├── ph
│  ├── migrations
│  │  ├── __pycache__
│  │  │  └── __init__.cpython-312.pyc
│  │  └── __init__.py
│  ├── admin.py
│  ├── apps.py
│  ├── models.py
│  ├── serializers.py
│  ├── tests.py
│  ├── urls.py
│  ├── views.py
│  └── __init__.py
├── ph_drf
│  ├── asgi.py
│  ├── settings.py
│  ├── urls.py
│  ├── wsgi.py
│  └── __init__.py
├── manage.py
├── README.md
└── requirements.txt
```
## Installation

Go to the cloned repository & create the virtual enviroment in python
```bash
  cd ph_drf
```

```bash
  python venv myvenv
```

Activate the virtual enviroment.

```bash
  myvenv\Scripts\activate
```

Install the requirements
```bash
  pip install -r "requirements.txt"
```


    
## Run Locally
- MongoEngine is also ORM which bypasses the Django Models ORM.
- So we don't have to run migrations.
- Hence, instead of using Django models we will use Document from MongoEngine.
- If we had relational database with primary key, foreign key then we would have to run migrations to kiigrate data to Django models.
- Since we are not running migrations in this case, we won't be able to view data in django admin panel.

After install all the dependencies run the manage.py file..



Run the streamlit file in another terminal....

```bash
  python manage.py runserver
```
The server runs on http://localhost:8000
## API Reference

#### Get all items

```http
  GET /ph/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| None |  | Fetches JSON containing all articles from MongoDB |

#### Get item

```http
  GET /ph/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |




## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

