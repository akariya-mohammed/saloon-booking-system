from flask_mail import Message
from app import mail
from flask import current_app


def send_booking_confirmation(recipient_email, appointment):
    """Send booking confirmation email to customer."""
    try:
        subject = 'Booking Confirmation - GlamBook'

        body = f"""
        Dear {appointment.customer.first_name},

        Your appointment has been successfully booked!

        Appointment Details:
        -------------------
        Service: {appointment.service.name}
        Date: {appointment.appointment_date.strftime('%B %d, %Y')}
        Time: {appointment.appointment_time.strftime('%I:%M %p')}
        Duration: {appointment.service.duration} minutes
        Price: ${appointment.service.price}
        Status: {appointment.status.capitalize()}

        {f'Notes: {appointment.notes}' if appointment.notes else ''}

        We look forward to seeing you!

        If you need to reschedule or cancel, please log in to your account.

        Best regards,
        GlamBook Team
        """

        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            body=body
        )

        mail.send(msg)
        return True

    except Exception as e:
        current_app.logger.error(f'Failed to send email: {str(e)}')
        return False


def send_booking_reminder(recipient_email, appointment):
    """Send appointment reminder email (24 hours before)."""
    try:
        subject = 'Appointment Reminder - GlamBook'

        body = f"""
        Dear {appointment.customer.first_name},

        This is a friendly reminder about your upcoming appointment tomorrow!

        Appointment Details:
        -------------------
        Service: {appointment.service.name}
        Date: {appointment.appointment_date.strftime('%B %d, %Y')}
        Time: {appointment.appointment_time.strftime('%I:%M %p')}

        We look forward to seeing you!

        Best regards,
        GlamBook Team
        """

        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            body=body
        )

        mail.send(msg)
        return True

    except Exception as e:
        current_app.logger.error(f'Failed to send reminder email: {str(e)}')
        return False


def send_booking_cancellation(recipient_email, appointment):
    """Send booking cancellation confirmation email."""
    try:
        subject = 'Booking Cancelled - GlamBook'

        body = f"""
        Dear {appointment.customer.first_name},

        Your appointment has been cancelled.

        Cancelled Appointment:
        ---------------------
        Service: {appointment.service.name}
        Date: {appointment.appointment_date.strftime('%B %d, %Y')}
        Time: {appointment.appointment_time.strftime('%I:%M %p')}

        If you'd like to book a new appointment, please visit our website.

        Best regards,
        GlamBook Team
        """

        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            body=body
        )

        mail.send(msg)
        return True

    except Exception as e:
        current_app.logger.error(f'Failed to send cancellation email: {str(e)}')
        return False
