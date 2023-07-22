from django.core import mail
from django.core.exceptions import ValidationError
from datetime import date
from .models import Invitation
from django.test import TestCase, RequestFactory
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import InvitationForm
from .views import send_invitation_email, invite
from datetime import datetime


class InvitationModelTest(TestCase):
    def test_valid_invitation(self):
        invitation = Invitation(
            name='John Doe',
            email='john@example.com',
            location='Some Location',
            date=date.today()
        )

        try:
            invitation.full_clean()
        except ValidationError:
            self.fail("Validation failed.")

        self.assertTrue(True)

    def test_invalid_invitation(self):
        invitation = Invitation(
            name='J',
            email='john@example.com',
            location='Some Location',
            date=date.today()
        )

        with self.assertRaises(ValidationError):
            invitation.full_clean()

    def test_invalid_email(self):
        invitation = Invitation(
            name='John Doe',
            email='john@example',
            location='Some Location',
            date=date.today()
        )

        with self.assertRaises(ValidationError):
            invitation.full_clean()

    def test_blank_fields(self):
        invitation = Invitation()

        with self.assertRaises(ValidationError):
            invitation.full_clean()


class InvitationEmailTest(TestCase):
    def test_send_invitation_email(self):
        invitee_email = 'test@example.com'
        person_name = 'John Doe'
        marriage_date = '2022-01-01'
        marriage_location = 'Some Location'

        send_invitation_email(invitee_email, person_name, marriage_date, marriage_location)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Marriage Invitation')
        self.assertEqual(mail.outbox[0].from_email, 'thindan@gmail.com')
        self.assertEqual(mail.outbox[0].to, [invitee_email])

        html_message = render_to_string('invitation-email.html', {
            'person_name': person_name,
            'marriage_date': marriage_date,
            'marriage_location': marriage_location
        })
        plain_message = strip_tags(html_message)
        self.assertEqual(mail.outbox[0].body, plain_message)
        self.assertEqual(mail.outbox[0].alternatives[0][0], html_message)

    def test_invite_view(self):
        factory = RequestFactory()
        request = factory.post('/invite/', {'name': 'John Doe', 'email': 'test@example.com', 'date': '2022-01-01', 'location': 'Some Location'})

        response = invite(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), 'Invitation sent!')

        self.assertEqual(Invitation.objects.count(), 1)
        invitation = Invitation.objects.first()
        self.assertEqual(invitation.name, 'John Doe')
        self.assertEqual(invitation.email, 'test@example.com')
        self.assertEqual(invitation.date, datetime.strptime('2022-01-01', '%Y-%m-%d').date())
        self.assertEqual(invitation.location, 'Some Location')


class InvitationFormTest(TestCase):
    def test_valid_invitation_form(self):
        form_data = {
            'name': 'John Doe',
            'email': 'test@example.com',
            'date': '2022-01-01',
            'location': 'Some Location',
        }

        form = InvitationForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_invalid_invitation_form(self):
        form_data = {}

        form = InvitationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('date', form.errors)
        self.assertIn('location', form.errors)
