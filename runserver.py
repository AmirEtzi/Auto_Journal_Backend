import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    from django.core.management import execute_from_command_line
    # Auto-run migrations
    execute_from_command_line([sys.argv[0], 'migrate', '--noinput'])
    # Start server
    port = os.environ.get('PORT', '8000')
    execute_from_command_line([sys.argv[0], 'runserver', f'0.0.0.0:{port}'])


if __name__ == '__main__':
    main()
