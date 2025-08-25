from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Fix database schema issues'

    def handle(self, *args, **options):
        self.stdout.write('Fixing database schema...')
        
        with connection.cursor() as cursor:
            # Check if newsletter_subscription column exists in pages_contactmessage
            cursor.execute("PRAGMA table_info(pages_contactmessage)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'newsletter_subscription' not in columns:
                self.stdout.write('Adding newsletter_subscription column to pages_contactmessage...')
                cursor.execute("""
                    ALTER TABLE pages_contactmessage 
                    ADD COLUMN newsletter_subscription BOOLEAN DEFAULT 0
                """)
                self.stdout.write(self.style.SUCCESS('✓ Added newsletter_subscription column'))
            else:
                self.stdout.write('✓ newsletter_subscription column already exists')
            
            # Check if currency_code column exists in pages_sitesettings
            cursor.execute("PRAGMA table_info(pages_sitesettings)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Add missing columns to pages_sitesettings
            missing_columns = [
                ('currency_code', 'VARCHAR(3) DEFAULT "INR"'),
                ('currency_symbol', 'VARCHAR(5) DEFAULT "₹"'),
                ('currency_position', 'VARCHAR(10) DEFAULT "before"'),
                ('default_currency', 'VARCHAR(3) DEFAULT "INR"'),
                ('primary_color', 'VARCHAR(7) DEFAULT "#2563eb"'),
                ('secondary_color', 'VARCHAR(7) DEFAULT "#059669"'),
                ('accent_color', 'VARCHAR(7) DEFAULT "#f59e0b"'),
                ('meta_title', 'VARCHAR(60) DEFAULT "GiveGrip - Make a Difference Through Crowdfunding"'),
                ('meta_description', 'TEXT DEFAULT "Join thousands of people helping others through crowdfunding. Every donation counts, every story matters."'),
                ('meta_keywords', 'TEXT'),
                ('google_analytics_id', 'VARCHAR(20)'),
                ('facebook_pixel_id', 'VARCHAR(20)'),
                ('enable_registration', 'BOOLEAN DEFAULT 1'),
                ('enable_social_login', 'BOOLEAN DEFAULT 0'),
                ('enable_newsletter', 'BOOLEAN DEFAULT 1'),
                ('enable_live_chat', 'BOOLEAN DEFAULT 1'),
                ('enable_testimonials', 'BOOLEAN DEFAULT 1'),
                ('enable_faq', 'BOOLEAN DEFAULT 1'),
                ('max_campaign_duration', 'INTEGER DEFAULT 90'),
                ('min_donation_amount', 'DECIMAL(10,2) DEFAULT 1.00'),
                ('max_donation_amount', 'DECIMAL(10,2) DEFAULT 100000.00'),
                ('email_notifications', 'BOOLEAN DEFAULT 1'),
                ('sms_notifications', 'BOOLEAN DEFAULT 0'),
                ('push_notifications', 'BOOLEAN DEFAULT 0'),
                ('enable_captcha', 'BOOLEAN DEFAULT 0'),
                ('require_email_verification', 'BOOLEAN DEFAULT 1'),
                ('require_phone_verification', 'BOOLEAN DEFAULT 0'),
                ('maintenance_mode', 'BOOLEAN DEFAULT 0'),
                ('maintenance_message', 'TEXT DEFAULT "We are currently performing maintenance. Please check back soon."'),
            ]
            
            for column_name, column_def in missing_columns:
                if column_name not in columns:
                    self.stdout.write(f'Adding {column_name} column to pages_sitesettings...')
                    cursor.execute(f"""
                        ALTER TABLE pages_sitesettings 
                        ADD COLUMN {column_name} {column_def}
                    """)
                    self.stdout.write(self.style.SUCCESS(f'✓ Added {column_name} column'))
                else:
                    self.stdout.write(f'✓ {column_name} column already exists')
        
        self.stdout.write(self.style.SUCCESS('✓ Database schema fixed successfully!'))
