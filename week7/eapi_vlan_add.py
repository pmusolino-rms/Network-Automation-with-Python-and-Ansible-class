#!/usr/bin/env python
'''
Ansible module to add/modify vlans on Arista switches
'''

from ansible.module_utils.basic import *
import pyeapi
from arista_network_admin import AristaNetworkAdmin, Vlan

def main():
  '''
  Ansible module to add/modify vlans on Arista switches
  '''  
  module = AnsibleModule(
      argument_spec=dict(
          host=dict(required=True),
          port=dict(default=443, required=False),
          username=dict(required=True),
          password=dict(required=True),
          transport=dict(default="https", required=False),
          vlan_name=dict(required=True),
          vlan_id=dict(required=True)
          #vlan_state=dict(default='present',required=False),
      ),
      supports_check_mode=True
  )

  connection=pyeapi.connect(host=module.params['host'],username=module.params['username'],password=module.params['password'], port=module.params['port'],transport=module.params['transport'])
  switch=pyeapi.client.Node(connection)
  network_admin = AristaNetworkAdmin(switch)
  vlan=Vlan(module.params['vlan_id'],module.params['vlan_name'])

  if network_admin.vlan_exists(vlan):
    module.exit_json(msg="vlan exists", changed=False)
  if module.check_mode:
    if network_admin.vlan_exists(vlan):
      module.exit_json(msg="Vlan already exits",changed=False)
    module.exit(msg="Check mode: Vlan would be added or updated with a new name",changed=True)

  status=network_admin.vlan_add(vlan)
  vl=network_admin.vlan_list(vlan)
  if status and vl:
    module.exit_json(msg="Vlan successfully added/modified",changed=True)
  else:
    module.fail_json(msg="Vlan failed to add")

if __name__ == '__main__':
    main()
