#!/usr/bin/env python
"""
Simple script to populate the Give Grip database with sample data.
Run this script from the project directory.
"""

import os
import sys
import django
from datetime import timedelta
from decimal import Decimal
import random

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'givegrip.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from campaigns.models import Campaign, Category, CampaignComment, CampaignShare, CampaignUpdate
from donations.models import Donation, DonationGoal, DonationMilestone
from payments.models import PaymentMethod, PaymentTransaction

User = get_user_model()

def create_categories():
    """Create sample campaign categories"""
    print("Creating campaign categories...")
    
    categories_data = [
        {'name': 'Education', 'description': 'Supporting educational initiatives and scholarships'},
        {'name': 'Healthcare', 'description': 'Medical care, research, and health-related causes'},
        {'name': 'Environment', 'description': 'Environmental conservation and climate action'},
        {'name': 'Poverty Relief', 'description': 'Helping communities overcome poverty'},
        {'name': 'Animal Welfare', 'description': 'Protecting and caring for animals'},
        {'name': 'Arts & Culture', 'description': 'Supporting creative and cultural projects'},
        {'name': 'Disaster Relief', 'description': 'Emergency response and recovery efforts'},
        {'name': 'Community Development', 'description': 'Building stronger communities'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        categories.append(category)
        if created:
            print(f'  ✓ Created category: {category.name}')
        else:
            print(f'  - Category already exists: {category.name}')
    
    return categories

def create_users():
    """Create sample users"""
    print("\nCreating sample users...")
    
    users_data = [
        {
            'username': 'john_doe',
            'email': 'john.doe@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '+1234567890',
        },
        {
            'username': 'jane_smith',
            'email': 'jane.smith@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone_number': '+1234567891',
        },
        {
            'username': 'mike_wilson',
            'email': 'mike.wilson@example.com',
            'first_name': 'Mike',
            'last_name': 'Wilson',
            'phone_number': '+1234567892',
        },
        {
            'username': 'sarah_jones',
            'email': 'sarah.jones@example.com',
            'first_name': 'Sarah',
            'last_name': 'Jones',
            'phone_number': '+1234567893',
        },
        {
            'username': 'david_brown',
            'email': 'david.brown@example.com',
            'first_name': 'David',
            'last_name': 'Brown',
            'phone_number': '+1234567894',
        },
    ]
    
    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f'  ✓ Created user: {user.username} (password: password123)')
        else:
            print(f'  - User already exists: {user.username}')
        users.append(user)
    
    return users

def create_campaigns(categories, users):
    """Create sample campaigns"""
    print("\nCreating sample campaigns...")
    
    campaigns_data = [
        {
            'title': 'Help Build a School in Rural India',
            'slug': 'help-build-school-rural-india',
            'description': 'We are raising funds to build a primary school in a remote village in India. This will provide education to over 200 children who currently have to walk 5+ km to the nearest school.',
            'short_description': 'Building a school for 200 children in rural India',
            'category': categories[0],  # Education
            'goal_amount': Decimal('25000.00'),
            'current_amount': Decimal('18750.00'),
            'status': 'active',
            'is_featured': True,
            'is_verified': True,
            'start_date': timezone.now() - timedelta(days=30),
            'end_date': timezone.now() + timedelta(days=60),
            'creator_name': f"{users[0].first_name} {users[0].last_name}",
            'creator_email': users[0].email,
            'creator_phone': users[0].phone_number,
            'story': 'Our mission is to provide quality education to children in rural areas who currently have limited access to schools.',
            'impact': 'Your donation will help build classrooms, provide furniture, and create a safe learning environment for children.',
        },
        {
            'title': 'Medical Equipment for Children\'s Hospital',
            'slug': 'medical-equipment-children-hospital',
            'description': 'Our local children\'s hospital needs new medical equipment to provide better care for young patients. We\'re raising funds for ventilators, monitors, and other essential equipment.',
            'short_description': 'Providing essential medical equipment for children\'s hospital',
            'category': categories[1],  # Healthcare
            'goal_amount': Decimal('50000.00'),
            'current_amount': Decimal('32500.00'),
            'status': 'active',
            'is_featured': True,
            'is_verified': True,
            'start_date': timezone.now() - timedelta(days=45),
            'end_date': timezone.now() + timedelta(days=45),
            'creator_name': f"{users[1].first_name} {users[1].last_name}",
            'creator_email': users[1].email,
            'creator_phone': users[1].phone_number,
            'story': 'We are working to improve healthcare outcomes for children by providing state-of-the-art medical equipment.',
            'impact': 'Your support will directly impact the quality of care we can provide to our youngest patients.',
        },
        {
            'title': 'Plant 10,000 Trees in Amazon Rainforest',
            'slug': 'plant-trees-amazon-rainforest',
            'description': 'Join us in reforesting the Amazon rainforest. Every dollar donated will plant one tree, helping to combat climate change and preserve biodiversity.',
            'short_description': 'Reforesting the Amazon rainforest to combat climate change',
            'category': categories[2],  # Environment
            'goal_amount': Decimal('10000.00'),
            'current_amount': Decimal('7500.00'),
            'status': 'active',
            'is_featured': False,
            'is_verified': True,
            'start_date': timezone.now() - timedelta(days=20),
            'end_date': timezone.now() + timedelta(days=70),
            'creator_name': f"{users[2].first_name} {users[2].last_name}",
            'creator_email': users[2].email,
            'creator_phone': users[2].phone_number,
            'story': 'We are committed to environmental conservation and fighting climate change through reforestation efforts.',
            'impact': 'Each tree planted will help absorb CO2 and restore the natural habitat for countless species.',
        },
        {
            'title': 'Emergency Food Bank Support',
            'slug': 'emergency-food-bank-support',
            'description': 'Our local food bank is running low on supplies and needs immediate support to help families in crisis. Every donation will provide meals for families in need.',
            'short_description': 'Supporting families in crisis through food bank assistance',
            'category': categories[3],  # Poverty Relief
            'goal_amount': Decimal('15000.00'),
            'current_amount': Decimal('12000.00'),
            'status': 'active',
            'is_featured': False,
            'is_verified': True,
            'start_date': timezone.now() - timedelta(days=15),
            'end_date': timezone.now() + timedelta(days=30),
            'creator_name': f"{users[3].first_name} {users[3].last_name}",
            'creator_email': users[3].email,
            'creator_phone': users[3].phone_number,
            'story': 'We are working to ensure no family goes hungry during these challenging times.',
            'impact': 'Your donation will provide nutritious meals to families facing food insecurity.',
        },
        {
            'title': 'Rescue and Rehabilitate Street Animals',
            'slug': 'rescue-rehabilitate-street-animals',
            'description': 'We rescue abandoned and injured street animals, provide medical care, and find them loving homes. Your support helps us save more lives.',
            'short_description': 'Rescuing and rehabilitating abandoned street animals',
            'category': categories[4],  # Animal Welfare
            'goal_amount': Decimal('8000.00'),
            'current_amount': Decimal('4800.00'),
            'status': 'active',
            'is_featured': False,
            'is_verified': True,
            'start_date': timezone.now() - timedelta(days=25),
            'end_date': timezone.now() + timedelta(days=55),
            'creator_name': f"{users[4].first_name} {users[4].last_name}",
            'creator_email': users[4].email,
            'creator_phone': users[4].phone_number,
            'story': 'We are dedicated to giving abandoned animals a second chance at life through rescue and rehabilitation.',
            'impact': 'Your support will help us provide medical care, food, and shelter to animals in need.',
        },
        {
            'title': 'Community Art Center for Youth',
            'slug': 'community-art-center-youth',
            'description': 'Building a creative space where young people can explore art, music, and theater. This center will provide free classes and workshops for underprivileged youth.',
            'short_description': 'Creating a creative space for youth to explore arts and culture',
            'category': categories[5],  # Arts & Culture
            'goal_amount': Decimal('35000.00'),
            'current_amount': Decimal('21000.00'),
            'status': 'active',
            'is_featured': True,
            'is_verified': True,
            'start_date': timezone.now() - timedelta(days=40),
            'end_date': timezone.now() + timedelta(days=50),
            'creator_name': f"{users[0].first_name} {users[0].last_name}",
            'creator_email': users[0].email,
            'creator_phone': users[0].phone_number,
            'story': 'We believe every child deserves access to creative expression and artistic opportunities.',
            'impact': 'Your donation will help create a space where young people can discover their artistic talents.',
        },
    ]
    
    campaigns = []
    for campaign_data in campaigns_data:
        campaign, created = Campaign.objects.get_or_create(
            slug=campaign_data['slug'],
            defaults=campaign_data
        )
        campaigns.append(campaign)
        if created:
            print(f'  ✓ Created campaign: {campaign.title}')
        else:
            print(f'  - Campaign already exists: {campaign.title}')
    
    return campaigns

def create_donations(campaigns, users):
    """Create sample donations"""
    print("\nCreating sample donations...")
    
    donation_amounts = [25, 50, 100, 250, 500, 1000, 2500]
    total_donations = 0
    
    for campaign in campaigns:
        # Create 5-15 donations per campaign
        num_donations = random.randint(5, 15)
        
        for i in range(num_donations):
            donor = random.choice(users)
            amount = Decimal(str(random.choice(donation_amounts)))
            is_anonymous = random.choice([True, False])
            
            donation = Donation.objects.create(
                campaign=campaign,
                donor=donor,
                amount=amount,
                message=f'Keep up the great work! #{i+1}' if not is_anonymous else '',
                is_anonymous=is_anonymous,
                status='completed',
                payment_method='stripe',
                created_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            total_donations += 1
    
    print(f'  ✓ Created {total_donations} donations')

def create_payment_methods(users):
    """Create sample payment methods"""
    print("\nCreating sample payment methods...")
    
    payment_types = ['card', 'bank_account', 'paypal', 'wallet']
    card_brands = ['Visa', 'Mastercard', 'American Express', 'Discover']
    total_methods = 0
    
    for user in users:
        # Create 1-2 payment methods per user
        num_methods = random.randint(1, 2)
        
        for i in range(num_methods):
            payment_type = random.choice(payment_types)
            
            if payment_type == 'card':
                brand = random.choice(card_brands)
                last_four = str(random.randint(1000, 9999))
                payment_method = PaymentMethod.objects.create(
                    user=user,
                    payment_type=payment_type,
                    token=f'tok_{user.id}_{i}_{random.randint(1000, 9999)}',
                    last_four=last_four,
                    brand=brand,
                    expiry_month=str(random.randint(1, 12)).zfill(2),
                    expiry_year=str(random.randint(2025, 2030)),
                    is_default=i == 0,  # First method is default
                    is_active=True
                )
            else:
                payment_method = PaymentMethod.objects.create(
                    user=user,
                    payment_type=payment_type,
                    token=f'tok_{user.id}_{i}_{random.randint(1000, 9999)}',
                    is_default=i == 0,
                    is_active=True
                )
            total_methods += 1
    
    print(f'  ✓ Created {total_methods} payment methods')

def create_campaign_interactions(campaigns, users):
    """Create sample comments, shares, and updates"""
    print("\nCreating campaign interactions...")
    
    # Create comments
    comment_messages = [
        'This is such an important cause!',
        'Keep up the amazing work!',
        'I\'m so happy to support this project.',
        'This will make a real difference.',
        'Thank you for organizing this campaign.',
        'I shared this with my friends and family.',
        'Can\'t wait to see the results!',
        'This is exactly what our community needs.',
    ]
    
    total_comments = 0
    total_updates = 0
    total_shares = 0
    
    for campaign in campaigns:
        # Create 3-8 comments per campaign
        num_comments = random.randint(3, 8)
        
        for i in range(num_comments):
            commenter = random.choice(users)
            message = random.choice(comment_messages)
            
            CampaignComment.objects.create(
                campaign=campaign,
                user=commenter,
                content=message,
                created_at=timezone.now() - timedelta(days=random.randint(1, 25))
            )
            total_comments += 1
        
        # Create 1-3 updates per campaign
        num_updates = random.randint(1, 3)
        
        for i in range(num_updates):
            CampaignUpdate.objects.create(
                campaign=campaign,
                title=f'Update #{i+1}',
                content=f'Here\'s what we\'ve accomplished so far! We\'re making great progress and your support is making a real difference.',
                created_at=timezone.now() - timedelta(days=random.randint(1, 20))
            )
            total_updates += 1
        
        # Create some shares
        num_shares = random.randint(5, 15)
        
        for i in range(num_shares):
            sharer = random.choice(users)
            platform = random.choice(['facebook', 'twitter', 'instagram', 'linkedin'])
            
            CampaignShare.objects.create(
                campaign=campaign,
                platform=platform,
                user=sharer,
                created_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            total_shares += 1
    
    print(f'  ✓ Created {total_comments} comments')
    print(f'  ✓ Created {total_updates} updates')
    print(f'  ✓ Created {total_shares} shares')

def main():
    """Main function to populate the database"""
    print("🚀 Starting to populate Give Grip database with sample data...")
    print("=" * 60)
    
    try:
        # Create sample categories
        categories = create_categories()
        
        # Create sample users
        users = create_users()
        
        # Create sample campaigns
        campaigns = create_campaigns(categories, users)
        
        # Create sample donations
        create_donations(campaigns, users)
        
        # Create sample payment methods
        create_payment_methods(users)
        
        # Create sample campaign interactions
        create_campaign_interactions(campaigns, users)
        
        print("\n" + "=" * 60)
        print("✅ Successfully populated database with sample data!")
        print("\n📊 Summary:")
        print(f"  • {Category.objects.count()} campaign categories")
        print(f"  • {User.objects.count()} users")
        print(f"  • {Campaign.objects.count()} campaigns")
        print(f"  • {Donation.objects.count()} donations")
        print(f"  • {PaymentMethod.objects.count()} payment methods")
        print(f"  • {CampaignComment.objects.count()} comments")
        print(f"  • {CampaignUpdate.objects.count()} updates")
        print(f"  • {CampaignShare.objects.count()} shares")
        
        print("\n🔑 Sample User Credentials:")
        print("  • Username: john_doe, Password: password123")
        print("  • Username: jane_smith, Password: password123")
        print("  • Username: mike_wilson, Password: password123")
        print("  • Username: sarah_jones, Password: password123")
        print("  • Username: david_brown, Password: password123")
        
        print("\n🌐 You can now:")
        print("  • Visit http://127.0.0.1:8000/admin/ to view the data")
        print("  • Login with any of the sample users above")
        print("  • Explore campaigns and donations")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()




