from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from assets.models import Asset
from assets.models.base import AbsConnectivity
from common.utils import lazyproperty, get_logger
from labels.mixins import LabeledMixin
from .base import BaseAccount
from .mixins import VaultModelMixin
from ..const import Source

logger = get_logger(__file__)

__all__ = ['Account', 'AccountHistoricalRecords']


class AccountHistoricalRecords(HistoricalRecords):
    def __init__(self, *args, **kwargs):
        self.updated_version = None
        self.included_fields = kwargs.pop('included_fields', None)
        super().__init__(*args, **kwargs)

    def post_save(self, instance, created, using=None, **kwargs):
        if not self.included_fields:
            return super().post_save(instance, created, using=using, **kwargs)

        # self.updated_version = 0
        if created:
            return super().post_save(instance, created, using=using, **kwargs)

        history_account = instance.history.first()
        if history_account is None:
            return super().post_save(instance, created, using=using, **kwargs)

        check_fields = set(self.included_fields) - {'version'}
        history_attrs = {field: getattr(history_account, field) for field in check_fields}

        attrs = {field: getattr(instance, field) for field in check_fields}
        history_attrs = set(history_attrs.items())
        attrs = set(attrs.items())
        diff = attrs - history_attrs
        if not diff:
            return
        self.updated_version = history_account.version + 1
        instance.version = self.updated_version
        return super().post_save(instance, created, using=using, **kwargs)

    def create_historical_record(self, instance, history_type, using=None):
        super().create_historical_record(instance, history_type, using=using)
        # Ignore deletion history_type: -
        if self.updated_version is not None and history_type != '-':
            instance.save(update_fields=['version'])

    def create_history_model(self, model, inherited):
        if self.included_fields and not self.excluded_fields:
            self.excluded_fields = [
                field.name for field in model._meta.fields
                if field.name not in self.included_fields
            ]
        return super().create_history_model(model, inherited)


class JSONFilterMixin:
    @staticmethod
    def get_json_filter_attr_q(name, value, match):
        if name == "asset":
            if match == "m2m_all":
                asset_id = (
                    Asset.objects.filter(id__in=value)
                    .annotate(count=models.Count("id"))
                    .filter(count=len(value))
                    .values_list("id", flat=True)
                )
            else:
                asset_id = Asset.objects.filter(id__in=value).values_list("id", flat=True)
            return models.Q(asset_id__in=asset_id)
        return None


