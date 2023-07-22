from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Photo
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse
from .views import (
    add_photo,
    details_photo,
    edit_photo,
    confirm_delete_photo,
    delete_photo,
    gallery,
)
from .forms import PhotoCreateForm, PhotoEditForm
from ..accounts.models import SettleUser

UserModel = get_user_model()


class PhotoModelTest(TestCase):
    def setUp(self):
        self.user = SettleUser.objects.create_user(username='testuser', password='testpass')
        self.photo = SimpleUploadedFile('test_photo.jpg', content=b'test_photo_data', content_type='image/jpeg')

    def test_create_photo(self):
        photo = Photo.objects.create(
            title='Test Photo',
            photo=self.photo,
            description='Test description',
            location='Test location',
            user=self.user
        )
        self.assertEqual(photo.title, 'Test Photo')
        self.assertEqual(photo.description, 'Test description')
        self.assertEqual(photo.location, 'Test location')
        self.assertEqual(photo.user, self.user)

    def test_photo_fields_blank_or_null(self):
        photo = Photo.objects.create(title='Test Photo', user=self.user)
        self.assertEqual(photo.description, None)
        self.assertEqual(photo.location, None)

    def test_photo_fields_validators(self):
        photo = Photo(
            title='Short',
            description='Too short',
            location='Long location name',
            user=self.user
        )
        with self.assertRaises(Exception):
            photo.full_clean()

    def test_photo_upload_to_directory(self):
        photo = Photo.objects.create(
            title='Test Photo',
            photo=self.photo,
            user=self.user
        )
        self.assertEqual(photo.photo.path.startswith('images/'), True)

    def test_date_of_publication_auto_now(self):
        photo = Photo.objects.create(
            title='Test Photo',
            photo=self.photo,
            user=self.user
        )
        self.assertIsNotNone(photo.date_of_publication)


class PhotoViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = SettleUser.objects.create_user(username='testuser', password='testpass')
        self.photo = Photo.objects.create(title='Test Photo', user=self.user)

    def test_add_photo_view(self):
        url = reverse('add-photo')
        request = self.factory.get(url)
        request.user = self.user

        response = add_photo(request)
        self.assertEqual(response.status_code, 200)

    def test_details_photo_view(self):
        url = reverse('details-photo', kwargs={'pk': self.photo.pk})
        request = self.factory.get(url)

        response = details_photo(request, pk=self.photo.pk)
        self.assertEqual(response.status_code, 200)

    def test_edit_photo_view(self):
        url = reverse('edit-photo', kwargs={'pk': self.photo.pk})
        request = self.factory.get(url)
        request.user = self.user

        response = edit_photo(request, pk=self.photo.pk)
        self.assertEqual(response.status_code, 200)

    def test_confirm_delete_photo_view(self):
        url = reverse('confirm-delete-photo', kwargs={'pk': self.photo.pk})
        request = self.factory.get(url)

        response = confirm_delete_photo(request, pk=self.photo.pk)
        self.assertEqual(response.status_code, 200)

    def test_delete_photo_view(self):
        url = reverse('delete-photo', kwargs={'pk': self.photo.pk})
        request = self.factory.post(url)
        request.user = self.user

        response = delete_photo(request, pk=self.photo.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('gallery'))

    def test_gallery_view(self):
        url = reverse('gallery')
        request = self.factory.get(url)

        response = gallery(request)
        self.assertEqual(response.status_code, 200)


class PhotoFormsTest(TestCase):
    def setUp(self):
        self.user = SettleUser.objects.create_user(username='testuser', password='testpass')

    def test_photo_create_form(self):
        form_data = {
            'title': 'Test Photo',
            'photo': 'path/to/photo.jpg',
            'location': 'Test Location',
            'description': 'Test Description',
        }
        form = PhotoCreateForm(data=form_data)
        form.instance.user = self.user

        self.assertTrue(form.is_valid(), form.errors.as_text())

        photo = form.save()

        self.assertEqual(photo.title, 'Test Photo')
        self.assertEqual(photo.photo, 'path/to/photo.jpg')
        self.assertEqual(photo.location, 'Test Location')
        self.assertEqual(photo.description, 'Test Description')
        self.assertEqual(photo.user, self.user)

    def test_photo_edit_form(self):
        photo = Photo.objects.create(
            title='Original Title',
            location='Original Location',
            description='Original Description',
            user=self.user,
        )

        form_data = {
            'title': 'Updated Title',
            'location': 'Updated Location',
            'description': 'Updated Description',
        }
        form = PhotoEditForm(data=form_data, instance=photo)
        form.instance.user = self.user

        self.assertTrue(form.is_valid())
        updated_photo = form.save()

        self.assertEqual(updated_photo.title, 'Updated Title')
        self.assertEqual(updated_photo.location, 'Updated Location')
        self.assertEqual(updated_photo.description, 'Updated Description')
        self.assertEqual(updated_photo.user, self.user)
