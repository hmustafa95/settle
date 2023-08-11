from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from .forms import InvitationForm
from settle.common.forms import SubscribeForm


def send_invitation_email(invitee_email, person_name, marriage_date, marriage_location):
    # Render the email content using a template and provided data
    html_message = render_to_string('invitation-email.html', {
        'person_name': person_name,
        'marriage_date': marriage_date,
        'marriage_location': marriage_location
    })
    plain_message = strip_tags(html_message)  # Convert HTML to plain text
    subject = 'Marriage Invitation'  # Subject of the email
    from_email = 'settleprojectdjango@gmail.com'  # Sender's email address
    recipient_list = [invitee_email]  # List of recipients

    # Send the email with both plain and HTML content
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


@login_required
def invite(request):
    if request.method == 'POST':
        invite_form = InvitationForm(request.POST)  # Create an invitation form from the submitted data
        if invite_form.is_valid():
            invitee_email = invite_form.cleaned_data['email']  # Extract cleaned data from the form
            person_name = invite_form.cleaned_data['name']
            marriage_date = invite_form.cleaned_data['date']
            marriage_location = invite_form.cleaned_data['location']

            invite_form.save()  # Save the form data to the database
            send_invitation_email(invitee_email, person_name, marriage_date, marriage_location)
            subscribe_form = SubscribeForm()
            context = {'subscribe_form': subscribe_form}

            return render(request, 'invitation/invite-success.html', context)  # Render a success page after sending

    invite_form = InvitationForm()  # Create an empty invitation form for GET requests
    subscribe_form = SubscribeForm()

    context = {'invite_form': invite_form, 'subscribe_form': subscribe_form}

    return render(request, 'invitation/invitation.html', context)  # Render the invitation form page
