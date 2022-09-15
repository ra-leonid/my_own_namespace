#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This module creates a context file on the node

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "2.5.0"

description: A text file with the specified name is created on the node and filled with the passed context.

options:
    path:
        description: Full text file name.
        required: true
        type: str
    context:
        description: The contents of the text file.
        required: false
        type: str
        default: Empty string
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_own_namespace.yandex_cloud_elk.my_own_module

author:
    - L. Rastorguev (@ra-leonid)
'''

EXAMPLES = r'''
# Pass in a message
- name: Creating a text file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: test.txt
    content: Hello World
'''

RETURN = r'''
none
'''

from ansible.module_utils.basic import AnsibleModule
import os.path


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False, default='')
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    file_name = module.params['path']
    content = module.params['content']

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    try:
        if os.path.isfile(file_name):
            read_file = open(file_name)
            original_content = read_file.read()
            read_file.close()
            if original_content == content:
                module.exit_json(**result)

        result_file = open(file_name, 'w')
        result_file.write(content)
        result_file.close()

        result['changed'] = True

    except IOError:
        module.fail_json(msg=IOError.strerror, **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()