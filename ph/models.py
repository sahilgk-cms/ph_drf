from django.db import models
from mongoengine import Document, StringField, DateTimeField, ListField, FloatField, IntField

# Create your models here.

# MongoEngine is also ORM which bypasses the Django Models ORM
# so we don't have to run migrations
# hence, instead of using Django models we will use Document from MongoEngine
# if we had relational database with primary key, foreign key then we would have to run migrations to kiigrate data to Django models
# since we are not running migrations in this case, we won't be able to view data in django admin panel

class Article(Document):
    date = StringField()
    text = StringField()
    article_links = StringField()
    scraped_date = DateTimeField()
    scraped_from = StringField()
    category = ListField(StringField())
    sentiment_color = StringField()
    summary = StringField()
    detailed_description = ListField(StringField())
    disease_disorder = ListField(StringField())
    duration = ListField(StringField())
    lab_value = ListField(StringField())
    nonbiological_location = ListField(StringField())
    title = StringField()
    organizations = ListField(StringField())
    other_event = ListField(StringField())
    sign_symptom = ListField(StringField())
    subject = ListField(StringField())
    therapeutic_procedure = ListField(StringField())
    numeric_value = ListField(StringField())
    sentiment_score = FloatField()
    matched_disease = ListField(StringField())
    matching_word = ListField(StringField())
    cluster_id = IntField()
    states = ListField(StringField())
    districts = ListField(StringField())
    locations = ListField(StringField())
    alert_url = StringField()
    display_document = StringField()
    disease_type = ListField(StringField())
    
    # some keys might not be present in each data point hence set strict = False to avoid errors 
    meta = {"collection": "processed_data", 'strict': False}

