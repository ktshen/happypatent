from django.apps import AppConfig


class ProposalsConfig(AppConfig):
    name = 'proposals'

    def ready(self):
        from proposals import signals
        from actstream import registry
        registry.register(self.get_model('Patent'),
                          self.get_model('Agent'))
