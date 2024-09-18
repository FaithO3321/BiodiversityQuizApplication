import json
from django.core.management.base import BaseCommand
from quiz_app.models import Category, Quiz, Question, Choice

class Command(BaseCommand):
    help = 'Load questions from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        with open(options['json_file'], 'r') as file:
            data = json.load(file)
            
        category, _ = Category.objects.get_or_create(name=data['category'])
        quiz, _ = Quiz.objects.get_or_create(title=data['title'], category=category)
        
        for question_data in data['questions']:
            question = Question.objects.create(
                quiz=quiz,
                text=question_data['text']
            )
            for choice_data in question_data['choices']:
                Choice.objects.create(
                    question=question,
                    text=choice_data['text'],
                    is_correct=choice_data['is_correct']
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded questions for quiz: {quiz.title}'))
