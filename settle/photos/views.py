from django.shortcuts import render, redirect
from settle.common.forms import SubscribeForm
from .models import Photo
from .forms import PhotoCreateForm, PhotoEditForm
from django.contrib.auth.decorators import login_required


@login_required
def add_photo(request):
    if request.method == 'GET':
        form = PhotoCreateForm()
    else:
        form = PhotoCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('gallery')

    subscribe_form = SubscribeForm()
    context = {
        'form': form,
        'subscribe_form': subscribe_form,
    }
    print(form.errors)
    return render(request, 'photos/add-photo.html', context)


def details_photo(request, pk):
    photo = Photo.objects.filter(pk=pk).get()
    subscribe_form = SubscribeForm()
    context = {
        'photo': photo,
        'subscribe_form': subscribe_form,
    }

    return render(request, 'photos/details-photo.html', context)


def edit_photo(request, pk):
    photo = Photo.objects.filter(pk=pk).get()

    if request.method == 'GET':
        form = PhotoEditForm(instance=photo)
    else:
        form = PhotoEditForm(request.POST, instance=photo)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('details-photo', pk=pk)

    subscribe_form = SubscribeForm()
    context = {
        'form': form,
        'photo': photo,
        'subscribe_form': subscribe_form,
    }

    return render(request, 'photos/edit-photo.html', context)


def confirm_delete_photo(request, pk):
    photo = Photo.objects.filter(pk=pk).get()
    subscribe_form = SubscribeForm()
    context = {
        'photo': photo,
        'subscribe_form': subscribe_form,
    }

    return render(request, 'photos/delete-photo.html', context)


def delete_photo(request, pk):
    photo = Photo.objects.filter(pk=pk)
    photo.delete()
    return redirect('gallery')


@login_required
def gallery(request):
    user = request.user
    photos = Photo.objects.filter(user=user)
    subscribe_form = SubscribeForm()
    context = {
        'photos': photos,
        'subscribe_form': subscribe_form,
    }
    return render(request, 'photos/gallery.html', context)
