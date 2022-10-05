# Microsoft Azure Linux Agent
#
# Copyright 2022 Bernhard Rosenkränzer <bero@lindev.ch>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Requires Python 2.6+ and OpenSSL 1.0+

import azurelinuxagent.common.utils.shellutil as shellutil
from azurelinuxagent.common.osutil.default import DefaultOSUtil

class OpenMandrivaOSUtil(DefaultOSUtil):
    def __init__(self):
        super(OpenMandrivaOSUtil, self).__init__()
        self.agent_conf_file_path = '/etc/waagent.conf'
        self.jit_enabled = True

    @staticmethod
    def get_systemd_unit_file_install_path():
        return '/usr/lib/systemd/system'

    @staticmethod
    def get_agent_bin_path():
        return '/usr/bin'

    def is_dhcp_enabled(self):
        return True

    def start_network(self):
        return shellutil.run("systemctl start NetworkManager", chk_err=False)

    def restart_if(self, ifname=None, retries=None, wait=None):
        retry_limit = retries+1
        for attempt in range(1, retry_limit):
            return_code = shellutil.run("ip link set {0} down && ip link set {0} up".format(ifname))
            if return_code == 0:
                return
            logger.warn("failed to restart {0}: return code {1}".format(ifname, return_code))
            if attempt < retry_limit:
                logger.info("retrying to restart {0} in {1} seconds".format(ifname, wait))
                time.sleep(wait)
            else:
                logger.warn("exceeded restart retries for {0}".format(ifname))

    def restart_ssh_service(self):
        shellutil.run('systemctl restart sshd')

    def stop_dhcp_service(self):
        # NetworkManager handles DHCP in OpenMandriva.
        # Stopping it is not usually a good idea.
        pass

    def start_dhcp_service(self):
        # NetworkManager handles DHCP in OpenMandriva.
        # Stopping it is not usually a good idea.
        pass

    def start_agent_service(self):
        return shellutil.run("systemctl start {0}".format(self.service_name), chk_err=False)

    def stop_agent_service(self):
        return shellutil.run("systemctl stop {0}".format(self.service_name), chk_err=False)

    def get_dhcp_pid(self):
        return self._get_dhcp_pid(["pidof", "NetworkManager"])

    def conf_sshd(self, disable_password):
        # We prefer the system sshd conf
        pass
