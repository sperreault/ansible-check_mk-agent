#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

from ansible.module_utils.basic import AnsibleModule
from urllib2 import HTTPError
import check_mk_web_api

def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        username=dict(type='str', required=True),
        secret=dict(type='str', required=True),
        url=dict(type='str', required=True),
        hostname=dict(type='str', required=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    api = check_mk_web_api.WebApi(  module.params['url'], 
                                    username=module.params['username'], 
                                    secret=module.params['secret'])

    try:
        result['changed']=True
        result['discover_services']=api.discover_services(module.params['hostname'])
        result['message']='Discovered '+ module.params['hostname']
        result['code']=200
    except HTTPError as err:
        result['changed']=False
        result['message']=err.reason
        result['code']=err.code
    except check_mk_web_api.exception.CheckMkWebApiException as err:
        result['changed']=False
        result['message']=str(err)
        result['code']=501

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    if result['code'] == 200:
        module.exit_json(**result)
    elif result['code'] == 301:
        module.exit_json(**result)
    else:
        module.fail_json(msg=result['message'], **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
