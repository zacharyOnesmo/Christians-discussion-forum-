from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserAuthFlowTests(TestCase):
    def test_login_page_is_available(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_is_available(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_access_dashboard(self):
        user = get_user_model().objects.create_user(username='mwanafunzi', email='mwanafunzi@example.com', password='secret123')
        self.client.login(username='mwanafunzi', password='secret123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, 'mwanafunzi')

    def test_unauthenticated_user_redirects_to_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_csrf_trusted_origins_include_dev_preview_hosts(self):
        self.assertIn('https://*.app.github.dev', settings.CSRF_TRUSTED_ORIGINS)
        self.assertIn('https://*.preview.app.github.dev', settings.CSRF_TRUSTED_ORIGINS)

    def test_authenticated_user_can_view_profile_with_claim_history(self):
        user = get_user_model().objects.create_user(username='profileuser', email='profile@example.com', password='secret123')
        self.client.login(username='profileuser', password='secret123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'profileuser')
        self.assertContains(response, 'My investigations')

    def test_authenticated_user_can_view_individual_claim_detail(self):
        user = get_user_model().objects.create_user(username='claimviewer', email='claimviewer@example.com', password='secret123')
        claim = user.claims.create(
            claim='666 is a brain chip',
            language='en',
            category='technology',
            status='interpretation',
            confidence=0.45,
        )
        self.client.login(username='claimviewer', password='secret123')
        response = self.client.get(f"{reverse('claim_detail', args=[claim.pk])}?lang=en")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '666 is a brain chip')
        self.assertContains(response, 'Claim details')
