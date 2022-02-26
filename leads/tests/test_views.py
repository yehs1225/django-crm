from django.test import TestCase
from django.shortcuts import reverse

class LandingPageTest(TestCase):
    
    def test_get(self):
        response = self.client.get(reverse("landing-page"))
        # TO test status code
        self.assertEqual(response.status_code,200)
        # TO test template code
        self.assertTemplateUsed(response,"landing.html")
