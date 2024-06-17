from django.db import models
from django.utils.translation import gettext_lazy as _


class Scope(models.TextChoices):
    system = 'system', _('System')
    org = 'org', _('Organization')


exclude_permissions = (
    # ('App', 'Model', 'Action', 'Resource') Model 和 Resource 可能不同
    # users.add_user
    ('auth', '*', '*', '*'),
    ('captcha', '*', '*', '*'),
    ('contenttypes', '*', '*', '*'),
    ('django_cas_ng', '*', '*', '*'),
    ('django_celery_beat', '*', '*', '*'),
    ('jms_oidc_rp', '*', '*', '*'),
    ('admin', '*', '*', '*'),
    ('sessions', '*', '*', '*'),
    ('notifications', '*', '*', '*'),
    ('common', 'setting', '*', '*'),

    ('authentication', 'privatetoken', '*', '*'),
    ('authentication', 'connectiontoken', 'delete,change', 'connectiontoken'),
    ('authentication', 'connectiontoken', 'view', 'connectiontokensecret'),
    ('authentication', 'ssotoken', '*', '*'),
    ('authentication', 'superconnectiontoken', 'change,delete', 'superconnectiontoken'),
    ('authentication', 'temptoken', 'delete', 'temptoken'),
    ('users', 'userpasswordhistory', '*', '*'),
    ('users', 'usersession', '*', '*'),
    ('assets', 'adminuser', '*', '*'),
    ('assets', 'label', '*', '*'),
    ('assets', 'assetgroup', '*', '*'),
    ('assets', 'cluster', '*', '*'),
    ('assets', 'systemuser', '*', '*'),
    ('assets', 'favoriteasset', '*', '*'),
    ('assets', 'assetuser', '*', '*'),
    ('assets', 'web', '*', '*'),
    ('assets', 'host', '*', '*'),
    ('assets', 'cloud', '*', '*'),
    ('assets', 'device', '*', '*'),
    ('assets', 'database', '*', '*'),
    ('assets', 'protocol', '*', '*'),
    ('assets', 'baseautomation', '*', '*'),
    ('assets', 'assetbaseautomation', '*', '*'),
    ('assets', 'automationexecution', '*', '*'),
    ('assets', 'pingautomation', '*', '*'),
    ('assets', 'platformprotocol', '*', '*'),
    ('assets', 'platformautomation', '*', '*'),
    ('assets', 'verifyaccountautomation', '*', '*'),
    ('assets', 'gatherfactsautomation', '*', '*'),
    ('assets', 'commandfilter', '*', '*'),
    ('assets', 'commandfilterrule', '*', '*'),
    ('assets', 'asset', 'add,move', 'assettonode'),
    ('assets', 'asset', 'remove', 'assetfromnode'),
    ('assets', 'asset', 'test', 'account'),
    ('assets', 'asset', 'push', 'assetaccount'),

    ('accounts', 'historicalaccount', '*', '*'),
    ('accounts', 'accountbaseautomation', '*', '*'),
    ('accounts', 'verifyaccountautomation', '*', '*'),
    ('accounts', 'automationexecution', '*', 'automationexecution'),
    ('accounts', 'accountbackupexecution', 'delete,change', 'accountbackupexecution'),
    ('accounts', 'changesecretrecord', 'add,delete,change', 'changesecretrecord'),
    ('accounts', 'account', 'change', 'accountsecret'),
    ('accounts', 'account', 'view', 'historyaccount'),
    ('accounts', 'account', 'view', 'historyaccountsecret'),

    ('perms', 'userassetgrantedtreenoderelation', '*', '*'),
    ('perms', 'permedaccount', '*', '*'),
    ('perms', 'permedasset', 'view', 'usergroupassets'),
    ('perms', 'usergrantedmappingnode', '*', '*'),
    ('perms', 'permnode', '*', '*'),
    ('perms', 'rebuildusertreetask', '*', '*'),
    ('perms', 'permedasset', '*', 'permedasset'),
    ('perms', 'permedapplication', 'add,change,delete', 'permedapplication'),
    ('rbac', 'contenttype', 'add,change,delete', '*'),
    ('rbac', 'permission', 'add,delete,change', 'permission'),
    ('rbac', 'rolebinding', '*', '*'),
    ('rbac', 'systemrolebinding', 'change', 'systemrolebinding'),
    ('rbac', 'orgrolebinding', 'change', 'orgrolebinding'),
    ('rbac', 'menupermission', '*', 'menupermission'),
    ('ops', 'adhocexecution', 'view,add,delete,change', '*'),
    ('ops', 'jobexecution', 'change,delete', 'jobexecution'),
    ('ops', 'historicaljob', '*', '*'),
    ('ops', 'celerytask', 'add,change,delete', 'celerytask'),
    ('ops', 'celerytaskexecution', 'add,change,delete', 'celerytaskexecution'),
    ('orgs', 'organizationmember', '*', '*'),
    ('settings', 'setting', 'add,change,delete', 'setting'),
    ('audits', 'joblog', 'add,delete,change', '*'),
    ('audits', 'operatelog', 'add,delete,change', 'operatelog'),
    ('audits', 'activitylog', 'add,delete,change', 'activitylog'),
    ('audits', 'passwordchangelog', 'add,change,delete', 'passwordchangelog'),
    ('audits', 'userloginlog', 'add,change,delete,change', 'userloginlog'),
    ('audits', 'usersession', 'add,delete,change', 'usersession'),
    ('audits', 'ftplog', 'delete', 'ftplog'),
    ('tickets', 'ticketassignee', '*', 'ticketassignee'),
    ('tickets', 'ticketflow', 'add,delete', 'ticketflow'),
    ('tickets', 'comment', '*', '*'),
    ('tickets', 'ticket', 'add,delete,change', 'ticket'),
    ('tickets', 'ticketstep', '*', '*'),
    ('tickets', 'approvalrule', '*', '*'),
    ('tickets', 'applyloginticket', '*', '*'),
    ('tickets', 'applyloginassetticket', '*', '*'),
    ('tickets', 'applycommandticket', '*', '*'),
    ('tickets', 'applyassetticket', '*', '*'),
    ('tickets', 'applyapplicationticket', '*', '*'),
    ('tickets', 'superticket', 'delete', 'superticket'),
    ('tickets', 'ticketsession', 'view,delete', 'ticketsession'),
    ('xpack', 'interface', '*', '*'),
    ('xpack', 'license', '*', '*'),
    ('xpack', 'syncinstancedetail', 'add,delete,change', 'syncinstancedetail'),
    ('xpack', 'syncinstancetaskexecution', 'delete,change', 'syncinstancetaskexecution'),
    ('common', 'permission', 'add,delete,view,change', 'permission'),
    ('terminal', 'command', 'delete,change', 'command'),
    ('terminal', 'status', 'delete,change', 'status'),
    ('terminal', 'task', 'add,delete', 'task'),
    ('terminal', 'sessionjoinrecord', 'delete', 'sessionjoinrecord'),
    ('terminal', 'sessionreplay', 'add,change,delete', 'sessionreplay'),
    ('terminal', 'sessionsharing', 'view,add,change,delete', 'sessionsharing'),
    ('terminal', 'session', 'delete,share', 'session'),
    ('terminal', 'session', 'delete,change', 'command'),
    ('applications', '*', '*', '*'),
    ('settings', 'chatprompt', 'add,delete,change', 'chatprompt'),
)

