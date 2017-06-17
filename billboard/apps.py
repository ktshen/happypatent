from django.apps import AppConfig


class BillboardConfig(AppConfig):
    name = 'billboard'

    def ready(self):
        from billboard import signals
        from actstream import registry
        registry.register(self.get_model('Post'),
                          self.get_model('Comment'))
