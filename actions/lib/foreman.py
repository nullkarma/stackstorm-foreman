#!/usr/bin/env python

from st2actions.runners.pythonrunner import Action
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ForemanAPI(Action):
    def __init__(self, config):
        super(ForemanAPI, self).__init__(config=config)
        self.url = self.config.get('url', None)
        self.username = self.config.get('username', None)
        self.password = self.config.get('password', None)
        self.verify_ssl = self.config.get('verify_ssl', False)

        self._headers = {"Accept": "version=2,application/json"}

    def active_hosts(self, hosts):
        for host in hosts:
            try:
                hostname = host.get('name')
            except AttributeError:
                hostname = host

            host_status = self._query("hosts/{0}/status/global".format(hostname), verify_ssl=self.verify_ssl).get(
                'status')
            if host_status == 0:
                yield host

    def _query(self, endpoint, verify_ssl):
        api_url = "{url}/{api_ext}/{endpoint}".format(url=self.url, api_ext='api', endpoint=endpoint)
        response = requests.get(api_url,
                                auth=(self.username, self.password),
                                headers=self._headers,
                                verify=verify_ssl or self.verify_ssl,
                                params={"per_page": "100"})

        if response.status_code == 200:
            return response.json()
        else:
            return response.text

    def query(self, *args, **kwargs):
        return self._query(*args, **kwargs)


class ForemanPuppet(ForemanAPI):
    def __init__(self, config):
        super(ForemanPuppet, self).__init__(config=config)

    def hosts(self, environment, extended, only_active):
        hosts_raw = self._query("environments/{0}/hosts".format(environment), verify_ssl=self.verify_ssl).get('results')
        if only_active:

            # hosts = [host for host in hosts_raw if host['global_status'] == 0]

            # BUG: Global Status is always set to 0, even if a system is shutdown.
            # 'hosts/:id/status/global' tells the truth, or like in this quick fix
            # global_status_label does, too. But it might not be as acurate as 'status/global'

            # hosts = [host for host in hosts_raw if host['global_status_label'] == 'OK']

            # That's why a 2nd query fetches the true host status

            hosts = [host for host in self.active_hosts(hosts_raw)]
        else:
            hosts = hosts_raw

        if not extended:
            try:
                return [host.get('name') for host in hosts]
            except AttributeError:
                pass

        return hosts
