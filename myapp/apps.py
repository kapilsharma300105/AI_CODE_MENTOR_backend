from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals   # ✅ yahi important hai
        from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        try:
            from django.contrib.sites.models import Site
            site, _ = Site.objects.get_or_create(id=1)
            site.domain = "ai-code-mentor-backend-0rmn.onrender.com"
            site.name = "AI Code Mentor"
            site.save()
        except:
            pass