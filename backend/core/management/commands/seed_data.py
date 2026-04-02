from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Topic, ForumPost, ForumMember
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusCommunity with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexuscommunity.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Topic.objects.count() == 0:
            for i in range(10):
                Topic.objects.create(
                    title=f"Sample Topic {i+1}",
                    category=f"Sample {i+1}",
                    author=f"Sample {i+1}",
                    replies=random.randint(1, 100),
                    views=random.randint(1, 100),
                    status=random.choice(["open", "closed", "pinned", "locked"]),
                    last_reply=date.today() - timedelta(days=random.randint(0, 90)),
                    tags=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Topic records created'))

        if ForumPost.objects.count() == 0:
            for i in range(10):
                ForumPost.objects.create(
                    topic_title=f"Sample ForumPost {i+1}",
                    author=f"Sample {i+1}",
                    content=f"Sample content for record {i+1}",
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                    likes=random.randint(1, 100),
                    status=random.choice(["published", "flagged", "hidden"]),
                    is_solution=random.choice([True, False]),
                )
            self.stdout.write(self.style.SUCCESS('10 ForumPost records created'))

        if ForumMember.objects.count() == 0:
            for i in range(10):
                ForumMember.objects.create(
                    username=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    email=f"demo{i+1}@example.com",
                    join_date=date.today() - timedelta(days=random.randint(0, 90)),
                    posts=random.randint(1, 100),
                    reputation=random.randint(1, 100),
                    role=random.choice(["member", "moderator", "admin"]),
                    bio=f"Sample bio for record {i+1}",
                    active=random.choice([True, False]),
                )
            self.stdout.write(self.style.SUCCESS('10 ForumMember records created'))
