from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Article



class ArticleSerializer(serializers.Serializer):
    _id = serializers.CharField()  # MongoDB document ID

    date = serializers.CharField(allow_null=True, required=False)
    text = serializers.CharField(allow_null=True, required=False)
    article_links = serializers.CharField(allow_null=True, required=False)
    scraped_date = serializers.DateTimeField(allow_null=True, required=False)
    scraped_from = serializers.CharField(allow_null=True, required=False)
    category = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    sentiment_color = serializers.CharField(allow_null=True, required=False)
    summary = serializers.CharField(allow_null=True, required=False)
    detailed_description = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    disease_disorder = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    duration = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    lab_value = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    nonbiological_location = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    title = serializers.CharField(allow_null=True, required=False)
    organizations = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    other_event = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    sign_symptom = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    subject = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    therapeutic_procedure = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    numeric_value = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    sentiment_score = serializers.FloatField(allow_null=True, required=False)
    matched_disease = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    matching_word = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    cluster_id = serializers.IntegerField(allow_null=True, required=False)
    states = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    districts = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    locations = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
    alert_url = serializers.CharField(allow_null=True, required=False)
    display_document = serializers.CharField(allow_null=True, required=False)
    disease_type = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)




# class ArticleSerializer(DocumentSerializer):
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         list_fields = [
#             'category', 'detailed_description', 'disease_disorder', 'duration',
#             'lab_value', 'nonbiological_location', 'organizations', 'other_event',
#             'sign_symptom', 'subject', 'therapeutic_procedure', 'numeric_value',
#             'matched_disease', 'matching_word', 'states', 'districts', 'locations', 
#             'disease_type'
#         ]

#         for field in list_fields:
#             try:
#                 value = data.get(field)
#                 if not isinstance(value, list):
#                     data[field] = [value] if value not in [None, float('nan')] else []
#             except Exception as e:
#                 print(f"[ERROR] Problem in field '{field}': {e}")

#         return data

#     class Meta:
#         model = Article
#         fields = "__all__"