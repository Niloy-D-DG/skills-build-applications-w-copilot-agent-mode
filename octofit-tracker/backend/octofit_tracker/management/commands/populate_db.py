import random
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # clear existing data
        self.stdout.write('Deleting existing data...')
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # sample heroes
        marvel_heroes = ['Iron Man', 'Spider-Man', 'Thor', 'Hulk', 'Black Widow']
        dc_heroes = ['Batman', 'Superman', 'Wonder Woman', 'Flash', 'Aquaman']

        users = []
        for name in marvel_heroes:
            users.append(User.objects.create(name=name, email=f"{name.replace(' ', '').lower()}@example.com", team=marvel))
        for name in dc_heroes:
            users.append(User.objects.create(name=name, email=f"{name.replace(' ', '').lower()}@example.com", team=dc))

        # create some workouts
        w1 = Workout.objects.create(name='Cardio Blast', description='High intensity cardio routine')
        w2 = Workout.objects.create(name='Strength Training', description='Build muscle strength')
        w1.suggested_for.set(users[:3])
        w2.suggested_for.set(users[3:6])

        # create activities and leaderboard entries
        for user in users:
            # random activities
            for _ in range(3):
                Activity.objects.create(
                    user=user,
                    activity_type=random.choice(['Run', 'Swim', 'Bike', 'Yoga']),
                    duration=random.randint(20, 120),
                    date=timezone.now().date()
                )
            # leaderboard score
            score = random.randint(0, 1000)
            Leaderboard.objects.create(user=user, score=score, rank=0)

        # assign ranks based on score
        entries = list(Leaderboard.objects.order_by('-score'))
        for idx, entry in enumerate(entries, start=1):
            entry.rank = idx
            entry.save()

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
