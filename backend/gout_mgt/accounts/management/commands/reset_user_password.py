from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()

class Command(BaseCommand):
    help = '重置指定用户的密码'

    def add_arguments(self, parser):
        parser.add_argument('phone', type=str, help='用户的手机号')
        parser.add_argument(
            '--password',
            type=str,
            help='新密码，如果不提供则自动生成',
            required=False
        )

    def handle(self, *args, **options):
        phone = options['phone']
        password = options['password']
        
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise CommandError(f'手机号为 {phone} 的用户不存在')
        
        if not password:
            # Generate a random 8-character password
            password = get_random_string(8)
        
        user.set_password(password)
        user.save()
        
        self.stdout.write(self.style.SUCCESS(f'用户 {phone} 的密码已重置为: {password}'))