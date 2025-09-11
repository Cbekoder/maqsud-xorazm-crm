from django.core.management.base import BaseCommand

from models import User, Group, UserGroups


class Command(BaseCommand):
    help = "Add existing Users to Group"

    def handle(self, *args, **options):
        user_group_created = 0
        user_group_exists = 0
        for n in range(3, 14):
            student = User.objects.get(username=f"student{n}")
            group = Group.objects.get(pk=12)

            user_group, created = UserGroups.objects.get_or_create(
                user=student,
                group=group
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    "student added"
                ))
                user_group_created += 1
            else:
                self.stdout.write(self.style.WARNING(
                    "student exists"
                ))

                user_group_exists += 1

        self.stdout.write(self.style.SUCCESS(
            f"Summary: Added {user_group_created}, exists {user_group_exists}"
        ))



