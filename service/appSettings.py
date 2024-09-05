import os
from .models import Settings
from dotenv import load_dotenv, find_dotenv
from django.db.utils import ProgrammingError

load_dotenv(find_dotenv()) if not os.getenv("VERCEL_ENV") else None


class AppSettings:
    def __init__(self) -> None:
        settings_values = {}
        settings = Settings.objects.first()
        if not settings:
            settings = Settings()
        for field in settings._meta.fields:
            value = getattr(settings, field.name)
            if not value or value == "":
                value = os.getenv(field.name.upper())
                if value:
                    setattr(settings, field.name, value)
            settings_values[field.name] = value
        settings.save()

        self.token_pickle_base64 = settings.token_pickle_base64
        self.google_credentials = settings.google_credentials
        self.created_at = settings.created_at
        self.password = settings.password

    def __str__(self) -> str:
        return "\n".join([f"{attr}: {getattr(self, attr)}" for attr in self.list()])

    def update(self, key: str, value: str):
        if isinstance(getattr(self, key), list):
            setattr(self, key, value.split(","))
        else:
            setattr(self, key, value)
        settings = Settings.objects.first()
        setattr(settings, key, value)
        settings.save()

    def append(self, key, value):
        if not isinstance(getattr(self, key), list):
            raise ValueError(f"{key} is not a list.")
        getattr(self, key).append(value)
        settings = Settings.objects.first()
        setattr(settings, key, ",".join(getattr(self, key)))
        settings.save()

    def remove(self, key, value):
        if not isinstance(getattr(self, key), list):
            raise ValueError(f"{key} is not a list.")
        if not value in getattr(self, key):
            raise ValueError(f"{value} is not in {key}.")
        getattr(self, key).remove(value)
        settings = Settings.objects.first()
        setattr(settings, key, ",".join(getattr(self, key)))
        settings.save()

    def empty(self):
        for field in self.__dict__:
            setattr(self, field, "")
        settings = Settings.objects.first()
        for field in settings._meta.fields:
            if field.name != "id":
                setattr(settings, field.name, "")

        settings.save()

    def list(self):
        return [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    def dict(self):
        return {attr: getattr(self, attr) for attr in self.list()}


try:
    appSettings = AppSettings()

except ProgrammingError:

    class AppSettings:
        def __init__(self) -> None:
            self.token_pickle_base64 = ""
            self.google_credentials = ""
            self.created_at = ""
            self.password = ""

    appSettings = AppSettings()
