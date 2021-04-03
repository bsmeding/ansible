#!/usr/bin/python
#
# @author: Gaurav Rastogi (grastogi@avinetworks.com)
#          Eric Anderson (eanderson@avinetworks.com)
# module_check: supported
# Avi Version: 17.1.1
#
# Copyright: (c) 2017 Gaurav Rastogi, <grastogi@avinetworks.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: avi_sslkeyandcertificate
author: Gaurav Rastogi (@grastogi23) <grastogi@avinetworks.com>

short_description: Module for setup of SSLKeyAndCertificate Avi RESTful Object
description:
    - This module is used to configure SSLKeyAndCertificate object
    - more examples at U(https://github.com/avinetworks/devops)
requirements: [ avisdk ]
version_added: "2.3"
options:
    state:
        description:
            - The state that should be applied on the entity.
        default: present
        choices: ["absent", "present"]
    avi_api_update_method:
        description:
            - Default method for object update is HTTP PUT.
            - Setting to patch will override that behavior to use HTTP PATCH.
        version_added: "2.5"
        default: put
        choices: ["put", "patch"]
    avi_api_patch_op:
        description:
            - Patch operation to use when using avi_api_update_method as patch.
        version_added: "2.5"
        choices: ["add", "replace", "delete"]
    ca_certs:
        description:
            - Ca certificates in certificate chain.
    certificate:
        description:
            - Sslcertificate settings for sslkeyandcertificate.
        required: true
    certificate_base64:
        description:
            - States if the certificate is base64 encoded.
            - Field introduced in 18.1.2, 18.2.1.
            - Default value when not specified in API or module is interpreted by Avi Controller as False.
        version_added: "2.9"
        type: bool
    certificate_management_profile_ref:
        description:
            - It is a reference to an object of type certificatemanagementprofile.
    created_by:
        description:
            - Creator name.
    dynamic_params:
        description:
            - Dynamic parameters needed for certificate management profile.
    enckey_base64:
        description:
            - Encrypted private key corresponding to the private key (e.g.
            - Those generated by an hsm such as thales nshield).
    enckey_name:
        description:
            - Name of the encrypted private key (e.g.
            - Those generated by an hsm such as thales nshield).
    format:
        description:
            - Format of the key/certificate file.
            - Enum options - SSL_PEM, SSL_PKCS12.
            - Field introduced in 18.1.2, 18.2.1.
            - Default value when not specified in API or module is interpreted by Avi Controller as SSL_PEM.
        version_added: "2.9"
    hardwaresecuritymodulegroup_ref:
        description:
            - It is a reference to an object of type hardwaresecuritymodulegroup.
    key:
        description:
            - Private key.
    key_base64:
        description:
            - States if the private key is base64 encoded.
            - Field introduced in 18.1.2, 18.2.1.
            - Default value when not specified in API or module is interpreted by Avi Controller as False.
        version_added: "2.9"
        type: bool
    key_params:
        description:
            - Sslkeyparams settings for sslkeyandcertificate.
    key_passphrase:
        description:
            - Passphrase used to encrypt the private key.
            - Field introduced in 18.1.2, 18.2.1.
        version_added: "2.9"
    name:
        description:
            - Name of the object.
        required: true
    status:
        description:
            - Enum options - ssl_certificate_finished, ssl_certificate_pending.
            - Default value when not specified in API or module is interpreted by Avi Controller as SSL_CERTIFICATE_FINISHED.
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
    type:
        description:
            - Enum options - ssl_certificate_type_virtualservice, ssl_certificate_type_system, ssl_certificate_type_ca.
    url:
        description:
            - Avi controller URL of the object.
    uuid:
        description:
            - Unique object identifier of the object.
extends_documentation_fragment:
    - avi
'''

EXAMPLES = """
- name: Create a SSL Key and Certificate
  avi_sslkeyandcertificate:
    controller: 10.10.27.90
    username: admin
    password: AviNetworks123!
    key: |
        -----BEGIN PRIVATE KEY-----
        ....
        -----END PRIVATE KEY-----
    certificate:
        self_signed: true
        certificate: |
          -----BEGIN CERTIFICATE-----
          ....
          -----END CERTIFICATE-----
    type: SSL_CERTIFICATE_TYPE_VIRTUALSERVICE
    name: MyTestCert
"""

RETURN = '''
obj:
    description: SSLKeyAndCertificate (api/sslkeyandcertificate) object
    returned: success, changed
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from ansible.module_utils.network.avi.avi import (
        avi_common_argument_spec, avi_ansible_api, HAS_AVI)
except ImportError:
    HAS_AVI = False


def main():
    argument_specs = dict(
        state=dict(default='present',
                   choices=['absent', 'present']),
        avi_api_update_method=dict(default='put',
                                   choices=['put', 'patch']),
        avi_api_patch_op=dict(choices=['add', 'replace', 'delete']),
        ca_certs=dict(type='list',),
        certificate=dict(type='dict', required=True),
        certificate_base64=dict(type='bool',),
        certificate_management_profile_ref=dict(type='str',),
        created_by=dict(type='str',),
        dynamic_params=dict(type='list',),
        enckey_base64=dict(type='str', no_log=True),
        enckey_name=dict(type='str',),
        format=dict(type='str',),
        hardwaresecuritymodulegroup_ref=dict(type='str',),
        key=dict(type='str', no_log=True,),
        key_base64=dict(type='bool',),
        key_params=dict(type='dict',),
        key_passphrase=dict(type='str', no_log=True,),
        name=dict(type='str', required=True),
        status=dict(type='str',),
        tenant_ref=dict(type='str',),
        type=dict(type='str',),
        url=dict(type='str',),
        uuid=dict(type='str',),
    )
    argument_specs.update(avi_common_argument_spec())
    module = AnsibleModule(
        argument_spec=argument_specs, supports_check_mode=True)
    if not HAS_AVI:
        return module.fail_json(msg=(
            'Avi python API SDK (avisdk>=17.1) or requests is not installed. '
            'For more details visit https://github.com/avinetworks/sdk.'))
    return avi_ansible_api(module, 'sslkeyandcertificate',
                           set(['key_passphrase', 'key']))


if __name__ == '__main__':
    main()
