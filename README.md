
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
│  ├── utils
│  │  ├── data_retrieving.py
│  │  ├── date_formatting.py
│  │  ├── entity_extraction.py
│  │  └── generating_reports.py
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
│  ├── config.py
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

![image](https://github.com/user-attachments/assets/7d128843-b15e-4199-a392-67d712b1ab78)


#### Get item

```http
  GET /ph/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

![image](https://github.com/user-attachments/assets/138793a6-76fc-4f44-bc4c-01bc5dc4b598)



#### Generate summary
```http
  GET /ph/generate_summary
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| None |  | Generates Summary |

![image](https://github.com/user-attachments/assets/3c162f63-9762-4da5-8a50-fb45d402c463)


#### Generate situational report
```http
  GET /ph/generate_situational_report
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| None |  | Generates situational report |

![image](https://github.com/user-attachments/assets/4fdd7f21-ed92-44e7-bf8c-3c3cd0328de1)


#### Generate risk assessment report
```http
  POST /ph/generate_risk_assessment
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| None |  | Generates risk assessment report |


![image](https://github.com/user-attachments/assets/ea408634-02ac-47e9-ab67-b38293f62251)


#### Group by sentiment
```http
  GET /ph/group_by_sentiment
```
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| None |  | Group by sentiment |


![image](https://github.com/user-attachments/assets/f9e3f5ef-e1c4-40c9-8ef2-7d391240cbc2)



