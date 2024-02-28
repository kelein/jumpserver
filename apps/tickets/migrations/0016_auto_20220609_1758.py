# Generated by Django 3.1.14 on 2022-06-09 09:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('terminal', '0049_endpoint_redis_port'),
        ('assets', '0090_auto_20220412_1145'),
        ('applications', '0020_auto_20220316_2028'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0015_superticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyLoginTicket',
            fields=[
                ('ticket_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='tickets.ticket')),
                ('apply_login_ip', models.GenericIPAddressField(null=True, verbose_name='Login IP')),
                ('apply_login_city', models.CharField(max_length=64, null=True, verbose_name='Login city')),
                ('apply_login_datetime', models.DateTimeField(null=True, verbose_name='Login Date')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Apply Login Ticket'
            },
            bases=('tickets.ticket',),
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='process_map',
        ),
        migrations.AddField(
            model_name='comment',
            name='state',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='type',
            field=models.CharField(choices=[('state', 'State'), ('common', 'common')], default='common', max_length=16,
                                   verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='rel_snapshot',
            field=models.JSONField(default=dict, verbose_name='Relation snapshot'),
        ),
        migrations.AddField(
            model_name='ticketstep',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('active', 'Active'), ('closed', 'Closed')],
                                   default='pending', max_length=16),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='state',
            field=models.CharField(choices=[('pending', 'Open'), ('approved', 'Approved'), ('rejected', 'Rejected'),
                                            ('closed', 'Cancel'), ('reopen', 'Reopen')], default='pending',
                                   max_length=16, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Finished')], default='open', max_length=16,
                                   verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='ticketassignee',
            name='state',
            field=models.CharField(choices=[('pending', 'Open'), ('approved', 'Approved'), ('rejected', 'Rejected'),
                                            ('closed', 'Cancel'), ('reopen', 'Reopen')], default='pending',
                                   max_length=64),
        ),
        migrations.AlterField(
            model_name='ticketstep',
            name='state',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'),
                                            ('closed', 'Closed'), ('reopen', 'Reopen')], default='pending',
                                   max_length=64, verbose_name='State'),
        ),
        migrations.CreateModel(
            name='ApplyLoginAssetTicket',
            fields=[
                ('ticket_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='tickets.ticket')),
                ('apply_login_asset',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.asset',
                                   verbose_name='Login asset')),
                ('apply_login_system_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.systemuser',
                                   verbose_name='Login system user')),
                ('apply_login_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL,
                                   verbose_name='Login user')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Apply Login Asset Ticket'
            },
            bases=('tickets.ticket',),
        ),
        migrations.CreateModel(
            name='ApplyCommandTicket',
            fields=[
                ('ticket_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='tickets.ticket')),
                ('apply_run_command', models.CharField(max_length=4096, verbose_name='Run command')),
                ('apply_run_asset', models.CharField(max_length=128, verbose_name='Run asset')),
                ('apply_from_cmd_filter',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.commandfilter',
                                   verbose_name='From cmd filter')),
                ('apply_from_cmd_filter_rule',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                   to='assets.commandfilterrule', verbose_name='From cmd filter rule')),
                ('apply_from_session',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='terminal.session',
                                   verbose_name='Session')),
                ('apply_run_system_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.systemuser',
                                   verbose_name='Run system user')),
                ('apply_run_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL,
                                   verbose_name='Run user')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Apply Command Ticket'
            },
            bases=('tickets.ticket',),
        ),
        migrations.CreateModel(
            name='ApplyAssetTicket',
            fields=[
                ('ticket_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='tickets.ticket')),
                ('apply_permission_name', models.CharField(max_length=128, verbose_name='Permission name')),
                ('apply_actions', models.IntegerField(
                    choices=[(255, 'All'), (1, 'Connect'), (2, 'Upload file'), (4, 'Download file'),
                             (6, 'Upload download'), (8, 'Clipboard copy'), (16, 'Clipboard paste'),
                             (24, 'Clipboard copy paste')], default=255, verbose_name='Actions')),
                ('apply_date_start', models.DateTimeField(null=True, verbose_name='Date start')),
                ('apply_date_expired', models.DateTimeField(null=True, verbose_name='Date expired')),
                ('apply_assets', models.ManyToManyField(to='assets.Asset', verbose_name='Apply assets')),
                ('apply_nodes', models.ManyToManyField(to='assets.Node', verbose_name='Apply nodes')),
                ('apply_system_users',
                 models.ManyToManyField(to='assets.SystemUser', verbose_name='Apply system users')),
            ],
            options={
                'abstract': False,
            },
            bases=('tickets.ticket',),
        ),
        migrations.CreateModel(
            name='ApplyApplicationTicket',
            fields=[
                ('ticket_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='tickets.ticket')),
                ('apply_permission_name', models.CharField(max_length=128, verbose_name='Permission name')),
                ('apply_category',
                 models.CharField(choices=[('db', 'Database'), ('remote_app', 'Remote app'), ('cloud', 'Cloud')],
                                  max_length=16, verbose_name='Category')),
                ('apply_type', models.CharField(
                    choices=[('mysql', 'MySQL'), ('mariadb', 'MariaDB'), ('oracle', 'Oracle'),
                             ('postgresql', 'PostgreSQL'), ('sqlserver', 'SQLServer'), ('redis', 'Redis'),
                             ('mongodb', 'MongoDB'), ('chrome', 'Chrome'), ('mysql_workbench', 'MySQL Workbench'),
                             ('vmware_client', 'vSphere Client'), ('custom', 'Custom'), ('k8s', 'Kubernetes')],
                    max_length=16, verbose_name='Type')),
                ('apply_date_start', models.DateTimeField(null=True, verbose_name='Date start')),
                ('apply_date_expired', models.DateTimeField(null=True, verbose_name='Date expired')),
                ('apply_applications',
                 models.ManyToManyField(to='applications.Application', verbose_name='Apply applications')),
                ('apply_system_users',
                 models.ManyToManyField(to='assets.SystemUser', verbose_name='Apply system users')),
            ],
            options={
                'abstract': False,
            },
            bases=('tickets.ticket',),
        ),
    ]
