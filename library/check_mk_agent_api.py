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
        action=dict(type='str', required=True),
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

    api = check_mk_web_api.WebApi(module.params['url'], username=module.params['username'], secret=module.params['secret'])

    if module.params['action'] == 'get_host':
        result=get_host(api, module.params['hostname'], result)
        
    elif module.params['action'] == 'add_host':
        result=add_host(api, module.params['hostname'], result)

    elif module.params['action'] == 'discover_services':
        result=discover_services(api, module.params['hostname'], result)

    elif module.params['action'] == 'activate_changes':
        result=activate_changes(api, module.params['hostname'], result)
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result
    

    if result['code'] == 200:
        module.exit_json(**result)
    elif result['code'] == 301:
        module.exit_json(**result)
    elif result['code'] == 404 and module.params['action'] == 'get_host':
        result['changed'] = False
        module.exit_json(**result)
    else:
        module.fail_json(msg=result['message'], **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()


def get_host(api, hostname, res):
    try:
        res['changed']=True
        res['get_host']=api.get_host(hostname)
        res['message']='Host informations for '+hostname
        res['code'] = 200
    except HTTPError as err:
        res['changed']=False
        res['message']=err.reason
        res['code']=err.code
    except check_mk_web_api.exception.CheckMkWebApiException as err:
        res['changed']=False
        res['message']=str(err)
        res['code']=404
    finally:
        return res

def add_host(api, hostname, res):
    try:
        res['changed']=True
        api.add_host(hostname)
        res['message']='Added '+hostname
        res['code']=200
    except HTTPError as err:
        res['changed']=False
        res['message']=err.reason
        res['code']=err.code
    except check_mk_web_api.exception.CheckMkWebApiException as err:
        res['changed']=False
        res['message']=str(err)
        if "exists" in res['message']:
            res['code']=409
        else:
            res['code']=501
    finally:
        return res   

def discover_services(api, hostname, res):
    try:
        res['changed']=True
        res['discover_services']=api.discover_services(hostname)
        res['message']='Discovered '+hostname
        res['code']=200
    except HTTPError as err:
        res['changed']=False
        res['message']=err.reason
        res['code']=err.code
    except check_mk_web_api.exception.CheckMkWebApiException as err:
        res['changed']=False
        res['message']=str(err)
        res['code']=501

    finally:
        return res

def activate_changes(api, hostname, res):
    try:
        res['changed']=True
        res['activate_changes']=api.activate_changes()
        res['message']='Activated changes'
        res['code']=200
    except HTTPError as err:
        res['changed']=False
        res['message']=err.reason
        res['code']=err.code
    except check_mk_web_api.exception.CheckMkWebApiException as err:
        res['changed']=False
        res['message']=str(err)
        if "no changes" in res['message']:
            res['code']=301
        else:
            res['code']=501

    finally:
        return res

if __name__ == '__main__':
    main()
if __name__ == '__main__':
    main()

