from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Category, Quiz, Question, Choice, QuizResult
from .serializers import (
    CategorySerializer,
    QuizSerializer,
    QuestionSerializer,
    ChoiceSerializer,
    QuizResultSerializer
)
from django.core.cache import cache
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class QuizPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20


class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = QuizPagination

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        quiz = self.get_object()
        answers = request.data.get('answers', {})

        if not answers:
            raise ValidationError({"answers": "This field is required."})

        score = 0
        total_questions = quiz.question_set.count()

        for question_id, choice_id in answers.items():
            try:
                question = Question.objects.get(id=question_id, quiz=quiz)
                choice = Choice.objects.get(id=choice_id, question=question)
                if choice.is_correct:
                    score += 1
            except (Question.DoesNotExist, Choice.DoesNotExist):
                raise ValidationError({
                    "answers": (
                        f"Invalid question or choice ID: "
                        f"{question_id}, {choice_id}"
                    )
                })

        if len(answers) != total_questions:
            raise ValidationError({
                "answers": f"You must answer all {total_questions} questions."
            })

        quiz_result = QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score
        )

        serializer = QuizResultSerializer(quiz_result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QuizResultViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuizResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuizResult.objects.filter(user=self.request.user)


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        quiz_id = request.query_params.get('quiz_id')
        if quiz_id:
            cache_key = f'questions_quiz_{quiz_id}'
            questions = cache.get(cache_key)
            if not questions:
                questions = self.queryset.filter(quiz_id=quiz_id)
                cache.set(cache_key, questions, settings.CACHE_TTL)
        else:
            questions = self.queryset

        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)
