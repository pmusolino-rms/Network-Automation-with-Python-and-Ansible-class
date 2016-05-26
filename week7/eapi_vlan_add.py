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

  with open("/tmp/eapi.log","w+") as f:
    if network_admin.vlan_exists(vlan):
      f.write("Exists: " + str(network_admin.vlan_exists(vlan)) + "\n")
      f.write("DEBUG: vlan %s with id %s exists \n" %(vlan.name,vlan.vlan_id))
      module.exit_json(msg="vlan exists", changed=False)
    else:
      f.write("DEBUG: vlan %s with id %s does not exist or has a different name \n" %(vlan.name,vlan.vlan_id))

    if module.check_mode:
      if network_admin.vlan_exists(vlan):
        f.write("Check Mode: Vlan already exists\n")
        module.exit_json(msg="Vlan already exits",changed=False)
      module.exit(msg="Check mode: Vlan would be added or updated with a new name",changed=True)
    
    f.write("Attempting add\n")
    status=network_admin.vlan_add(vlan)
    f.write("Add complete with result %s\n" %(str(status)))
    vl=network_admin.vlan_list(vlan)
    if status and vl:
      f.write("Vlan changed\n")
      module.exit_json(msg="Vlan successfully added/modified",changed=True)
    else:
      f.write("failed to add vlan\n")
      module.fail_json(msg="Vlan failed to add")

if __name__ == '__main__':
    main()
