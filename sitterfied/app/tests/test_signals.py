# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta

import mock
import pytz
from django.db.models.signals import pre_save, m2m_changed, pre_delete
from django.template.loader import render_to_string
from hamcrest import *
from pytz import timezone

from app import signals, sms, utils
from app.models import Booking, Parent, Sitter, Reminder
from app.tasks.tests import utils


def test_booking_request_message():
    sitter = Sitter()
    sitter.first_name = 'Devon'
    sitter.cell = '+17322397588'

    parent = Parent()
    parent.full_name = 'Elana Nanscawen'

    instance = Booking()
    instance.id = 22
    instance.start_date_time = datetime.now()
    instance.stop_date_time = instance.start_date_time + timedelta(hours=5)

    short_url = 'test.sttrfd.us/' + utils.generate_short_url_code()

    message = render_to_string("sms/booking/booking_request_received.sms", {
        'sitter_name': sitter.first_name,
        'parent_name': parent.full_name,
        'start_date_time': instance.start_date_time,
        'stop_date_time': instance.stop_date_time,
        'short_url': short_url,
        'booking_code': instance.id,
        'num_sitters': str(len(instance.sitters.all()))
    })

    assert_that(message, string_contains_in_order(
        sitter.first_name,
        parent.full_name,
        re.sub('^0', '', instance.start_date_time.strftime('%b %d')),
        re.sub('^0', '', instance.start_date_time.strftime('%I:%M%p').lower()),
        re.sub('^0', '', instance.stop_date_time.strftime('%I:%M%p').lower()),
        short_url,
        str(instance.id),
        str(instance.id),
    ))

    message = render_to_string('sms/booking/booking_request_received_multiple.sms', {
        'sitter_name': sitter.first_name,
        'parent_name': parent.full_name,
        'start_date_time': instance.start_date_time,
        'stop_date_time': instance.stop_date_time,
        'short_url': short_url,
        'booking_code': instance.id,
        'num_sitters': str(len(instance.sitters.all()))
    })

    assert_that(message, string_contains_in_order(
        sitter.first_name,
        parent.full_name,
        str(len(instance.sitters.all())),
        re.sub('^0', '', instance.start_date_time.strftime('%b %d')),
        re.sub('^0', '', instance.start_date_time.strftime('%I:%M%p').lower()),
        re.sub('^0', '', instance.stop_date_time.strftime('%I:%M%p').lower()),
        short_url,
        str(instance.id),
        str(instance.id),
    ))
    #sms.client.messages.create(body=message, to=sitter.cell,
    #from_=sms.sitterfied_number


def test_new_sitter_signal():
    sitter = mock.Mock(spec=Sitter)
    sitter.email = 'alewisohn@gmail.com'
    sitter.first_name = 'Test'
    sitter.last_name = 'Signals'

    signals.new_sitter(sitter, sitter, created=True)


def test_new_parent_signal():
    parent = mock.Mock(spec=Parent)
    parent.email = 'alewisohn@gmail.com'
    parent.first_name = 'Test'
    parent.last_name = 'Signals'

    signals.new_parent(parent, parent, created=True)


def test_reminder_save_handler():
    eastern = timezone('America/New_York')

    booking = Booking()
    booking.start_date_time = datetime.now(eastern) + timedelta(days=0, hours=2, seconds=15)
    booking.stop_date_time = booking.start_date_time + timedelta(seconds=10)
    booking.parent = Parent.objects.get(first_name='Parent')
    booking.accepted_sitter = Sitter.objects.get(first_name='Sitter')

    reminder = Reminder()

    try:
        disconnect_signals()

        booking.save()

        reminder.booking = booking
        reminder.save()

        signals.reminder_save_handler(instance=reminder)

        # booking.start_date_time = datetime.now(eastern) + timedelta(hours=2, minutes=1)
        # booking.stop_date_time = booking.stop_date_time + timedelta(hours=3)
        # booking.save()

        # signals.reminder_save_handler(instance=reminder)
    finally:
        try:
            #booking.delete()
            #reminder.delete()
            pass
        finally:
            reconnect_signals()


def disconnect_signals():
    utils.disconnect_signal(m2m_changed, signals.receive_booking_request, Booking)
    utils.disconnect_signal(pre_save, signals.reminder_save_handler, Reminder)
    utils.disconnect_signal(pre_delete, signals.reminder_del_handler, Reminder)


def reconnect_signals():
    utils.reconnect_signal(m2m_changed, signals.receive_booking_request, Booking)
    utils.reconnect_signal(pre_save, signals.reminder_save_handler, Reminder)
    utils.reconnect_signal(pre_delete, signals.reminder_del_handler, Reminder)
