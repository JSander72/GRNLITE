from django.test import TestCase
from manuscripts.models import Manuscript


class ManuscriptModelTest(TestCase):
    def test_manuscript_creation(self):
        manuscript = Manuscript.objects.create(
            title="Test Manuscript", description="Test Description"
        )
        self.assertEqual(manuscript.title, "Test Manuscript")
