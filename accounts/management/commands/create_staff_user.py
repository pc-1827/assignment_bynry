from django.core.management.base import BaseCommand
from accounts.models import User, CSRProfile

class Command(BaseCommand):
    help = 'Creates a staff user and CSR profile'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('employee_id', type=str)
        parser.add_argument('--department', type=str, default='Customer Support')
        parser.add_argument('--email', type=str, default='')
        parser.add_argument('--first_name', type=str, default='')
        parser.add_argument('--last_name', type=str, default='')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=options['email'],
            password=password,
            first_name=options['first_name'],
            last_name=options['last_name'],
            is_staff_member=True
        )
        
        # Create CSR profile
        CSRProfile.objects.create(
            user=user,
            employee_id=options['employee_id'],
            department=options['department']
        )
        
        self.stdout.write(self.style.SUCCESS(f'Staff user "{username}" created successfully'))