class Account(AbsConnectivity, LabeledMixin, BaseAccount, JSONFilterMixin):
    asset = models.ForeignKey(
        'assets.Asset', related_name='accounts',
        on_delete=models.CASCADE, verbose_name=_('Asset')
    )
    su_from = models.ForeignKey(
        'accounts.Account', related_name='su_to', null=True,
        on_delete=models.SET_NULL, verbose_name=_("Su from")
    )
    version = models.IntegerField(default=0, verbose_name=_('Version'))
    history = AccountHistoricalRecords(
        included_fields=['id', '_secret', 'secret_type', 'version'],
        verbose_name=_("historical Account")
    )
    secret_reset = models.BooleanField(default=True, verbose_name=_('Secret reset'))
    source = models.CharField(max_length=30, default=Source.LOCAL, verbose_name=_('Source'))
    source_id = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Source ID'))
    date_last_login = models.DateTimeField(null=True, blank=True, verbose_name=_('Date last access'))
    login_by = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Access by'))
    date_change_secret = models.DateTimeField(null=True, blank=True, verbose_name=_('Date change secret'))
    change_secret_status = models.CharField(
        max_length=16, null=True, blank=True, verbose_name=_('Change secret status')
    )

    class Meta:
        verbose_name = _('Account')
        unique_together = [
            ('username', 'asset', 'secret_type'),
            ('name', 'asset'),
        ]
        permissions = [
            ('view_accountsecret', _('Can view asset account secret')),
            ('view_historyaccount', _('Can view asset history account')),
            ('view_historyaccountsecret', _('Can view asset history account secret')),
            ('verify_account', _('Can verify account')),
            ('push_account', _('Can push account')),
            ('remove_account', _('Can remove account')),
        ]

    def __str__(self):
        if self.asset_id:
            host = self.asset.name
        else:
            host = 'Dynamic'
        return '{}({})'.format(self.name, host)

    @lazyproperty
    def platform(self):
        return self.asset.platform

    @lazyproperty
    def alias(self):
        """
        别称，因为有虚拟账号，@INPUT @MANUAL @USER, 否则为 id
        """
        if self.username.startswith('@'):
            return self.username
        return str(self.id)

    def is_virtual(self):
        """
        不要用 username 去判断，因为可能是构造的 account 对象，设置了同名账号的用户名,
        """
        return self.alias.startswith('@')

    def is_ds_account(self):
        if self.is_virtual():
            return ''
        if not self.asset.is_directory_service:
            return False
        return True

    @lazyproperty
    def ds(self):
        if not self.is_ds_account():
            return None
        return self.asset.ds

    @lazyproperty
    def ds_domain(self):
        """这个不能去掉，perm_account 会动态设置这个值，以更改 full_username"""
        if self.is_virtual():
            return ''
        if self.ds and self.ds.domain_name:
            return self.ds.domain_name
        return ''

    def username_has_domain(self):
        return '@' in self.username or '\\' in self.username

    @property
    def full_username(self):
        if not self.username_has_domain() and self.ds_domain:
            return '{}@{}'.format(self.username, self.ds_domain)
        return self.username

    @lazyproperty
    def has_secret(self):
        return bool(self.secret)

    @lazyproperty
    def versions(self):
        return self.history.count()

    def get_su_from_accounts(self):
        """ 排除自己和以自己为 su-from 的账号 """
        return self.asset.accounts.exclude(id=self.id).exclude(su_from=self)

    def make_account_ansible_vars(self, su_from):
        var = {
            'ansible_user': su_from.username,
        }
        if not su_from.secret:
            return var
        var['ansible_password'] = self.escape_jinja2_syntax(su_from.secret)
        var['ansible_ssh_private_key_file'] = su_from.private_key_path
        return var

    def get_ansible_become_auth(self):
        su_from = self.su_from
        platform = self.platform
        auth = {'ansible_become': False}
        if not (platform.su_enabled and su_from):
            return auth

        auth.update(self.make_account_ansible_vars(su_from))

        become_method = platform.ansible_become_method
        password = su_from.secret if become_method == 'sudo' else self.secret
        auth['ansible_become'] = True
        auth['ansible_become_method'] = become_method
        auth['ansible_become_user'] = self.username
        auth['ansible_become_password'] = self.escape_jinja2_syntax(password)
        return auth

    @staticmethod
    def escape_jinja2_syntax(value):
        if not isinstance(value, str):
            return value

        def escape(v):
            v = v.replace('{{', '__TEMP_OPEN_BRACES__') \
                .replace('}}', '__TEMP_CLOSE_BRACES__')

            v = v.replace('__TEMP_OPEN_BRACES__', '{{ "{{" }}') \
                .replace('__TEMP_CLOSE_BRACES__', '{{ "}}" }}')

            return v.replace('{%', '{{ "{%" }}').replace('%}', '{{ "%}" }}')

        return escape(value)

    def update_last_login_date(self):
        self.date_last_login = timezone.now()
        self.save(update_fields=['date_last_login'])


def replace_history_model_with_mixin():
    """
    替换历史模型中的父类为指定的Mixin类。

    Parameters:
        model (class): 历史模型类，例如 Account.history.model
        mixin_class (class): 要替换为的Mixin类

    Returns:
        None
    """
    model = Account.history.model
    model.__bases__ = (VaultModelMixin,) + model.__bases__


replace_history_model_with_mixin()
