import os


class Configuration:

    domain = None

    @classmethod
    def init_domain(cls):
        domain = os.environ.get('BEANSTALK_DOMAIN')
        if not domain:
            domain = 'http://localhost:8000/'
        return domain

    @classmethod
    def get_domain(cls):
        if not cls.domain:
            cls.domain = cls.init_domain()
        return cls.domain
