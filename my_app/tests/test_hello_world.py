import django
from django.test import TestCase


class HelloWorldTest(TestCase):
    def test_hello_world(self):
        self.assertEqual("Hello, World!", "Hello, World!")

    def test_hello_world2(self):
        self.assertEqual("Hello, World!", "Hello, World!")
