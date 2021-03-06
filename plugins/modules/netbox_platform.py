#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: netbox_platform
short_description: Create or delete platforms within Netbox
description:
  - Creates or removes platforms from Netbox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
requirements:
  - pynetbox
version_added: '0.1.0'
options:
  netbox_url:
    description:
      - URL of the Netbox instance resolvable by Ansible control host
    required: true
  netbox_token:
    description:
      - The token created within Netbox to authorize API access
    required: true
  data:
    description:
      - Defines the platform configuration
    suboptions:
      name:
        description:
          - The name of the platform
        required: true
      manufacturer:
        description:
          - The manufacturer the platform will be tied to
      napalm_driver:
        description:
          - The name of the NAPALM driver to be used when using the NAPALM plugin
      napalm_args:
        description:
          - The optional arguments used for NAPALM connections
        type: dict
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: 'yes'
    type: bool
"""

EXAMPLES = r"""
- name: "Test Netbox modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create platform within Netbox with only required information
      netbox_platform:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test Platform
        state: present

    - name: Create platform within Netbox with only required information
      netbox_platform:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test Platform All
          manufacturer: Test Manufacturer
          napalm_driver: ios
          napalm_args:
            global_delay_factor: 2
        state: present

    - name: Delete platform within netbox
      netbox_platform:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test Platform
        state: absent
"""

RETURN = r"""
platform:
  description: Serialized object as created or already existent within Netbox
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.fragmentedpacket.netbox_modules.plugins.module_utils.netbox_utils import (
    NetboxAnsibleModule,
)
from ansible_collections.fragmentedpacket.netbox_modules.plugins.module_utils.netbox_dcim import (
    NetboxDcimModule,
    NB_PLATFORMS,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = dict(
        netbox_url=dict(type="str", required=True),
        netbox_token=dict(type="str", required=True, no_log=True),
        data=dict(type="dict", required=True),
        state=dict(required=False, default="present", choices=["present", "absent"]),
        validate_certs=dict(type="bool", default=True),
    )
    required_if = [("state", "present", ["name"]), ("state", "absent", ["name"])]

    module = NetboxAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    netbox_platform = NetboxDcimModule(module, NB_PLATFORMS)
    netbox_platform.run()


if __name__ == "__main__":
    main()
