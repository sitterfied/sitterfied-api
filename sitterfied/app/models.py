from datetime import datetime

from django.db import models

from django.utils.functional import cached_property


from model_utils.models import TimeStampedModel
# Create your models here.

from model_utils.choices import Choices


from django.contrib.auth.models import AbstractUser, UserManager

from django_localflavor_us.models import USStateField
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^django_localflavor_us\.models\.USStateField"])


from model_utils.managers import InheritanceManager



from pyuploadcare.dj import ImageField as UploadcareImageField

import re
import time

UPLOADS_DIR = 'uploads/{0}/{1.year:04}/{1.month:02}/{1.day:02}/{2}/{3}'
def file_url(name):
    def inner(instance, filename):
        r = re.compile(r'[^\S]')
        filename = r.sub('', filename)
        now = datetime.now()
        timestamp = int(time.time())
        return  UPLOADS_DIR.format(name, now, timestamp, filename)
    return inner



class User(AbstractUser, TimeStampedModel):
    objects = UserManager()

    MEMBERSHIP_STATUS = Choices("Trial", "paid")
    users_in_network = models.ManyToManyField('self',  blank=True, symmetrical=True)
    friends = models.ManyToManyField('self',  blank=True)

    sitter_groups = models.ManyToManyField('Group', blank=True)
    invited_by = models.ManyToManyField('self',  symmetrical =False, blank=True)
    languages = models.ManyToManyField('Language', blank=True, related_name="users")
    status = models.CharField(blank=False, max_length=10, choices=MEMBERSHIP_STATUS, default="Trial")
    membership_exp_date = models.DateTimeField(null=True)

    facebook_token = models.CharField(max_length=256, null=True, blank=True)
    facebook_id = models.IntegerField(null=True, blank=True)

    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = USStateField(blank=True, default="AZ")
    zip = models.CharField(max_length=9, blank=True)  # there is forms.USZipCodeField but no model.USZip..., ComingSoonInterest does not use
    cell = models.CharField(max_length=12, blank=True)


    avatar = UploadcareImageField(blank=True, manual_crop="")
    #avatar_url = models.URLField(blank=True)
    #objects = InheritanceManager()

    @property
    def avatar_url(self):
        return getattr(self.avatar, 'cdn_url', None)

    def __unicode__(self):
        return self.get_full_name()

    def is_parent_or_sitter(self):
        if hasattr(self, 'sitter'):
            return 'Sitter'
        elif hasattr(self, 'parent'):
            return 'Parent'




class Address(TimeStampedModel):
    user = models.ForeignKey(User)



class Phone(TimeStampedModel):
    PHONE_TYPES = Choices("Work", "Home", "Cell", "Emergency", "Contact", "Other")

    phone_type = models.CharField(max_length=10, choices=PHONE_TYPES, default="work")
    number = models.CharField(max_length=25)
    #TODO: use a unique partial index to ensure that a user only has a single primary
    primary = models.BooleanField()
    user = models.ForeignKey(User)



class Parent(User):
    emergency_contact_one_name = models.CharField(max_length=128, blank=True)
    emergency_contact_one_phone = models.CharField(max_length=10, blank=True)
    emergency_contact_two_name = models.CharField(max_length=128, blank=True)
    emergency_contact_two_phone = models.CharField(max_length=10, blank=True)

    sitter_teams = models.ManyToManyField('Sitter', related_name="sitter_teams", blank=True)
    bookmarks = models.ManyToManyField('Sitter', related_name="bookmarks", blank=True)

    class Meta:
         verbose_name = "Parent"

