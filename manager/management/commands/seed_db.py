# manager/management/commands/seed_db.py
from datetime import timedelta
from random import sample

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from manager.models import Position, TaskType, Task   # your models

User = get_user_model()  # custom Worker model


class Command(BaseCommand):
    help = "Populate the database with demo Positions, Workers, TaskTypes and Tasks."

    def add_arguments(self, parser):
        parser.add_argument("--workers", type=int, default=5,
                            help="How many workers to create (default: 5)")
        parser.add_argument("--tasks", type=int, default=10,
                            help="How many tasks to create (default: 10)")

    def handle(self, *args, **opts):
        num_workers = opts["workers"]
        num_tasks   = opts["tasks"]

        # ---------- Positions ----------------------------------------------
        dev, _ = Position.objects.get_or_create(name="Developer")
        qa,  _ = Position.objects.get_or_create(name="QA Engineer")
        pm,  _ = Position.objects.get_or_create(name="Project Manager")

        # ---------- Workers -------------------------------------------------
        workers = []
        for i in range(1, num_workers + 1):
            worker, created = User.objects.get_or_create(
                username=f"user{i}",
                defaults={
                    "first_name": f"Demo{i}",
                    "last_name": "User",
                    "email": f"user{i}@example.com",
                    "position": [dev, qa, pm][i % 3],
                },
            )
            if created:
                worker.set_password("password")
                worker.save()
            workers.append(worker)
        self.stdout.write(self.style.SUCCESS(f"Workers ready: {len(workers)}"))

        # ---------- Task types ---------------------------------------------
        bugfix,  _ = TaskType.objects.get_or_create(name="Bug Fix")
        feature, _ = TaskType.objects.get_or_create(name="Feature")
        refactor, _= TaskType.objects.get_or_create(name="Refactor")
        task_types = [bugfix, feature, refactor]

        # ---------- Tasks ---------------------------------------------------
        priorities = ["Urgent", "High", "Normal", "Low"]

        for i in range(1, num_tasks + 1):
            task = Task.objects.create(
                name=f"Task #{i}",
                description=f"Auto-generated task {i}",
                deadline=timezone.now() + timedelta(days=i),
                is_completed=False,
                priority=priorities[i % len(priorities)],
                task_type=task_types[i % len(task_types)],
            )
            # assign 1-3 random workers
            task.assignees.set(sample(workers, min(3, len(workers))))

        self.stdout.write(self.style.SUCCESS(f"Tasks created: {num_tasks}"))
        self.stdout.write(self.style.SUCCESS("Database seeding complete!"))