only_system_permissions = (
    ('assets', 'platform', 'add,change,delete', 'platform'),
    ('users', 'user', 'delete', 'user'),
    ('rbac', 'role', 'delete,add,change', 'role'),
    ('rbac', 'systemrole', '*', '*'),
    ('rbac', 'rolebinding', '*', '*'),
    ('rbac', 'systemrolebinding', '*', '*'),
    ('rbac', 'orgrole', 'delete,add,change', 'orgrole'),
    ('orgs', 'organization', '*', '*'),
    ('xpack', 'license', '*', '*'),
    ('settings', 'setting', '*', '*'),
    ('tickets', '*', '*', '*'),
    ('ops', 'celerytask', 'view', 'taskmonitor'),
    ('terminal', 'terminal', '*', '*'),
    ('terminal', 'commandstorage', '*', '*'),
    ('terminal', 'replaystorage', '*', '*'),
    ('terminal', 'status', '*', '*'),
    ('terminal', 'task', '*', '*'),
    ('terminal', 'endpoint', '*', '*'),
    ('terminal', 'endpointrule', '*', '*'),
    ('authentication', 'accesskey', '*', '*'),
    ('authentication', 'superconnectiontoken', '*', '*'),
    ('authentication', 'temptoken', '*', '*'),
    ('authentication', 'passkey', '*', '*'),
    ('tickets', '*', '*', '*'),
    ('orgs', 'organization', 'view', 'rootorg'),
    ('terminal', 'applet', '*', '*'),
    ('terminal', 'applethost', '*', '*'),
    ('terminal', 'appletpublication', '*', '*'),
    ('terminal', 'applethostdeployment', '*', '*'),
    ('acls', 'loginacl', '*', '*'),
    ('acls', 'connectmethodacl', '*', '*')
)

only_org_permissions = (
)

system_exclude_permissions = list(exclude_permissions) + list(only_org_permissions)
org_exclude_permissions = list(exclude_permissions) + list(only_system_permissions)
