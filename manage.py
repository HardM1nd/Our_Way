import os
import sys


def main():
    """Run administrative tasks for Django project."""
    # Устанавливаем настройки проекта, если они ещё не заданы
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Если нужно, можно вызвать django.setup() здесь
    # (Например, если ваши скрипты требуют инициализации Django до выполнения команд)
    # try:
    #     import django
    #     django.setup()
    # except Exception:
    #     pass

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

