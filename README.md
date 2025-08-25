# GiveGrip - Donation Platform

A modern, feature-rich donation platform built with Django that enables individuals and organizations to create fundraising campaigns and accept donations securely.

![GiveGrip Logo](https://img.shields.io/badge/GiveGrip-Donation%20Platform-blue?style=for-the-badge&logo=django)
![Django](https://img.shields.io/badge/Django-4.2.7-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=for-the-badge&logo=bootstrap)

## 🌟 Live Demo

**Production Site**: [https://givegrip.onrender.com](https://givegrip.onrender.com)

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🎯 Core Features
- **Campaign Management**: Create, edit, and manage fundraising campaigns
- **Secure Donations**: Multiple payment gateway integrations (Razorpay, Stripe, PayPal)
- **User Authentication**: Complete user registration, login, and profile management
- **Real-time Tracking**: Live donation tracking and campaign progress
- **Responsive Design**: Mobile-first, modern UI/UX design
- **Admin Dashboard**: Comprehensive admin panel for content management

### 🎨 User Features
- **User Profiles**: Personalized user dashboards with donation history
- **Campaign Discovery**: Browse and search campaigns by category
- **Social Sharing**: Share campaigns on social media platforms
- **Email Notifications**: Automated email notifications for donations
- **Progress Tracking**: Real-time campaign progress visualization

### 🛠️ Admin Features
- **Content Management System (CMS)**: Dynamic content management
- **Analytics Dashboard**: Campaign performance and donation analytics
- **User Management**: Complete user account management
- **Payment Management**: Payment gateway configuration and monitoring
- **Site Settings**: Customizable site configuration

### 💳 Payment Features
- **Multiple Gateways**: Razorpay, Stripe, and PayPal integration
- **Secure Transactions**: SSL encryption and secure payment processing
- **Payment History**: Complete transaction history and receipts
- **Refund Management**: Automated refund processing

## 🛠️ Technology Stack

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **PostgreSQL/SQLite**: Database
- **Celery**: Background task processing
- **Redis**: Caching and message broker

### Frontend
- **Bootstrap 5**: CSS framework
- **FontAwesome**: Icons
- **JavaScript**: Interactive features
- **Responsive Design**: Mobile-first approach

### Payment Gateways
- **Razorpay**: Primary payment gateway (India)
- **Stripe**: International payments
- **PayPal**: Alternative payment option

### Deployment
- **Render.com**: Hosting platform
- **Gunicorn**: WSGI server
- **Whitenoise**: Static file serving
- **PostgreSQL**: Production database

## 🚀 Installation

### Prerequisites
- Python 3.11+
- pip
- Git

### Local Development Setup

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

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py setup_cms
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Payment Gateways
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
STRIPE_PUBLISHABLE_KEY=your-stripe-key
STRIPE_SECRET_KEY=your-stripe-secret
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-secret

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
```

### Payment Gateway Setup

1. **Razorpay** (Recommended for India)
   - Sign up at [razorpay.com](https://razorpay.com)
   - Get API keys from dashboard
   - Configure webhook endpoints

2. **Stripe** (International)
   - Sign up at [stripe.com](https://stripe.com)
   - Get API keys from dashboard
   - Configure webhook endpoints

3. **PayPal** (Alternative)
   - Sign up at [paypal.com](https://paypal.com)
   - Get client credentials
   - Configure webhook endpoints

## 📖 Usage

### For Users

1. **Register/Login**: Create an account or login
2. **Browse Campaigns**: Explore fundraising campaigns
3. **Make Donations**: Support causes with secure payments
4. **Track Progress**: Monitor campaign progress
5. **Manage Profile**: Update personal information

### For Campaign Creators

1. **Create Campaign**: Set up fundraising campaign
2. **Add Details**: Include description, images, goals
3. **Share Campaign**: Promote on social media
4. **Monitor Progress**: Track donations and progress
5. **Withdraw Funds**: Access raised funds

### For Administrators

1. **Access Admin Panel**: `/admin/`
2. **Manage Content**: Update site content via CMS
3. **Monitor Campaigns**: Review and approve campaigns
4. **User Management**: Manage user accounts
5. **Analytics**: View donation and user analytics

## 🔌 API Documentation

### Authentication Endpoints

```http
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
GET /api/auth/profile/
```

### Campaign Endpoints

```http
GET /api/campaigns/
POST /api/campaigns/
GET /api/campaigns/{id}/
PUT /api/campaigns/{id}/
DELETE /api/campaigns/{id}/
```

### Donation Endpoints

```http
GET /api/donations/
POST /api/donations/
GET /api/donations/{id}/
```

### Example API Usage

```python
import requests

# Get all campaigns
response = requests.get('https://givegrip.onrender.com/api/campaigns/')
campaigns = response.json()

# Create a donation
donation_data = {
    'campaign_id': 1,
    'amount': 1000,
    'currency': 'INR',
    'donor_name': 'John Doe',
    'message': 'Great cause!'
}
response = requests.post('https://givegrip.onrender.com/api/donations/', json=donation_data)
```

## 🚀 Deployment

### Render.com Deployment

1. **Fork/Clone** this repository
2. **Connect** to Render.com
3. **Create** new Web Service
4. **Configure** environment variables
5. **Deploy** automatically

### Manual Deployment

1. **Build the application**
   ```bash
   python manage.py collectstatic --no-input
   python manage.py migrate
   ```

2. **Configure production settings**
   ```bash
   # Update settings.py for production
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com']
   ```

3. **Set up web server**
   ```bash
   gunicorn givegrip.wsgi:application
   ```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --no-input

EXPOSE 8000
CMD ["gunicorn", "givegrip.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 📁 Project Structure

```
GiveGrip/
├── accounts/                 # User authentication and profiles
├── donations/               # Campaign and donation management
├── payments/                # Payment gateway integrations
├── pages/                   # CMS and static pages
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── media/                   # User uploaded files
├── givegrip/               # Main Django project
├── requirements.txt         # Python dependencies
├── build.sh                # Deployment script
├── render.yaml             # Render.com configuration
└── README.md               # This file
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 Python style guide
- Write tests for new features
- Update documentation
- Ensure mobile responsiveness
- Test payment integrations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive CSS framework
- Payment gateway providers for their APIs
- All contributors and supporters

## 📞 Support

- **Website**: [https://givegrip.onrender.com](https://givegrip.onrender.com)
- **Email**: support@givegrip.com
- **Issues**: [GitHub Issues](https://github.com/Vijayapardhu/GiveGrip/issues)

## 🔄 Changelog

### Version 1.0.0 (Current)
- Initial release
- Complete donation platform
- Multiple payment gateway support
- CMS integration
- Responsive design
- Admin dashboard

---

**Made with ❤️ by the GiveGrip Team**

[![GitHub stars](https://img.shields.io/github/stars/Vijayapardhu/GiveGrip?style=social)](https://github.com/Vijayapardhu/GiveGrip/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Vijayapardhu/GiveGrip?style=social)](https://github.com/Vijayapardhu/GiveGrip/network)
[![GitHub issues](https://img.shields.io/github/issues/Vijayapardhu/GiveGrip)](https://github.com/Vijayapardhu/GiveGrip/issues)
