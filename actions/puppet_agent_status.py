#!/usr/bin/env python

from lib.foreman import ForemanPuppet


class PuppetAgentStatus(ForemanPuppet):

    def _filter(self, hosts, status):
        for host in hosts:
            status_label = self.query("hosts/{0}/status/configuration".format(host), self.verify_ssl).get('status_label')

            if status_label.lower() == status:
                yield host

    def run(self, url, username, password, hosts, environment, status, verify_ssl, extended, only_active):
        self.url = url or self.url
        self.username = username or self.username
        self.password = password or self.password
        self.verify_ssl = verify_ssl or self.verify_ssl

        if hosts:
            hosts_list = hosts
        else:
            hosts_list = self.hosts(environment, extended, only_active)

        return True, dict(hosts=list(self._filter(hosts_list, status)))
