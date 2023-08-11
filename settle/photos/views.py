from django.shortcuts import render, redirect
from settle.common.forms import SubscribeForm
from .models import Photo
from .forms import PhotoCreateForm, PhotoEditForm
from django.contrib.auth.decorators import login_required


# This decorator ensures that the user must be logged in to access this view.
@login_required
def add_photo(request):
    if request.method == 'GET':
        form = PhotoCreateForm()
    else:
        form = PhotoCreateForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the photo while associating it with the current user.
            form.save(user=request.user)
            return redirect('gallery') # Redirect to the gallery page after successful submission.

    subscribe_form = SubscribeForm()
    context = {
        'form': form,
        'subscribe_form': subscribe_form,
    }
    print(form.errors) # Print any form errors for debugging purposes.
    return render(request, 'photos/add-photo.html', context)


@login_required
# This view displays the details of a specific photo.
def details_photo(request, pk):
    photo = Photo.objects.filter(pk=pk).get()
    subscribe_form = SubscribeForm()
    context = {
        'photo': photo,
        'subscribe_form': subscribe_form,
    }

    return render(request, 'photos/details-photo.html', context)


@login_required
# This view handles editing of a specific photo's details.
def edit_photo(request, pk):
    photo = Photo.objects.filter(pk=pk).get()

    if request.method == 'GET':
        form = PhotoEditForm(instance=photo)
    else:
        form = PhotoEditForm(request.POST, instance=photo)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('details-photo', pk=pk) # Redirect to the photo details page after editing.

    subscribe_form = SubscribeForm()
    context = {
        'form': form,
        'photo': photo,
        'subscribe_form': subscribe_form,
    }

    return render(request, 'photos/edit-photo.html', context)


@login_required
# This view displays a confirmation page before deleting a specific photo.
def confirm_delete_photo(request, pk):
    photo = Photo.objects.filter(pk=pk).get()
    subscribe_form = SubscribeForm()
    context = {
        'photo': photo,
        'subscribe_form': subscribe_form,
    }

    return render(request, 'photos/delete-photo.html', context)


@login_required
# This view handles the deletion of a specific photo.
def delete_photo(request, pk):
    photo = Photo.objects.filter(pk=pk)
    photo.delete()
    return redirect('gallery') # Redirect to the gallery page after deleting a photo.


# This decorator ensures that the user must be logged in to access this view.
@login_required
def gallery(request):
    user = request.user
    photos = Photo.objects.filter(user=user) # Retrieve photos associated with the current user.
    subscribe_form = SubscribeForm()
    context = {
        'photos': photos,
        'subscribe_form': subscribe_form,
    }
    return render(request, 'photos/gallery.html', context)
