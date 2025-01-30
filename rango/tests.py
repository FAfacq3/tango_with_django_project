from django.test import TestCase
from rango.models import Category
from django.urls import reverse
from rango.forms import CategoryForm

class CategoryModelTest(TestCase):

    def test_category_creation(self):
        category = Category.objects.create(name="Test Category", likes=5)
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.likes, 5)

class IndexViewTest(TestCase):

    def test_index_page_loads(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Rango")

class AddCategoryViewTest(TestCase):

    def test_add_category_form(self):
        form = CategoryForm(data={'name': 'New Category'})
        self.assertTrue(form.is_valid())

    def test_add_category_view(self):
        response = self.client.post(reverse('add_category'), {'name': 'Test Category'})
        self.assertEqual(response.status_code, 302)  # 302 = 重定向成功