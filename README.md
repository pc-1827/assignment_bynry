# Gas Utility Customer Service Application

A Django application that allows customers to submit and track service requests for a gas utility company, and provides customer service representatives (CSRs) with tools to manage and respond to these requests.

## Features

- **Customer Portal**
  - Submit service requests with file attachments
  - Track request status
  - View account information
  - Communicate with CSRs

- **CSR Dashboard**
  - Manage service requests
  - Update request status and priority
  - Assign requests to specific CSRs
  - Communicate with customers

- **Notifications System**
  - In-app notifications for status updates and comments
  - Email notifications

## Project Structure

```
assignment_bynry/
│
├── accounts/              # User authentication and profiles
├── service_requests/      # Core service request functionality
├── customer_portal/       # Customer-facing views and templates
├── csr_dashboard/         # Staff-facing views and templates
├── notifications/         # Email/SMS notification system
├── core/                  # Shared utilities and base templates
├── gas_utility_service/   # Project settings and configuration
├── templates/             # Templates for application
├── manage.py              # Django management script
├── docker-compose.yaml    # Docker Compose file
└── requirements.txt       # Project dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (for PostgreSQL)
- Git

---

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd assignment_bynry
```

### Step 2: Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\\Scripts\\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start PostgreSQL Container

```bash
docker-compose up -d db
```

### Step 5: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Load Initial Data

```bash
python manage.py loaddata service_requests/fixtures/initial_data.json
```

### Step 7: Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

### Step 8: Create a Staff User (CSR)

```bash
python manage.py create_staff_user staffuser password123 EMP-001 --email=staff@example.com --first_name=Staff --last_name=User
```

The command format is:

```bash
python manage.py create_staff_user <username> <password> <employee_id> [options]

Options:
  --department TEXT    CSR department (default: Customer Support)
  --email TEXT         Email address
  --first_name TEXT    First name
  --last_name TEXT     Last name
```

### Step 9: Run the Development Server
The application will be available at http://localhost:8000/

```bash
python manage.py runserver
```

## User Roles

### Customer
- Can register directly through the website
- Can submit and track service requests
- Can communicate with CSRs through chat

### CSR (Staff Member)
- Created through the admin interface or using the `create_staff_user` command
- Can view and manage all service requests
- Can update request status, priority, and assignment
- Can communicate with customers through chat

### Admin
- Created using the `createsuperuser` command
- Has access to the Django admin interface at [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Can manage all aspects of the system


