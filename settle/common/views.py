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
    user = request.user  # Get the current user

    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)  # Create a subscription form from the submitted data
        if subscribe_form.is_valid():
            subscribe_form.save()  # Save the subscription data to the database
            return redirect('subscribe')  # Redirect to the subscription page after successful submission

    context = {
        'subscribe_form': subscribe_form,
        'user': user,
    }

    return render(request, 'common/index.html', context)


@login_required
def search(request):
    form = SearchForm(request.GET or None)  # Create a search form using GET data or None
    user = request.user

    if form.is_valid():
        query = form.cleaned_data['search_bar']  # Extract cleaned data from the form
        photos = Photo.objects.filter(user=user, title__icontains=query)  # Filter photos based on the search query
    else:
        query = ''
        photos = Photo.objects.filter(user=user)  # Fetch all photos if the search form is not valid

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
        contact_form = ContactForm(request.POST)  # Create a contact form from the submitted data
        if contact_form.is_valid():
            contact_form.save()  # Save the contact form data to the database

        return redirect('home-page')  # Redirect to the home page after submitting the contact form

    contact_form = ContactForm()  # Create an empty contact form for GET requests
    subscribe_form = SubscribeForm()  # Create a subscription form

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
    Subscribe.objects.create(email=subscriber_email)  # Create a subscription entry in the database


def subscribe_view(request):
    if request.method == 'POST':
        subscribe_form = SubscribeForm()  # Create a subscription form from the submitted data
        subscriber_email = request.POST['email']  # Extract the subscriber's email from the POST data
        send_subscription_email(subscriber_email)  # Send a subscription welcome email
        return render(request, 'common/subscribe-success.html', {'subscribe_form': subscribe_form})
        # Render the subscription success page
    else:
        return HttpResponse('Invalid request!')  # Return an error response for non-POST requests
