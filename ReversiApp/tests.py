from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
class SanityCheck(TestCase):
    def setUp(self):
        pass

    def when_running_tests__should_pass_this_test(self):
        self.assertTrue(False)