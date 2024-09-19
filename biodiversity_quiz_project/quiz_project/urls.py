from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from quiz_app.views import (
    CategoryViewSet,
    QuizViewSet,
    QuizResultViewSet,
    QuestionViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'results', QuizResultViewSet, basename='quizresult')
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
