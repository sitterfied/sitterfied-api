# -*- coding: utf-8 -*-
from celery.utils.log import get_task_logger
from django.template.loader import render_to_string

from app.models import Booking
from app.sms import send_message
from app.utils import get_short_url
from sitterfied.celeryapp import app


logger = get_task_logger(__name__)


@app.task
def notify_parent_of_job_request(id):
    try:
        booking = Booking.objects.get(pk=id)
    except Booking.DoesNotExist:
        pass

    if booking:
        parent = booking.parent

        if parent.settings.email_booking_accepted_denied:
            pass  # TODO: implement email for parent request sent

        if parent.settings.mobile_booking_accepted_denied:
            if 'Interview' in booking.booking_type:
                sms_template = 'sms/interview/interview_request_parent_confirmation.sms'
            else:
                sms_template = 'sms/booking/booking_request_sent.sms'
            try:
                sms = render_to_string(sms_template, {'short_url': get_short_url('/mybookings/pending')})
                send_message(body=sms, to=parent.cell)
            except:
                pass


@app.task
def notify_sitters_of_job_request(id, pk_set):
    try:
        booking = Booking.objects.get(pk=id)
    except Booking.DoesNotExist:
        pass

    if booking:
        parent = booking.parent

        email_sitters = booking.sitters.filter(settings__email_booking_request=True).filter(id__in=pk_set)
        text_sitters = booking.sitters.filter(settings__mobile_booking_request=True).filter(id__in=pk_set)
        multi_request_suffix = '_multiple' if len(booking.sitters.all()) > 1 else ''

        for sitter in email_sitters:
            """
            *|FULL_NAME|* [URL link to parent's profile page] would like you to
            sit for *|CHILD_1|*, *|CHILD_2|* and *|CHILD_3|* on *|JOB_DATE|* from
            *|FROM_TIME|* to *|TO_TIME|*.

            The job is located at *|JOB_ADDRESS|*

            Go to your bookings page [URL link to sitter's bookings page] to
            Accept or Decline this job.

            *|FNAME|* added a note- "*|SHOW_NOTE|*"

            You can reach *|FNAME|* by email: *|EMAIL|* or phone: *|MOBILE|*
            """
            # message = create_message_base()
            # message['subject'] = 'You have a new job request!'
            # message['to'] = [create_email_to(sitter.email, sitter.get_full_name())]
            # message['global_merge_vars'] = [{
            #     'FNAME': sitter.first_name,
            #     'PARENT_NAME': parent.get_full_name(),
            #     'PARENT_URL': '/profile/' + str(parent.id),
            # }]
            # TODO: send_template_email('', message)

        short_url = get_short_url('/mybookings/pending')

        for sitter in text_sitters:
            if not sitter.cell:
                continue

            if 'Interview' in booking.booking_type:
                booking_type = booking.booking_type.replace(' Interview', '_Interview').lower()
                sms_template = 'sms/interview/{0}_request_to_sitter.sms'.format(booking_type)
            else:
                sms_template = 'sms/booking/booking_request_received{0}.sms'.format(multi_request_suffix)

            booking_date = booking.start_date_time.date()
            try:
                sms = render_to_string(sms_template, {
                    'sitter_name': sitter.first_name,
                    'parent_name': parent.get_full_name(),
                    'booking_date': booking_date,
                    'start_date_time': booking.start_date_time,
                    'stop_date_time': booking.stop_date_time,
                    'parent_city': parent.city,
                    'short_url': short_url,
                    'booking_code': booking.id,
                    'num_sitters': len(booking.sitters.all()) - 1,
                })
                send_message(body=sms, to=sitter.cell)
            except:
                pass