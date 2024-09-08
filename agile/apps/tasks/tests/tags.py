# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from apps.tasks.models import Tag
#
# class TagsListTestCase(APITestCase):
#     def setUp(self):
#         self.list_url = reverse('tag-list')
#         self.create_url = reverse('tag-create')
#
#     def test_get_empty_list_of_tags(self):
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#     def test_get_tags(self):
#         Tag.objects.create(name='Test Tag')
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_create_valid_tag(self):
#         data = {'name': 'New Tag'}
#         response = self.client.post(self.create_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['name'], 'New Tag')
#
#     def test_create_invalid_tag(self):
#         data = {}  # Invalid data
#         response = self.client.post(self.create_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_get_tag_by_id(self):
#         tag = Tag.objects.create(name='Existing Tag')
#         url = reverse('tag-detail', kwargs={'pk': tag.pk})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], 'Existing Tag')
#
#     def test_get_tag_by_id_not_found(self):
#         url = reverse('tag-detail', kwargs={'pk': 999})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_update_tag_with_valid_name(self):
#         tag = Tag.objects.create(name='Old Name')
#         url = reverse('tag-detail', kwargs={'pk': tag.pk})
#         data = {'name': 'Updated Name'}
#         response = self.client.patch(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], 'Updated Name')
#
#     def test_update_tag_with_invalid_name(self):
#         tag = Tag.objects.create(name='Valid Name')
#         url = reverse('tag-detail', kwargs={'pk': tag.pk})
#         data = {'name': ''}  # Invalid data
#         response = self.client.patch(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_delete_tag(self):
#         tag = Tag.objects.create(name='Tag to Delete')
#         url = reverse('tag-detail', kwargs={'pk': tag.pk})
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(Tag.objects.filter(pk=tag.pk).exists())