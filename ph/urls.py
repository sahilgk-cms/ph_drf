from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleListAV.as_view(), name = "article-index-page"),
    path("group_by_sentiment/", views.GroupBySentimentAV.as_view(), name = "group-by-sentiment"),
    path("generate_summary/", views.GenerateSummaryView.as_view(), name = "summary-page"),
    path("generate_situational_report/", views.GenerateSituationalReportView.as_view(), name = "situational-report-page"),
    path("generate_risk_assessment/", views.GenerateRiskAssessmentReportView.as_view(), name = "risk-assessment-page"),
    path("<str:pk>/", views.ArticleDetailAV.as_view(), name = "article-detail-page")
   
]