import requests
import json
import os

managed_policies = json.loads(requests.get('https://raw.githubusercontent.com/iann0036/iam-dataset/main/managed_policies.json').text)
privesc_policies = []
deprecated_policies = []

for policy in managed_policies['policies']:
    if policy['privesc']:
        privesc_policies.append(policy['name'])
    if policy['deprecated']:
        deprecated_policies.append(policy['name'])

privesc_policies_str = '\'' + '\',\''.join(privesc_policies) + '\'' if len(privesc_policies) > 0 else ''
deprecated_policies_str = '\'' + '\',\''.join(deprecated_policies) + '\'' if len(deprecated_policies) > 0 else ''

out = """let iam_roles = Resources.*[ Type == 'AWS::IAM::Role' ]
let iam_users = Resources.*[ Type == 'AWS::IAM::User' ]
let iam_groups = Resources.*[ Type == 'AWS::IAM::Group' ]

rule IAM_Role_Policies when %iam_roles !empty {{
    when %iam_roles.Properties.Policies exists {{
        %iam_roles.Properties.Policies is_list
        !%iam_roles.Properties.Policies[*] IN [{privesc}] <<Managed IAM Policy has possible privilege escalation>>
        !%iam_roles.Properties.Policies[*] IN [{deprecated}] <<Deprecated Managed IAM Policy in use>>
    }}
}}

rule IAM_User_Policies when %iam_users !empty {{
    when %iam_users.Properties.Policies exists {{
        %iam_users.Properties.Policies is_list
        !%iam_users.Properties.Policies[*] IN [{privesc}] <<Managed IAM Policy has possible privilege escalation>>
        !%iam_users.Properties.Policies[*] IN [{deprecated}] <<Deprecated Managed IAM Policy in use>>
    }}
}}

rule IAM_Group_Policies when %iam_groups !empty {{
    when %iam_groups.Properties.Policies exists {{
        %iam_groups.Properties.Policies is_list
        !%iam_groups.Properties.Policies[*] IN [{privesc}] <<Managed IAM Policy has possible privilege escalation>>
        !%iam_groups.Properties.Policies[*] IN [{deprecated}] <<Deprecated Managed IAM Policy in use>>
    }}
}}
""".format(privesc=privesc_policies_str, deprecated=deprecated_policies_str)

with open(os.path.dirname(os.path.realpath(__file__)) + '/../rules/iam-managed-policies.guard', 'w') as f:
    f.write(out)
