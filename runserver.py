import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    from django.core.management import execute_from_command_line
    # Auto-run migrations
    execute_from_command_line([sys.argv[0], 'migrate', '--noinput'])
    # Start server
    execute_from_command_line([sys.argv[0], 'runserver', '0.0.0.0:8000'])


if __name__ == '__main__':
    main()