class Sitter(User):
    biography = models.TextField(blank=True)

    GENDERS = Choices('male', 'female')
    gender = models.CharField(max_length=10, choices=GENDERS, default='female')
    id_verified = models.BooleanField(default=False)

    live_zip = models.CharField(max_length=9, blank=True)
    work_zip = models.CharField(max_length=9, blank=True)

    dob = models.DateTimeField(blank=False, default=datetime.now)
    smoker = models.BooleanField(default=True)
    sick =  models.BooleanField(default=True)
    will_transport = models.BooleanField(default=False)

    total_exp = models.SmallIntegerField(default=0)
    infant_exp = models.SmallIntegerField(default=0)
    toddler_exp = models.SmallIntegerField(default=0)
    preschool_exp = models.SmallIntegerField(default=0)
    school_age_exp = models.SmallIntegerField(default=0)
    pre_teen_exp = models.SmallIntegerField(default=0)
    teen_exp = models.SmallIntegerField(default=0)

    special_needs_exp = models.BooleanField(default=True)
    extra_exp = models.TextField(blank=True, default="", null=True)

    highest_education = models.CharField(max_length=50, blank=True, default="", null=True)
    last_school = models.CharField(max_length=50, blank=True, default="", null=True)

    major = models.CharField(max_length=50, blank=True, default="", null=True)
    occupation = models.CharField(max_length=50, blank=True, default="", null=True)

    current_student = models.BooleanField(default=False)


    other_services = models.ManyToManyField('OtherService', blank=True)

    one_child_min_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    one_child_max_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    two_child_min_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    two_child_max_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    three_child_min_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    three_child_max_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    smokers_ok = models.BooleanField(default=True)
    dogs_ok = models.BooleanField(default=True)
    cats_ok = models.BooleanField(default=True)
    other_animals_ok = models.BooleanField(default=True)

    has_drivers_licence = models.BooleanField(default=False)
    travel_distance = models.IntegerField(default=0)

    certifications = models.ManyToManyField("Certification", blank=True)

    class Meta:
         verbose_name = "Sitter"



class Certification(TimeStampedModel):
    certification = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.certification


class OtherService(TimeStampedModel):
    service = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.service


class Language(TimeStampedModel):
    language = models.CharField(max_length=100)

    def __unicode__(self):
        return self.language

class SpecialNeed(TimeStampedModel):
    need = models.CharField(max_length=100)

    def __unicode__(self):
        return self.need


class Settings(TimeStampedModel):
    #parent specific
    user =  models.OneToOneField('User', null=True)

    mobile_booking_accepted_denied = models.BooleanField()

    #sitter specific
    mobile_new_review  = models.BooleanField()
    mobile_booking_request = models.BooleanField()

    mobile_friend_joined = models.BooleanField()
    mobile_groups_added_network = models.BooleanField()
    mobile_upcoming_booking_remind = models.BooleanField()

    #parent specific
    email_booking_accepted_denied = models.BooleanField()

    #sitter specific
    email_new_review  = models.BooleanField()
    email_booking_request = models.BooleanField()

    email_friend_joined = models.BooleanField()
    email_groups_added_network = models.BooleanField()
    email_upcoming_booking_remind = models.BooleanField()

    email_news = models.BooleanField()
    email_blog = models.BooleanField()

class Child(TimeStampedModel):
    parent = models.ForeignKey(Parent, related_name="children")
    name = models.CharField(max_length=50, blank=True, default="")
    dob = models.DateTimeField(blank=True, null=True)
    school = models.CharField(max_length=50, blank=True, default="")
    special_needs = models.ManyToManyField(SpecialNeed, blank=True)

    class Meta:
        verbose_name_plural = "children"



class Contact(TimeStampedModel):
    name = models.CharField(max_length=50)
    phone = models.ForeignKey('Phone')


