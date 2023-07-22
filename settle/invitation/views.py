from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, HttpResponse
from .forms import InvitationForm
from settle.common.forms import SubscribeForm


def send_invitation_email(invitee_email, person_name, marriage_date, marriage_location):
    html_message = render_to_string('invitation-email.html', {
        'person_name': person_name,
        'marriage_date': marriage_date,
        'marriage_location': marriage_location
    })
    plain_message = strip_tags(html_message)
    subject = 'Marriage Invitation'
    from_email = 'settleprojectdjango@gmail.com'
    recipient_list = [invitee_email]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


def invite(request):
    if request.method == 'POST':
        invite_form = InvitationForm(request.POST)
        if invite_form.is_valid():
            invitee_email = invite_form.cleaned_data['email']
            person_name = invite_form.cleaned_data['name']
            marriage_date = invite_form.cleaned_data['date']
            marriage_location = invite_form.cleaned_data['location']

            invite_form.save()
            send_invitation_email(invitee_email, person_name, marriage_date, marriage_location)
            subscribe_form = SubscribeForm()
            context = {'subscribe_form': subscribe_form}

            return render(request, 'invitation/invite-success.html', context)

    invite_form = InvitationForm()
    subscribe_form = SubscribeForm()

    context = {'invite_form': invite_form, 'subscribe_form': subscribe_form}

    return render(request, 'invitation/invitation.html', context)
