# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'User.avatar_url'
        db.delete_column(u'app_user', 'avatar_url')


        # Changing field 'User.avatar'
        db.alter_column(u'app_user', 'avatar', self.gf('pyuploadcare.dj.models.ImageField')(default=''))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'User.avatar_url'
        raise RuntimeError("Cannot reverse this migration. 'User.avatar_url' and its values cannot be restored.")

        # Changing field 'User.avatar'
        db.alter_column(u'app_user', 'avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

    models = {
        u'app.address': {
            'Meta': {'object_name': 'Address'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.User']"})
        },
        u'app.booking': {
            'Meta': {'object_name': 'Booking'},
            'accepted_sitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Sitter']", 'null': 'True', 'blank': 'True'}),
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'booking_status': ('django.db.models.fields.CharField', [], {'default': "'Active'", 'max_length': '10'}),
            'booking_type': ('django.db.models.fields.CharField', [], {'default': "'Job'", 'max_length': '10'}),
            'canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'declined_sitters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'declined_bookings'", 'symmetrical': 'False', 'to': u"orm['app.Sitter']"}),
            'emergency_phone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'num_children': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'overnight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bookings'", 'to': u"orm['app.Parent']"}),
            'rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'respond_by': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sitters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'bookings'", 'symmetrical': 'False', 'to': u"orm['app.Sitter']"}),
            'start_date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'state': ('django_localflavor_us.models.USStateField', [], {'default': "'AZ'", 'max_length': '2', 'blank': 'True'}),
            'stop_date_time': ('django.db.models.fields.DateTimeField', [], {}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'})
        },
        u'app.certification': {
            'Meta': {'object_name': 'Certification'},
            'certification': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'app.child': {
            'Meta': {'object_name': 'Child'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'dob': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'to': u"orm['app.Parent']"}),
            'school': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'special_needs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.SpecialNeed']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'app.contact': {
            'Meta': {'object_name': 'Contact'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Phone']"})
        },
        u'app.group': {
            'Meta': {'object_name': 'Group'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'app.incomingsmsmessage': {
            'Meta': {'object_name': 'IncomingSMSMessage'},
            'body': ('django.db.models.fields.CharField', [], {'max_length': '161'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'sid': ('django.db.models.fields.CharField', [], {'max_length': '34'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'to': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'app.language': {
            'Meta': {'object_name': 'Language'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'app.otherservice': {
            'Meta': {'object_name': 'OtherService'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'service': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'app.parent': {
            'Meta': {'object_name': 'Parent', '_ormbases': [u'app.User']},
            'bookmarks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'bookmarks'", 'blank': 'True', 'to': u"orm['app.Sitter']"}),
            'emergency_contact_one_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'emergency_contact_one_phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'emergency_contact_two_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'emergency_contact_two_phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sitter_teams': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'sitter_teams'", 'blank': 'True', 'to': u"orm['app.Sitter']"}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['app.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'app.phone': {
            'Meta': {'object_name': 'Phone'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'phone_type': ('django.db.models.fields.CharField', [], {'default': "'work'", 'max_length': '10'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.User']"})
        },
        u'app.schedlue': {
            'Meta': {'object_name': 'Schedlue'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'fri_early_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fri_early_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fri_early_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fri_late_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fri_late_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fri_late_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fri_overnight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'mon_early_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mon_early_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mon_early_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mon_late_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mon_late_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mon_late_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mon_overnight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sat_early_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sat_early_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sat_early_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sat_late_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sat_late_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sat_late_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sat_overnight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sitter': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['app.Sitter']", 'unique': 'True'}),
            'sun_early_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sun_early_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sun_early_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sun_late_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sun_late_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sun_late_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sun_overnight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thurs_early_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thurs_early_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thurs_early_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thurs_late_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thurs_late_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thurs_late_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thurs_overnight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tues_early_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tues_early_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tues_early_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tues_late_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tues_late_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tues_late_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tues_overnight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wed_early_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wed_early_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wed_early_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wed_late_afternoon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wed_late_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wed_late_morning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wed_overnight': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'app.settings': {
            'Meta': {'object_name': 'Settings'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'email_blog': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_booking_accepted_denied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_booking_request': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_friend_joined': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_groups_added_network': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_new_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_news': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_upcoming_booking_remind': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_booking_accepted_denied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobile_booking_request': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobile_friend_joined': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobile_groups_added_network': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobile_new_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobile_upcoming_booking_remind': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['app.User']", 'unique': 'True', 'null': 'True'})
        },
        u'app.sitter': {
            'Meta': {'object_name': 'Sitter', '_ormbases': [u'app.User']},
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cats_ok': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'certifications': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Certification']", 'symmetrical': 'False', 'blank': 'True'}),
            'current_student': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dob': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'dogs_ok': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'extra_exp': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'female'", 'max_length': '10'}),
            'has_drivers_licence': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'highest_education': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'infant_exp': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'last_school': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'live_zip': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'one_child_max_rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'one_child_min_rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'other_animals_ok': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'other_services': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.OtherService']", 'symmetrical': 'False', 'blank': 'True'}),
            'pre_teen_exp': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'preschool_exp': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'school_age_exp': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'sick': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'smoker': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'smokers_ok': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'special_needs_exp': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'teen_exp': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'three_child_max_rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'three_child_min_rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'toddler_exp': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'total_exp': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'travel_distance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'two_child_max_rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            'two_child_min_rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['app.User']", 'unique': 'True', 'primary_key': 'True'}),
            'will_transport': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_zip': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'})
        },
        u'app.sitterreview': {
            'Meta': {'unique_together': "(('parent', 'sitter'),)", 'object_name': 'SitterReview'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': u"orm['app.Parent']"}),
            'recommended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'review': ('django.db.models.fields.TextField', [], {}),
            'sitter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': u"orm['app.Sitter']"})
        },
        u'app.specialneed': {
            'Meta': {'object_name': 'SpecialNeed'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'need': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'app.user': {
            'Meta': {'object_name': 'User'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'avatar': ('pyuploadcare.dj.models.ImageField', [], {'blank': 'True'}),
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_token': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'friends_rel_+'", 'blank': 'True', 'to': u"orm['app.User']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited_by': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'users'", 'blank': 'True', 'to': u"orm['app.Language']"}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'membership_exp_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'sitter_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'state': ('django_localflavor_us.models.USStateField', [], {'default': "'AZ'", 'max_length': '2', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Trial'", 'max_length': '10'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'users_in_network': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users_in_network_rel_+'", 'blank': 'True', 'to': u"orm['app.User']"}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']