class Schedlue(TimeStampedModel):
    sitter = models.OneToOneField(Sitter)
    mon_early_morning = models.BooleanField(default=False)
    tues_early_morning = models.BooleanField(default=False)
    wed_early_morning = models.BooleanField(default=False)
    thurs_early_morning = models.BooleanField(default=False)
    fri_early_morning = models.BooleanField(default=False)
    sat_early_morning = models.BooleanField(default=False)
    sun_early_morning = models.BooleanField(default=False)

    mon_late_morning = models.BooleanField(default=False)
    tues_late_morning = models.BooleanField(default=False)
    wed_late_morning = models.BooleanField(default=False)
    thurs_late_morning = models.BooleanField(default=False)
    fri_late_morning = models.BooleanField(default=False)
    sat_late_morning = models.BooleanField(default=False)
    sun_late_morning = models.BooleanField(default=False)

    mon_early_afternoon = models.BooleanField(default=False)
    tues_early_afternoon = models.BooleanField(default=False)
    wed_early_afternoon = models.BooleanField(default=False)
    thurs_early_afternoon = models.BooleanField(default=False)
    fri_early_afternoon = models.BooleanField(default=False)
    sat_early_afternoon = models.BooleanField(default=False)
    sun_early_afternoon = models.BooleanField(default=False)

    mon_late_afternoon = models.BooleanField(default=False)
    tues_late_afternoon = models.BooleanField(default=False)
    wed_late_afternoon = models.BooleanField(default=False)
    thurs_late_afternoon = models.BooleanField(default=False)
    fri_late_afternoon = models.BooleanField(default=False)
    sat_late_afternoon = models.BooleanField(default=False)
    sun_late_afternoon = models.BooleanField(default=False)

    mon_early_evening = models.BooleanField(default=False)
    tues_early_evening = models.BooleanField(default=False)
    wed_early_evening = models.BooleanField(default=False)
    thurs_early_evening = models.BooleanField(default=False)
    fri_early_evening = models.BooleanField(default=False)
    sat_early_evening = models.BooleanField(default=False)
    sun_early_evening = models.BooleanField(default=False)

    mon_late_evening = models.BooleanField(default=False)
    tues_late_evening = models.BooleanField(default=False)
    wed_late_evening = models.BooleanField(default=False)
    thurs_late_evening = models.BooleanField(default=False)
    fri_late_evening = models.BooleanField(default=False)
    sat_late_evening = models.BooleanField(default=False)
    sun_late_evening = models.BooleanField(default=False)

    mon_overnight = models.BooleanField(default=False)
    tues_overnight = models.BooleanField(default=False)
    wed_overnight = models.BooleanField(default=False)
    thurs_overnight = models.BooleanField(default=False)
    fri_overnight = models.BooleanField(default=False)
    sat_overnight = models.BooleanField(default=False)
    sun_overnight = models.BooleanField(default=False)


class SitterReview(TimeStampedModel):
    parent = models.ForeignKey(Parent, related_name="reviews")
    sitter  = models.ForeignKey(Sitter, related_name="reviews")
    recommended = models.BooleanField()
    review = models.TextField()

    class Meta:
        unique_together = ("parent", "sitter")






class Booking(TimeStampedModel):
    BOOKING_STATUS = Choices('Active', 'Pending', 'Completed', 'Expired', 'Declined', 'Canceled',)
    BOOKING_TYPES = Choices('Job', 'Interview')
    parent = models.ForeignKey(Parent, related_name="bookings")
    sitters = models.ManyToManyField(Sitter, related_name="bookings")
    declined_sitters = models.ManyToManyField(Sitter, related_name="declined_bookings")

    notes = models.TextField(blank=True)
    respond_by = models.DateTimeField(blank=True, null=True)
    start_date_time = models.DateTimeField()
    stop_date_time = models.DateTimeField()
    num_children = models.IntegerField(default=1)
    emergency_phone = models.CharField(max_length=10, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = USStateField(blank=True, default="AZ")
    zip = models.CharField(max_length=9, blank=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True)
    booking_status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='Active')
    booking_type =  models.CharField(max_length=10, choices=BOOKING_TYPES, default='Job')
    accepted_sitter= models.ForeignKey(Sitter, blank=True, null=True)
    overnight = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    @cached_property
    def accepted(self):
        return bool(self.accept_sitter)


class IncomingSMSMessage(TimeStampedModel):
    sid = models.CharField(max_length=34)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    date_sent = models.DateTimeField()
    to = models.CharField(max_length=16)
    body = models.CharField(max_length=161)
    status = models.CharField(max_length=12)
    #dealt_with = models.



class Group(TimeStampedModel):
    name = models.CharField(max_length=128, blank=False)
