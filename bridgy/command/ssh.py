from bridgy.error import *
from bridgy.inventory import get_bastion

class Ssh(object):

    def __init__(self, config, instance):
        if not hasattr(config, '__getitem__'):
            raise BadConfigError
        if not isinstance(instance, tuple):
            raise BadInstanceError

        self.config = config
        self.instance = instance

    @property
    def destination(self):
        if self.instance.user:            
            return '{user}@{host}'.format(user=self.instance.user,
                                         host=self.instance.address)

        elif self.config.dig('ssh', 'user'):
            return '{user}@{host}'.format(user=self.config.dig('ssh', 'user'),
                                          host=self.instance.address)
        else:
            return self.instance.address

    @property
    def options(self):
        identity = ''
        bastion = ''
        options = ''

        bastionObj = get_bastion(self.config, self.instance)

        if bastionObj != None:
            template = "-o ProxyCommand='ssh {options} -W %h:%p {destination}'"
            bastion = template.format(options=bastionObj.options,
                                      destination=bastionObj.destination)

        options = self.config.dig('ssh', 'options') or ''
        if self.instance.key:
            identity = '-i %s'%self.instance.key
        return '{} {} {}'.format(identity,bastion, options)


    @property
    def command(self):
        cmd = 'ssh {options} {destination}'
        return cmd.format(destination=self.destination,
                          options=self.options )
