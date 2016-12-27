#!/usr/bin/env python

from lib.foreman import ForemanPuppet


class PuppetHosts(ForemanPuppet):

    def run(self, url, username, password, environment, verify_ssl, extended, only_active):
        self.url = url or self.url
        self.username = username or self.username
        self.password = password or self.password
        self.verify_ssl = verify_ssl or self.verify_ssl

        return True, dict(hosts=self.hosts(environment,extended, only_active))
