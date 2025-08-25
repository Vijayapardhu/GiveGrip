from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create sample users
        users = []
        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                defaults={
                    'email': f'user{i}@example.com',
                    'first_name': f'User{i}',
                    'last_name': 'Example',
                    'is_active': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
            self.stdout.write(f'Created user: {user.username}')

        # Import models here to avoid circular imports
        try:
            from donations.models import Campaign, Donation
            from pages.models import SiteSettings, FAQ, Testimonial
            
            # Create site settings
            site_settings, created = SiteSettings.objects.get_or_create(
                defaults={
                    'site_name': 'GiveGrip',
                    'site_description': 'Empowering change through crowdfunding',
                    'contact_email': 'contact@givegrip.com',
                    'contact_phone': '+1-555-0123',
                    'address': '123 Fundraising Street, Charity City, CC 12345',
                    'facebook_url': 'https://facebook.com/givegrip',
                    'twitter_url': 'https://twitter.com/givegrip',
                    'instagram_url': 'https://instagram.com/givegrip',
                    'linkedin_url': 'https://linkedin.com/company/givegrip',
                    'youtube_url': 'https://youtube.com/givegrip'
                }
            )
            if created:
                self.stdout.write('Created site settings')

            # Create sample campaigns
            campaign_data = [
                {
                    'title': 'Help Sarah Beat Cancer',
                    'description': 'Sarah needs your help to cover medical expenses for her cancer treatment.',
                    'category': 'Medical',
                    'goal_amount': Decimal('50000.00'),
                    'currency': 'USD'
                },
                {
                    'title': 'Build a School in Rural India',
                    'description': 'Help us build a school to provide education to underprivileged children.',
                    'category': 'Education',
                    'goal_amount': Decimal('25000.00'),
                    'currency': 'USD'
                },
                {
                    'title': 'Emergency Relief for Flood Victims',
                    'description': 'Provide immediate relief to families affected by recent floods.',
                    'category': 'Emergency',
                    'goal_amount': Decimal('15000.00'),
                    'currency': 'USD'
                },
                {
                    'title': 'Animal Shelter Renovation',
                    'description': 'Help us renovate our animal shelter to provide better care for rescued animals.',
                    'category': 'Animals',
                    'goal_amount': Decimal('10000.00'),
                    'currency': 'USD'
                },
                {
                    'title': 'Community Garden Project',
                    'description': 'Create a community garden to provide fresh produce to local families.',
                    'category': 'Community',
                    'goal_amount': Decimal('8000.00'),
                    'currency': 'USD'
                }
            ]

            campaigns = []
            for i, data in enumerate(campaign_data):
                campaign, created = Campaign.objects.get_or_create(
                    title=data['title'],
                    defaults={
                        'creator': users[i % len(users)],
                        'description': data['description'],
                        'story': f"This is a detailed story about {data['title']}. " + 
                                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " +
                                "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                        'category': data['category'],
                        'goal_amount': data['goal_amount'],
                        'collected_amount': Decimal(str(random.randint(1000, int(data['goal_amount'] * 0.8)))),
                        'currency': data['currency'],
                        'status': 'active',
                        'is_featured': i < 2,  # First two campaigns are featured
                        'start_date': timezone.now().date() - timedelta(days=random.randint(1, 30)),
                        'end_date': timezone.now().date() + timedelta(days=random.randint(30, 90)),
                        'view_count': random.randint(100, 1000),
                        'share_count': random.randint(10, 100),
                        'donor_count': random.randint(5, 50)
                    }
                )
                if created:
                    campaigns.append(campaign)
                    self.stdout.write(f'Created campaign: {campaign.title}')

            # Create sample donations
            for campaign in campaigns:
                for i in range(random.randint(3, 8)):
                    donor = random.choice(users)
                    amount = Decimal(str(random.randint(10, 500)))
                    
                    donation = Donation.objects.create(
                        campaign=campaign,
                        donor=donor,
                        amount=amount,
                        currency=campaign.currency,
                        status='paid',
                        is_anonymous=random.choice([True, False]),
                        donor_name=donor.get_full_name() if not random.choice([True, False]) else '',
                        donor_message=random.choice([
                            'Keep up the great work!',
                            'Hope this helps!',
                            'Sending positive vibes!',
                            'You\'re doing amazing things!',
                            ''
                        ])
                    )
                    self.stdout.write(f'Created donation: ${amount} for {campaign.title}')

            # Create sample FAQs
            faq_data = [
                {
                    'question': 'How do I create a campaign?',
                    'answer': 'To create a campaign, simply click on "Create Campaign" and fill out the required information including your goal amount, story, and timeline.'
                },
                {
                    'question': 'What payment methods are accepted?',
                    'answer': 'We accept all major credit cards, debit cards, and digital wallets through our secure payment processor.'
                },
                {
                    'question': 'Are there any fees?',
                    'answer': 'We charge a small processing fee of 2.9% + $0.30 per donation to cover payment processing costs.'
                },
                {
                    'question': 'Can I make anonymous donations?',
                    'answer': 'Yes, you can choose to make anonymous donations. Your name will not be displayed publicly.'
                },
                {
                    'question': 'How do I track my campaign progress?',
                    'answer': 'You can track your campaign progress in real-time through your dashboard, which shows current donations, donor count, and progress towards your goal.'
                }
            ]

            for faq in faq_data:
                FAQ.objects.get_or_create(
                    question=faq['question'],
                    defaults={
                        'answer': faq['answer'],
                        'is_active': True,
                        'order': random.randint(1, 10)
                    }
                )
            self.stdout.write('Created sample FAQs')

            # Create sample testimonials
            testimonial_data = [
                {
                    'name': 'John Smith',
                    'role': 'Campaign Creator',
                    'content': 'GiveGrip helped me raise funds for my medical treatment. The platform is easy to use and the support team is amazing!'
                },
                {
                    'name': 'Sarah Johnson',
                    'role': 'Donor',
                    'content': 'I love how transparent GiveGrip is. I can see exactly where my donations are going and the impact they\'re making.'
                },
                {
                    'name': 'Mike Davis',
                    'role': 'Non-profit Director',
                    'content': 'GiveGrip has revolutionized our fundraising efforts. We\'ve been able to reach more donors and raise more funds than ever before.'
                }
            ]

            for testimonial in testimonial_data:
                Testimonial.objects.get_or_create(
                    name=testimonial['name'],
                    defaults={
                        'role': testimonial['role'],
                        'content': testimonial['content'],
                        'is_active': True,
                        'rating': random.randint(4, 5)
                    }
                )
            self.stdout.write('Created sample testimonials')

        except ImportError as e:
            self.stdout.write(self.style.WARNING(f'Some models could not be imported: {e}'))
            self.stdout.write('Created users only')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write(f'Created {len(users)} users')
        if 'campaigns' in locals():
            self.stdout.write(f'Created {len(campaigns)} campaigns')
            self.stdout.write('Created sample donations, FAQs, and testimonials')


