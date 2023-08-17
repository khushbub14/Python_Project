from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskCRUDTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some tasks for testing
        Task.objects.create(title='Task 1', completed=False)
        Task.objects.create(title='Task 2', completed=True)

    def test_create_task(self):
        url = reverse('task-create')
        data = {'title': 'New Task', 'completed': False}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Ensure the correct status code
        self.assertEqual(Task.objects.count(), 3)  # Ensure the new task is created

   

    def test_read_task_list(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Ensure we get a list of two tasks

    def test_read_task_detail(self):
        task = Task.objects.first()
        url = reverse('task-detail', args=[task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], task.title)  # Ensure the correct task is retrieved

    def test_update_task(self):
        task = Task.objects.first()
        url = reverse('task-update', args=[task.pk])
        data = {'title': 'Updated Task', 'completed': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')  # Ensure the task is updated

    def test_delete_task(self):
        task = Task.objects.first()
        url = reverse('task-delete', args=[task.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 1)  # Ensure the task is deleted

