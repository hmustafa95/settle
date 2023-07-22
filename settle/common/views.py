from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SubscribeForm, SearchForm, ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from settle.photos.models import Photo
from .models import Subscribe


def home_page(request):
    subscribe_form = SubscribeForm()
    user = request.user

    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            return redirect('subscribe')

    context = {
        'subscribe_form': subscribe_form,
        'user': user,
    }

    return render(request, 'common/index.html', context)


@login_required
def search(request):
    form = SearchForm(request.GET or None)
    user = request.user

    if form.is_valid():
        query = form.cleaned_data['search_bar']
        photos = Photo.objects.filter(user=user, title__icontains=query)
    else:
        query = ''
        photos = Photo.objects.filter(user=user)

    subscribe_form = SubscribeForm()
    context = {
        'form': form,
        'query': query,
        'photos': photos,
        'subscribe_form': subscribe_form,
    }

    return render(request, 'common/search_results.html', context)


def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()

        return redirect('home-page')

    contact_form = ContactForm()
    subscribe_form = SubscribeForm()

    return render(request, 'common/contact.html', {'contact_form': contact_form, 'subscribe_form': subscribe_form})


def about(request):
    subscribe_form = SubscribeForm()
    context = {'subscribe_form': subscribe_form}
    return render(request, 'common/about.html', context)


def couple(request):
    subscribe_form = SubscribeForm()
    return render(request, 'common/couple.html', {'subscribe_form': subscribe_form})


def send_subscription_email(subscriber_email):
    html_message = render_to_string('subscription-email.html', {'subscriber_email': subscriber_email})
    plain_message = strip_tags(html_message)

    subject = 'Welcome to Settle'
    from_email = 'settleprojectdjango@gmail.com'
    recipient_list = [subscriber_email]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    Subscribe.objects.create(email=subscriber_email)


def subscribe_view(request):
    if request.method == 'POST':
        subscriber_email = request.POST['email']
        send_subscription_email(subscriber_email)
        return render(request, 'common/subscribe-success.html')
    else:
        return HttpResponse('Invalid request!')
