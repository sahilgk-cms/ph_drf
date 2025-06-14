from django.shortcuts import render, get_object_or_404
from .models import Article
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import Http404 
from ph.serializers import ArticleSerializer
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from mongoengine.connection import get_db
from rest_framework.response import Response
from pymongo import DESCENDING
from bson import ObjectId
from rest_framework import status
from rest_framework_mongoengine.generics import ListAPIView, RetrieveAPIView
from bson.son import SON
from datetime import datetime
from dateutil.relativedelta import relativedelta
# Create your views here.

      
TIMESPAN_DICT = {
    'this week': datetime.now() - relativedelta(days=7),
    'this month': datetime.now().replace(day=1),
    'past 3 months': datetime.now() - relativedelta(months=3),
    'past 6 months': datetime.now() - relativedelta(months=6),
    'past 1 year': datetime.now() - relativedelta(years=1),
    'all time': datetime.now() - relativedelta(years=100),
}

      
class ArticleListAV(APIView):
    def get(self, request):
        db = get_db()
        collection = db["processed_data"]

        # Filters
        match_stage = {}

        # Severity
        severity = request.GET.get('Severity')
        if severity and severity != "All":
            sentiment_color = None
            if severity == "Low":
                sentiment_color = "green"
            elif severity == "Medium":
                sentiment_color = "orange"
            elif severity == "High":
                sentiment_color = "red"

            if sentiment_color:
                match_stage['sentiment_color'] = sentiment_color

        # Category
        category = request.GET.get('Categories')
        if category and category != "All":
            match_stage['category'] = {'$in': [category.lower()]}

        # timespan
        timespan = (request.GET.get("Timespan") or "").lower()
        if timespan != "All Time":
            start_date = TIMESPAN_DICT.get(timespan)
            if start_date:
                match_stage["$expr"] = {
                    "$gte":[
                        {
                            "$dateFromString":{
                                "dateString": "$date",
                                "format": "%d/%m/%Y",
                                "onError": None,
                                "onNull": None
                            }
                        },
                        start_date
                    ]
                }
            

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page_number = int(request.GET.get('page', 1))
        skip = (page_number - 1) * paginator.page_size

        # Total count for frontend
        total_count = collection.count_documents(match_stage)

        # Efficient MongoDB pagination using skip + limit
        results = list(
            collection.find(match_stage)
            .sort("date", -1)
            .skip(skip)
            .limit(paginator.page_size)
        )

        # Convert ObjectId for serialization
        for item in results:
            item['_id'] = str(item['_id'])

        serializer = ArticleSerializer(results, many=True)

        return Response({
            'count': total_count,
            'next': page_number + 1 if skip + paginator.page_size < total_count else None,
            'previous': page_number - 1 if page_number > 1 else None,
            'results': serializer.data,
        })


class ArticleDetailAV(APIView):
    def get(self, request, pk):
        db = get_db()
        collection = db["processed_data"]

        try:
            obj_id = ObjectId(pk)
        except:
            return Response({"Error": "Invalid ID"}, status = status.HTTP_400_BAD_REQUEST)
        
        article = collection.find_one({"_id": obj_id})
        if not article:
            return Response({"Error": "Article not found"}, status = status.HTTP_404_NOT_FOUND)
        
        article["_id"] = str(article["_id"])
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


class GroupBySentimentAV(APIView):
    def get(self, request):
        db = get_db()
        collection = db["processed_data"]

        #group by sentiment and value count
        pipeline = [
                    {"$group": {"_id":"$sentiment_color",
                      "count": {"$sum":1}}},
                    {"$sort": SON([("count", -1)])}
                    ] 

        results = list(collection.aggregate(pipeline))

        sentiments = [r["_id"] for r in results]
        count = [r["count"] for r in results] 

        return Response({"sentiment": sentiments, "count": count})

# These are some more inbuilt API Views which work comfortably with Django models but not with MongoDB
# These inbuilt views could have helped in reducing code 

# class ArticleListAV(ListAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer

#     def get(self, request, *args, **kwargs):
#         try:
#             return self.list(request, *args, **kwargs)
#         except Exception as e:
#             print(f"[CRASH] Error in ArticleListAV: {e}")
#             raise e


# class ArticleListAV(ListAPIView):
#     serializer_class = ArticleSerializer
#     queryset = Article.objects.all()

#     def get_queryset(self):
#         queryset = self.queryset

#         sentiment_color = self.request.GET.get('sentiment_color')
#         if sentiment_color:
#             queryset = queryset.filter(sentiment_color=sentiment_color)

#         category = self.request.GET.get('category')
#         if category:
#             queryset = queryset.filter(category__contains=[category])

#         return queryset
    

# class ArticleDetailAV(RetrieveAPIView):
#     serializer_class = ArticleSerializer
#     queryset = Article.objects.all()
#     lookup_field = "_id"
