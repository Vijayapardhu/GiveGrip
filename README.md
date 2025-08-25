# GiveGrip - Fundraising Platform

A comprehensive Django-based fundraising platform that allows users to create campaigns, make donations, and track progress in real-time.

## Features

### Core Functionality
- **User Authentication**: Secure registration, login, and profile management
- **Campaign Management**: Create, edit, and manage fundraising campaigns
- **Donation Processing**: Secure payment processing with Razorpay integration
- **Real-time Tracking**: Monitor campaign progress and donor statistics
- **Content Management**: Dynamic content management system for site pages

### User Features
- User registration and authentication
- Profile management with avatar upload
- Campaign creation and management
- Donation history tracking
- Anonymous donation options
- Social sharing capabilities

### Campaign Features
- Campaign creation with rich media support
- Goal setting and progress tracking
- Category-based organization
- Featured campaign highlighting
- Campaign statistics and analytics

### Payment Integration
- Razorpay payment gateway integration
- Secure payment processing
- Webhook handling for payment verification
- Multiple currency support

### Admin Features
- Comprehensive admin dashboard
- Campaign moderation tools
- User management
- Payment tracking
- Content management system

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Payment**: Razorpay API
- **Authentication**: Django Allauth
- **Forms**: Django Crispy Forms with Bootstrap 5
- **API**: Django REST Framework

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vijayapardhu/GiveGrip.git
   cd GiveGrip
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   RAZORPAY_KEY_ID=your-razorpay-key
   RAZORPAY_KEY_SECRET=your-razorpay-secret
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
GiveGrip/
├── accounts/                 # User authentication and profiles
├── campaigns/               # Campaign management
├── donations/               # Donation processing
├── payments/                # Payment gateway integration
├── pages/                   # Static pages and CMS
├── givegrip/                # Main project settings
├── templates/               # HTML templates
├── static/                  # CSS, JS, and images
├── management/              # Custom management commands
└── requirements.txt         # Python dependencies
```

## Apps Overview

### Accounts App
- Custom User model with extended fields
- Phone verification system
- Profile management
- Authentication views

### Donations App
- Campaign model with rich features
- Donation processing
- Progress tracking
- Statistics and analytics

### Payments App
- Razorpay integration
- Payment webhook handling
- Order management
- Payment verification

### Pages App
- Content Management System (CMS)
- Static page management
- FAQ management
- Site settings

## API Endpoints

The project includes REST API endpoints for:
- User management
- Campaign CRUD operations
- Donation processing
- Payment verification

## Customization

### Content Management
The platform includes a comprehensive CMS allowing customization of:
- Site settings and branding
- Static page content
- FAQ management
- Legal documents
- Testimonials

### Styling
- Bootstrap 5 based responsive design
- Custom CSS variables for easy theming
- Modular CSS structure
- Mobile-first approach

## Deployment

### Production Settings
1. Set `DEBUG=False`
2. Configure production database
3. Set up static file serving
4. Configure email settings
5. Set up SSL certificates

### Environment Variables
Required environment variables for production:
- `SECRET_KEY`
- `DATABASE_URL`
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`
- `EMAIL_HOST`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Email: support@givegrip.com
- Documentation: [Link to documentation]
- Issues: [GitHub Issues](https://github.com/Vijayapardhu/GiveGrip/issues)

## Roadmap

- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Mobile app development
- [ ] Social media integration
- [ ] Recurring donations
- [ ] Team fundraising features
- [ ] Advanced payment gateways
- [ ] Email marketing integration
