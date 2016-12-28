#!/usr/bin/env python

from lib.foreman import ForemanAPI


class ForemanHosts(ForemanAPI):

    def run(self, url, username, password, verify_ssl, extended, only_active):
        self.url = url or self.url
        self.username = username or self.username
        self.password = password or self.password
        self.verify_ssl = verify_ssl or self.verify_ssl

        payload = {"hosts": list()}

        hosts_raw = self._query("hosts", verify_ssl=verify_ssl).get('results')
        if only_active:
            hosts = [host for host in self.active_hosts(hosts_raw)]
        else:
            hosts = hosts_raw

        if extended:
            payload['hosts'] = hosts
        else:
            try:
                payload['hosts'] = [host.get('name') for host in hosts]
            except AttributeError:
                payload['hosts'] = [host for host in hosts]

        return True, payload
