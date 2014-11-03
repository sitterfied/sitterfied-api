# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import pyuploadcare.dj.models
import model_utils.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', models.CharField(default=b'Trial', max_length=10, choices=[(b'Trial', b'Trial'), (b'paid', b'paid')])),
                ('membership_exp_date', models.DateTimeField(null=True)),
                ('facebook_token', models.CharField(max_length=256, null=True, blank=True)),
                ('facebook_id', models.IntegerField(unique=True, null=True, blank=True)),
                ('google_imported', models.BooleanField(default=False)),
                ('address1', models.CharField(max_length=255, blank=True)),
                ('address2', models.CharField(default=b'', max_length=255, blank=True)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('state', models.CharField(default=b'AL', max_length=2, blank=True, choices=[(b'AL', b'AL'), (b'AK', b'AK'), (b'AZ', b'AZ'), (b'AR', b'AR'), (b'CA', b'CA'), (b'CO', b'CO'), (b'CT', b'CT'), (b'DE', b'DE'), (b'DC', b'DC'), (b'FL', b'FL'), (b'GA', b'GA'), (b'HI', b'HI'), (b'ID', b'ID'), (b'IL', b'IL'), (b'IN', b'IN'), (b'IA', b'IA'), (b'KS', b'KS'), (b'KY', b'KY'), (b'LA', b'LA'), (b'ME', b'ME'), (b'MD', b'MD'), (b'MA', b'MA'), (b'MI', b'MI'), (b'MN', b'MN'), (b'MS', b'MS'), (b'MO', b'MO'), (b'MT', b'MT'), (b'NE', b'NE'), (b'NV', b'NV'), (b'NH', b'NH'), (b'NJ', b'NJ'), (b'NM', b'NM'), (b'NY', b'NY'), (b'NC', b'NC'), (b'ND', b'ND'), (b'OH', b'OH'), (b'OK', b'OK'), (b'OR', b'OR'), (b'PA', b'PA'), (b'RI', b'RI'), (b'SC', b'SC'), (b'SD', b'SD'), (b'TN', b'TN'), (b'TX', b'TX'), (b'UT', b'UT'), (b'VT', b'VT'), (b'VA', b'VA'), (b'WA', b'WA'), (b'WV', b'WV'), (b'WI', b'WI'), (b'WY', b'WY')])),
                ('zip', models.CharField(max_length=9, blank=True)),
                ('timezone', models.CharField(max_length=255, blank=True)),
                ('cell', models.CharField(max_length=12, blank=True)),
                ('avatar', pyuploadcare.dj.models.ImageField(blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('notes', models.TextField(blank=True)),
                ('respond_by', models.DateTimeField(null=True, blank=True)),
                ('start_date_time', models.DateTimeField()),
                ('stop_date_time', models.DateTimeField()),
                ('num_children', models.IntegerField(default=1)),
                ('emergency_phone', models.CharField(max_length=12, blank=True)),
                ('address1', models.CharField(max_length=255, blank=True)),
                ('address2', models.CharField(max_length=255, blank=True)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('state', models.CharField(default=b'AL', max_length=2, blank=True, choices=[(b'AL', b'AL'), (b'AK', b'AK'), (b'AZ', b'AZ'), (b'AR', b'AR'), (b'CA', b'CA'), (b'CO', b'CO'), (b'CT', b'CT'), (b'DE', b'DE'), (b'DC', b'DC'), (b'FL', b'FL'), (b'GA', b'GA'), (b'HI', b'HI'), (b'ID', b'ID'), (b'IL', b'IL'), (b'IN', b'IN'), (b'IA', b'IA'), (b'KS', b'KS'), (b'KY', b'KY'), (b'LA', b'LA'), (b'ME', b'ME'), (b'MD', b'MD'), (b'MA', b'MA'), (b'MI', b'MI'), (b'MN', b'MN'), (b'MS', b'MS'), (b'MO', b'MO'), (b'MT', b'MT'), (b'NE', b'NE'), (b'NV', b'NV'), (b'NH', b'NH'), (b'NJ', b'NJ'), (b'NM', b'NM'), (b'NY', b'NY'), (b'NC', b'NC'), (b'ND', b'ND'), (b'OH', b'OH'), (b'OK', b'OK'), (b'OR', b'OR'), (b'PA', b'PA'), (b'RI', b'RI'), (b'SC', b'SC'), (b'SD', b'SD'), (b'TN', b'TN'), (b'TX', b'TX'), (b'UT', b'UT'), (b'VT', b'VT'), (b'VA', b'VA'), (b'WA', b'WA'), (b'WV', b'WV'), (b'WI', b'WI'), (b'WY', b'WY')])),
                ('zip', models.CharField(max_length=9, blank=True)),
                ('rate', models.DecimalField(default=0, max_digits=5, decimal_places=2, blank=True)),
                ('booking_status', models.CharField(default=b'Active', max_length=10, choices=[(b'Active', b'Active'), (b'Pending', b'Pending'), (b'Completed', b'Completed'), (b'Expired', b'Expired'), (b'Declined', b'Declined'), (b'Canceled', b'Canceled')])),
                ('booking_type', models.CharField(default=b'Job', max_length=20, choices=[(b'Job', b'Job'), (b'Interview', b'Interview'), (b'Meetup Interview', b'Meetup Interview'), (b'Phone Interview', b'Phone Interview')])),
                ('overnight', models.BooleanField(default=False)),
                ('canceled', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('certification', models.CharField(unique=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(default=b'', max_length=50, blank=True)),
                ('dob', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('school', models.CharField(default=b'', max_length=50, blank=True)),
            ],
            options={
                'verbose_name_plural': 'children',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IncomingSMSMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('sid', models.CharField(max_length=34)),
                ('date_created', models.DateTimeField()),
                ('date_updated', models.DateTimeField()),
                ('date_sent', models.DateTimeField()),
                ('to', models.CharField(max_length=16)),
                ('body', models.CharField(max_length=161)),
                ('status', models.CharField(max_length=12)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('language', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OtherService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('service', models.CharField(unique=True, max_length=128)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('emergency_contact_one_name', models.CharField(max_length=128, blank=True)),
                ('emergency_contact_one_phone', models.CharField(max_length=10, blank=True)),
                ('emergency_contact_two_name', models.CharField(max_length=128, blank=True)),
                ('emergency_contact_two_phone', models.CharField(max_length=10, blank=True)),
            ],
            options={
                'verbose_name': 'Parent',
            },
            bases=('app.user',),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('phone_type', models.CharField(default=b'cell', max_length=10, choices=[(b'Work', b'Work'), (b'Home', b'Home'), (b'Cell', b'Cell'), (b'Emergency', b'Emergency'), (b'Contact', b'Contact'), (b'Other', b'Other')])),
                ('number', models.CharField(max_length=25)),
                ('primary', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('task_id', models.CharField(max_length=256)),
                ('booking', models.ForeignKey(to='app.Booking')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('mon_early_morning', models.BooleanField(default=True)),
                ('tue_early_morning', models.BooleanField(default=True)),
                ('wed_early_morning', models.BooleanField(default=True)),
                ('thu_early_morning', models.BooleanField(default=True)),
                ('fri_early_morning', models.BooleanField(default=True)),
                ('sat_early_morning', models.BooleanField(default=True)),
                ('sun_early_morning', models.BooleanField(default=True)),
                ('mon_late_morning', models.BooleanField(default=True)),
                ('tue_late_morning', models.BooleanField(default=True)),
                ('wed_late_morning', models.BooleanField(default=True)),
                ('thu_late_morning', models.BooleanField(default=True)),
                ('fri_late_morning', models.BooleanField(default=True)),
                ('sat_late_morning', models.BooleanField(default=True)),
                ('sun_late_morning', models.BooleanField(default=True)),
                ('mon_early_afternoon', models.BooleanField(default=True)),
                ('tue_early_afternoon', models.BooleanField(default=True)),
                ('wed_early_afternoon', models.BooleanField(default=True)),
                ('thu_early_afternoon', models.BooleanField(default=True)),
                ('fri_early_afternoon', models.BooleanField(default=True)),
                ('sat_early_afternoon', models.BooleanField(default=True)),
                ('sun_early_afternoon', models.BooleanField(default=True)),
                ('mon_late_afternoon', models.BooleanField(default=True)),
                ('tue_late_afternoon', models.BooleanField(default=True)),
                ('wed_late_afternoon', models.BooleanField(default=True)),
                ('thu_late_afternoon', models.BooleanField(default=True)),
                ('fri_late_afternoon', models.BooleanField(default=True)),
                ('sat_late_afternoon', models.BooleanField(default=True)),
                ('sun_late_afternoon', models.BooleanField(default=True)),
                ('mon_early_evening', models.BooleanField(default=True)),
                ('tue_early_evening', models.BooleanField(default=True)),
                ('wed_early_evening', models.BooleanField(default=True)),
                ('thu_early_evening', models.BooleanField(default=True)),
                ('fri_early_evening', models.BooleanField(default=True)),
                ('sat_early_evening', models.BooleanField(default=True)),
                ('sun_early_evening', models.BooleanField(default=True)),
                ('mon_late_evening', models.BooleanField(default=True)),
                ('tue_late_evening', models.BooleanField(default=True)),
                ('wed_late_evening', models.BooleanField(default=True)),
                ('thu_late_evening', models.BooleanField(default=True)),
                ('fri_late_evening', models.BooleanField(default=True)),
                ('sat_late_evening', models.BooleanField(default=True)),
                ('sun_late_evening', models.BooleanField(default=True)),
                ('mon_overnight', models.BooleanField(default=True)),
                ('tue_overnight', models.BooleanField(default=True)),
                ('wed_overnight', models.BooleanField(default=True)),
                ('thu_overnight', models.BooleanField(default=True)),
                ('fri_overnight', models.BooleanField(default=True)),
                ('sat_overnight', models.BooleanField(default=True)),
                ('sun_overnight', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('mobile_booking_accepted_denied', models.BooleanField(default=True)),
                ('mobile_new_review', models.BooleanField(default=True)),
                ('mobile_booking_request', models.BooleanField(default=True)),
                ('mobile_friend_joined', models.BooleanField(default=True)),
                ('mobile_groups_added_network', models.BooleanField(default=True)),
                ('mobile_upcoming_booking_remind', models.BooleanField(default=True)),
                ('email_booking_accepted_denied', models.BooleanField(default=True)),
                ('email_new_review', models.BooleanField(default=True)),
                ('email_booking_request', models.BooleanField(default=True)),
                ('email_friend_joined', models.BooleanField(default=True)),
                ('email_groups_added_network', models.BooleanField(default=True)),
                ('email_upcoming_booking_remind', models.BooleanField(default=True)),
                ('email_news', models.BooleanField(default=False)),
                ('email_blog', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sitter',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('biography', models.TextField(blank=True)),
                ('gender', models.CharField(default=b'female', max_length=10, choices=[(b'male', b'male'), (b'female', b'female')])),
                ('id_verified', models.BooleanField(default=False)),
                ('dob', models.DateTimeField(default=datetime.datetime.now)),
                ('smoker', models.BooleanField(default=False)),
                ('sick', models.BooleanField(default=True)),
                ('will_transport', models.BooleanField(default=True)),
                ('total_exp', models.SmallIntegerField()),
                ('infant_exp', models.SmallIntegerField(blank=True)),
                ('toddler_exp', models.SmallIntegerField(blank=True)),
                ('preschool_exp', models.SmallIntegerField(blank=True)),
                ('school_age_exp', models.SmallIntegerField(blank=True)),
                ('pre_teen_exp', models.SmallIntegerField(blank=True)),
                ('teen_exp', models.SmallIntegerField(blank=True)),
                ('special_needs_exp', models.BooleanField(default=True)),
                ('extra_exp', models.TextField(default=b'', null=True, blank=True)),
                ('highest_education', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('last_school', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('major', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('occupation', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('current_student', models.BooleanField(default=False)),
                ('one_child_min_rate', models.DecimalField(max_digits=5, decimal_places=2)),
                ('one_child_max_rate', models.DecimalField(max_digits=5, decimal_places=2)),
                ('two_child_min_rate', models.DecimalField(max_digits=5, decimal_places=2, blank=True)),
                ('two_child_max_rate', models.DecimalField(max_digits=5, decimal_places=2, blank=True)),
                ('three_child_min_rate', models.DecimalField(max_digits=5, decimal_places=2, blank=True)),
                ('three_child_max_rate', models.DecimalField(max_digits=5, decimal_places=2, blank=True)),
                ('smokers_ok', models.BooleanField(default=True)),
                ('dogs_ok', models.BooleanField(default=True)),
                ('cats_ok', models.BooleanField(default=True)),
                ('other_animals_ok', models.BooleanField(default=True)),
                ('has_drivers_licence', models.BooleanField(default=False)),
                ('travel_distance', models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1)])),
                ('certifications', models.ManyToManyField(to='app.Certification', blank=True)),
                ('other_services', models.ManyToManyField(to='app.OtherService', blank=True)),
            ],
            options={
                'verbose_name': 'Sitter',
            },
            bases=('app.user',),
        ),
        migrations.CreateModel(
            name='SitterReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('recommended', models.BooleanField(default=False)),
                ('rehire', models.BooleanField(default=False)),
                ('review', models.TextField(blank=True)),
                ('parent', models.ForeignKey(related_name=b'reviews', to='app.Parent')),
                ('sitter', models.ForeignKey(related_name=b'reviews', to='app.Sitter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpecialNeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('need', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='sitterreview',
            unique_together=set([('parent', 'sitter')]),
        ),
        migrations.AddField(
            model_name='settings',
            name='user',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schedule',
            name='sitter',
            field=models.OneToOneField(to='app.Sitter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='phone',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='parent',
            name='bookmarks',
            field=models.ManyToManyField(related_name=b'bookmarks', to='app.Sitter', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='parent',
            name='sitter_teams',
            field=models.ManyToManyField(related_name=b'sitter_teams', to='app.Sitter', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='phone',
            field=models.ForeignKey(to='app.Phone'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='child',
            name='parent',
            field=models.ForeignKey(related_name=b'children', to='app.Parent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='child',
            name='special_needs',
            field=models.ManyToManyField(to='app.SpecialNeed', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='accepted_sitter',
            field=models.ForeignKey(blank=True, to='app.Sitter', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='declined_sitters',
            field=models.ManyToManyField(related_name=b'declined_bookings', to='app.Sitter', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='parent',
            field=models.ForeignKey(related_name=b'bookings', to='app.Parent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='sitters',
            field=models.ManyToManyField(related_name=b'bookings', to='app.Sitter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='friends_rel_+', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='invited_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='languages',
            field=models.ManyToManyField(related_name=b'users', to='app.Language', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='sitter_groups',
            field=models.ManyToManyField(to='app.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='users_in_network',
            field=models.ManyToManyField(related_name='users_in_network_rel_+', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
