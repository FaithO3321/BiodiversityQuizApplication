from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Quiz, Question, Choice, QuizResult


class QuizAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name='Test Category')
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            category=self.category
        )

        self.question = Question.objects.create(
            quiz=self.quiz,
            text='Test Question'
        )

        self.choice1 = Choice.objects.create(
            question=self.question,
            text='Choice 1',
            is_correct=True
        )

        self.choice2 = Choice.objects.create(
            question=self.question,
            text='Choice 2',
            is_correct=False
        )

    def test_list_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_quizzes(self):
        response = self.client.get('/api/quizzes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_questions(self):
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_submit_quiz(self):
        data = {
            'answers': {
                str(self.question.id): self.choice1.id
            }
        }
        response = self.client.post(
            f'/api/quizzes/{self.quiz.id}/submit/',
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['score'], 1)

    def test_submit_quiz_invalid_answer(self):
        data = {
            'answers': {
                str(self.question.id): 9999  # Invalid choice ID
            }
        }
        response = self.client.post(
            f'/api/quizzes/{self.quiz.id}/submit/',
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_quiz_missing_answer(self):
        data = {
            'answers': {}
        }
        response = self.client.post(
                f'/api/quizzes/{self.quiz.id}/submit/',
                data=data,
                format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_results(self):
        QuizResult.objects.create(user=self.user, quiz=self.quiz, score=1)
        response = self.client.get('/api/results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_quizzes_pagination(self):
        # Create 10 more quizzes
        for i in range(10):
            Quiz.objects.create(title=f'Test Quiz {i}', category=self.category)

    response = self.client.get('/api/quizzes/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('results', response.data)
    self.assertIn('count', response.data)
    self.assertIn('next', response.data)
    self.assertIn('previous', response.data)
    self.assertEqual(len(response.data['results']), 5)

    def test_list_questions_pagination(self):
        # Create 15 more questions
        for i in range(15):
            Question.objects.create(quiz=self.quiz, text=f'Test Question {i}')

    response = self.client.get('/api/questions/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('results', response.data)
    self.assertIn('count', response.data)
    self.assertIn('next', response.data)
    self.assertIn('previous', response.data)
    self.assertEqual(len(response.data['results']), 10)  # Default page size
