# -*- coding: utf-8 -*-
import pytz
import re

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django_twilio.decorators import twilio_view
from django.utils import timezone
from twilio.rest import TwilioRestClient
from twilio.twiml import Response

from sitterfied.app.utils import get_short_url
from sitterfied.bookings.models import Booking
from sitterfied.sitters.models import Sitter
from sitterfied.utils.models import IncomingSMSMessage


# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
sitterfied_number = settings.TWILIO_DEFAULT_CALLERID
client = TwilioRestClient(account_sid, auth_token)


response_pattern = '(accept|yes|decline|no)[^\d]*(\d+)'

@twilio_view
def sms_messages(request):
    from_number = request.POST.get('From', None)
    resp = Response()

    try:
        sitter = Sitter.objects.get(cell=from_number)
    except (Sitter.DoesNotExist, ObjectDoesNotExist):
        resp.sms('We\'re sorry, but this cell phone isn\'t registered.')
        return resp

    body = request.POST.get('Body')
    result = re.search(response_pattern, body, re.I | re.S)

    if result is None or len(result.groups()) < 2:
        resp.sms('We\'re sorry, but we couldn\'t understand your response. \
Please respond with either ACCEPT or DECLINE followed by the code you received.')
        return resp

    response = result.group(1).lower()
    request_id = result.group(2)

    try:
        booking = Booking.objects.get(id=request_id)
    except (Booking.DoesNotExist, ObjectDoesNotExist):
        resp.sms('We\'re sorry, but we couldn\'t find job request ' + request_id + '. Please check the code and try again.')
        return resp

    if booking.canceled:
        resp.sms('We\'re sorry, but this job has been cancelled.')
        return resp

    if sitter in booking.declined_sitters.all():
        resp.sms('We\'re sorry, but you\'ve already declined this job.')
        return resp

    if not sitter in booking.sitters.all():
        resp.sms('We\'re sorry, but we couldn\'t find job request ' + request_id + '. Please check the code and try again.')
        return resp

    if booking.accepted_sitter:
        if booking.accepted_sitter == sitter:
            if response != 'decline' and response != 'no':
                resp.sms('Hi ' + sitter.first_name + '. Thanks for responding, but you\'ve already accepted this job.')
        else:
            resp.sms('Hi ' + sitter.first_name + '. Thanks for responding, but this job has already been accepted.')
        return resp

    try:
        timezone.activate(sitter.timezone if sitter.timezone else pytz.UTC)
        if response == 'accept' or response == 'yes':
            booking.accept(sitter)
        elif response == 'decline' or response == 'no':
            if booking.accepted_sitter == sitter:
                short_url = get_short_url('/mybookings/upcoming')
                resp.sms('You have already ACCEPTED this job. If you\'d like to cancel, go here: ' + short_url)
            else:
                booking.decline(sitter)
    finally:
        timezone.deactivate()

    return resp


#for polling via cronjob
def get_new_messages():
    try:
        most_recent_message = IncomingSMSMessage.objects.all().order_by('-date_created')[0]
        most_recent = most_recent_message.date_created
        messages = client.sms.messages.list(to=sitterfied_number, after=most_recent)
    except IndexError:
        print "no messages yet"
        messages = client.sms.messages.list(to=sitterfied_number)
    for message in messages:
        new_message = IncomingSMSMessage(**message)
        new_message.save()


def send_message(body, to):
    client.messages.create(body=body, to=to, from_=sitterfied_number)
