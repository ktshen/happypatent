from django.apps import AppConfig


class ProposalsConfig(AppConfig):
    name = 'proposals'

    def ready(self):
        from proposals import signals
        from actstream import registry
        registry.register(self.get_model('Patent'),
                          self.get_model('Agent'),
                          self.get_model('Inventor'),
                          self.get_model('Proposal'))
        from watson import search as watson
        watson.register(self.get_model('Proposal'))
        watson.register(self.get_model('Patent'))
        watson.register(self.get_model('Inventor'))
        watson.register(self.get_model('Agent'))
        watson.register(self.get_model('FileAttachment'))
