from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.utils import timezone
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populates the database with test data for OctoFit Tracker.'

    def handle(self, *args, **options):
        # Use pymongo to clear collections directly
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]
        db[User._meta.db_table].delete_many({})
        db[Team._meta.db_table].delete_many({})
        db[Activity._meta.db_table].delete_many({})
        db[Leaderboard._meta.db_table].delete_many({})
        db[Workout._meta.db_table].delete_many({})

        # Create Teams
        team1 = Team.objects.create(name='Red Rockets', description='The fastest team in Mergington!')
        team2 = Team.objects.create(name='Blue Blazers', description='Blazing through every workout!')

        # Create Users
        user1 = User.objects.create(username='alice', email='alice@example.com', team=team1)
        user2 = User.objects.create(username='bob', email='bob@example.com', team=team1)
        user3 = User.objects.create(username='carol', email='carol@example.com', team=team2)
        user4 = User.objects.create(username='dave', email='dave@example.com', team=team2)

        # Create Workouts
        workout1 = Workout.objects.create(name='Morning Run', description='3km run around the school', points=30)
        workout2 = Workout.objects.create(name='Pushup Challenge', description='50 pushups', points=20)
        workout3 = Workout.objects.create(name='Jump Rope', description='5 minutes nonstop', points=15)

        # Create Activities
        Activity.objects.create(user=user1, workout=workout1, date=timezone.now(), points_earned=30)
        Activity.objects.create(user=user2, workout=workout2, date=timezone.now(), points_earned=20)
        Activity.objects.create(user=user3, workout=workout3, date=timezone.now(), points_earned=15)
        Activity.objects.create(user=user4, workout=workout1, date=timezone.now(), points_earned=30)

        # Create Leaderboard entries
        Leaderboard.objects.create(team=team1, total_points=50)
        Leaderboard.objects.create(team=team2, total_points=45)

        self.stdout.write(self.style.SUCCESS('Test data successfully populated!'))