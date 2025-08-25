from django.core.management.base import BaseCommand
from django.utils import timezone
from pages.models import (
    SiteSettings, Statistics, Feature, Testimonial, FAQ, 
    Banner, PageContent, LegalDocument
)
from datetime import timedelta


class Command(BaseCommand):
    help = 'Set up the CMS with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up CMS with initial data...')
        
        # Create site settings
        settings, created = SiteSettings.objects.get_or_create(
            pk=1,
                    defaults={
            'site_name': 'GiveGrip',
            'site_tagline': 'Make a Difference Through Crowdfunding',
            'site_description': 'Empowering communities through crowdfunding. Make a difference in someone\'s life today.',
            'contact_email': 'support@givegrip.com',
            'contact_phone': '+1 (555) 123-4567',
            'contact_address': '123 Charity Way, Suite 100\nNew York, NY 10001',
            'currency_code': 'INR',
            'currency_symbol': '₹',
            'primary_color': '#2563eb',
            'secondary_color': '#059669',
            'accent_color': '#f59e0b',
        }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Site settings created'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ Site settings already exist'))
        
        # Create statistics
        try:
            statistics_data = [
                {
                    'title': 'Active Donors',
                    'value': '50K',
                    'suffix': '+',
                    'icon': 'fas fa-users',
                    'color': '#2563eb',
                    'show_on_homepage': True,
                    'order': 1
                },
                {
                    'title': 'Successful Campaigns',
                    'value': '1,200',
                    'suffix': '+',
                    'icon': 'fas fa-heart',
                    'color': '#059669',
                    'show_on_homepage': True,
                    'order': 2
                },
                {
                    'title': 'Total Raised',
                    'value': '18.5Cr',
                    'suffix': '+',
                    'icon': 'fas fa-rupee-sign',
                    'color': '#f59e0b',
                    'show_on_homepage': True,
                    'order': 3
                },
                {
                    'title': 'Countries Served',
                    'value': '45',
                    'suffix': '+',
                    'icon': 'fas fa-globe',
                    'color': '#06b6d4',
                    'show_on_homepage': True,
                    'order': 4
                }
            ]
            
            for stat_data in statistics_data:
                stat, created = Statistics.objects.get_or_create(
                    title=stat_data['title'],
                    defaults=stat_data
                )
                if created:
                    self.stdout.write(f'✓ Created statistic: {stat.title}')
        except Exception as e:
            self.stdout.write(f'⚠ Skipping statistics creation: {e}')
        
        # Create features
        try:
            features_data = [
                {
                    'title': 'Discover',
                    'description': 'Browse through our verified campaigns and find a cause that resonates with your heart.',
                    'icon': 'fas fa-search',
                    'show_on_homepage': True,
                    'order': 1
                },
                {
                    'title': 'Donate',
                    'description': 'Choose your amount and make a secure donation. Every contribution makes a difference.',
                    'icon': 'fas fa-heart',
                    'show_on_homepage': True,
                    'order': 2
                },
                {
                    'title': 'Impact',
                    'description': 'Track the progress of campaigns and see the real impact of your donation.',
                    'icon': 'fas fa-smile',
                    'show_on_homepage': True,
                    'order': 3
                }
            ]
            
            for feature_data in features_data:
                feature, created = Feature.objects.get_or_create(
                    title=feature_data['title'],
                    defaults=feature_data
                )
                if created:
                    self.stdout.write(f'✓ Created feature: {feature.title}')
        except Exception as e:
            self.stdout.write(f'⚠ Skipping features creation: {e}')
        
        # Create testimonials
        try:
            testimonials_data = [
                {
                    'name': 'Sarah Johnson',
                    'role': 'Regular Donor',
                    'company': 'Community Volunteer',
                    'content': 'GiveGrip has made it so easy to support causes I care about. The transparency and impact tracking are amazing!',
                    'rating': 5,
                    'is_featured': True,
                    'order': 1
                },
                {
                    'name': 'Michael Chen',
                    'role': 'Campaign Creator',
                    'company': 'Local NGO',
                    'content': 'We raised funds for our community project in record time. The platform is user-friendly and trustworthy.',
                    'rating': 5,
                    'is_featured': True,
                    'order': 2
                },
                {
                    'name': 'Priya Patel',
                    'role': 'Social Worker',
                    'company': 'Healthcare Foundation',
                    'content': 'The support we received through GiveGrip helped us provide medical care to hundreds of families.',
                    'rating': 5,
                    'is_featured': True,
                    'order': 3
                }
            ]
            
            for testimonial_data in testimonials_data:
                testimonial, created = Testimonial.objects.get_or_create(
                    name=testimonial_data['name'],
                    defaults=testimonial_data
                )
                if created:
                    self.stdout.write(f'✓ Created testimonial: {testimonial.name}')
        except Exception as e:
            self.stdout.write(f'⚠ Skipping testimonials creation: {e}')
        
        # Create FAQs
        try:
            faqs_data = [
                {
                    'question': 'How do I make a donation?',
                    'answer': 'Making a donation is easy! Simply browse our campaigns, choose one you\'d like to support, click "Donate Now," and follow the secure payment process.',
                    'category': 'Donations',
                    'order': 1
                },
                {
                    'question': 'Is my donation secure?',
                    'answer': 'Absolutely! We use bank-level security with SSL encryption and PCI compliance. Your financial information is never stored on our servers.',
                    'category': 'Security',
                    'order': 2
                },
                {
                    'question': 'Can I make anonymous donations?',
                    'answer': 'Yes, you can choose to make anonymous donations. Your name won\'t be displayed publicly, but we\'ll still send you a receipt for tax purposes.',
                    'category': 'Privacy',
                    'order': 3
                },
                {
                    'question': 'How do I get a receipt for my donation?',
                    'answer': 'You\'ll receive an email receipt immediately after your donation is processed. You can also access all your donation receipts in your account dashboard.',
                    'category': 'Receipts',
                    'order': 4
                },
                {
                    'question': 'What payment methods do you accept?',
                    'answer': 'We accept all major credit cards (Visa, MasterCard, American Express, Discover), UPI, net banking, and digital wallets for Indian users.',
                    'category': 'Payments',
                    'order': 5
                },
                {
                    'question': 'How do I know my donation reaches the intended cause?',
                    'answer': 'We provide real-time updates and detailed reporting on how funds are used. You can track the progress of campaigns and see the impact of your donation.',
                    'category': 'Transparency',
                    'order': 6
                }
            ]
            
            for faq_data in faqs_data:
                faq, created = FAQ.objects.get_or_create(
                    question=faq_data['question'],
                    defaults=faq_data
                )
                if created:
                    self.stdout.write(f'✓ Created FAQ: {faq.question}')
        except Exception as e:
            self.stdout.write(f'⚠ Skipping FAQs creation: {e}')
        
        # Create a sample banner
        try:
            banner, created = Banner.objects.get_or_create(
                title='Welcome to GiveGrip',
                defaults={
                    'message': 'Join thousands of people making a difference through crowdfunding!',
                    'banner_type': 'info',
                    'show_on_homepage': True,
                    'start_date': timezone.now(),
                    'end_date': timezone.now() + timedelta(days=30)
                }
            )
            if created:
                self.stdout.write('✓ Created welcome banner')
        except Exception as e:
            self.stdout.write(f'⚠ Skipping banner creation: {e}')
        
        # Create legal documents
        try:
            legal_docs = [
                {
                    'title': 'Privacy Policy',
                    'document_type': 'privacy_policy',
                    'content': 'This Privacy Policy describes how GiveGrip collects, uses, and protects your personal information...',
                    'version': '1.0',
                    'effective_date': timezone.now().date()
                },
                {
                    'title': 'Terms of Service',
                    'document_type': 'terms_of_service',
                    'content': 'By using GiveGrip, you agree to these terms and conditions...',
                    'version': '1.0',
                    'effective_date': timezone.now().date()
                }
            ]
            
            for doc_data in legal_docs:
                doc, created = LegalDocument.objects.get_or_create(
                    document_type=doc_data['document_type'],
                    defaults=doc_data
                )
                if created:
                    self.stdout.write(f'✓ Created legal document: {doc.title}')
        except Exception as e:
            self.stdout.write(f'⚠ Skipping legal documents creation: {e}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ CMS setup completed successfully!'))
        self.stdout.write('You can now access the admin panel to customize your website content.')
