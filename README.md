
# RestaurantFlow

RestaurantFlow is a web application for managing restaurant tables, reservations, menus, and orders. I developed it as an individual project for the SoftUni Django Basics Regular Exam in October 2026.

The idea behind the project is simple: customers can reserve a table in advance or order food directly from a table when they visit the restaurant. These two features work independently, so making a reservation is not required to place an order.

The application also provides basic management functionality for restaurant tables, dishes, reservations, and orders.

## Technologies

- Python 3.14
- Django 6.1.2
- SQLite
- Django ORM
- Django Templates
- HTML5, CSS3, JavaScript
- Bootstrap 5

## Features

### Tables

Restaurant tables can be created, viewed, edited, and deleted.

Each table has a unique number, a seating capacity, a location (Indoor, Terrace, or Garden), and a field indicating whether it is in service.

Tables with existing orders or active/upcoming confirmed reservations cannot be deleted.

### Reservations

Customers can make reservations by choosing a date, time, number of guests, and one or more tables.

Reservations use a two-hour time interval. For confirmed reservations, the form checks that:

- The reservation is not in the past.
- The selected tables are in service.
- The combined table capacity is sufficient for the guests.
- The selected tables do not have overlapping confirmed reservations.

Customer names and phone numbers are also validated.

Reservations can be viewed, edited, and deleted through the website.

### Menu

The menu contains dishes organized into four categories: Starters, Main Dishes, Desserts, and Drinks.

Each dish has a name, category, price, optional description, and availability status.

Dishes can be created, viewed, edited, and deleted. Dishes associated with existing orders are protected from deletion. The menu also supports filtering by category.

A custom validator checks dish names, while Django's minimum-value validation ensures that prices meet the required minimum.

### Orders

Customers can select a table and choose dishes from the menu without making a reservation.

When creating an order, only tables in service and available dishes are displayed.

New orders start with the status **Pending**. When editing an order, the status can be changed to Preparing, Ready, or Served.

The table assigned to an existing order is displayed as a disabled field to prevent accidental changes.

Each available dish is displayed with its price, and the order form calculates the total as dishes are selected or removed.

The total is also displayed on the order list and detail pages.

## Project Structure

The project contains three Django applications and four database models.

```text
RestaurantFlow/
│
├── project_apps/
│   ├── reservations/
│   │   ├── models.py
│   │   ├── forms.py
│   │   ├── validators.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   ├── menu/
│   │   ├── models.py
│   │   ├── forms.py
│   │   ├── validators.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   └── orders/
│       ├── models.py
│       ├── forms.py
│       ├── views.py
│       ├── urls.py
│       ├── migrations/
│       └── templatetags/
│           └── order_extras.py
│
├── restaurant_op_system/
│   ├── settings.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── 404.html
│   ├── reservations/
│   ├── menu/
│   └── orders/
│
├── static/
│   └── css/
│       └── style.css
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Models and Relationships

| Model | Relationships |
|---|---|
| Table | Referenced by reservations and orders |
| Reservation | Many-to-Many with Table |
| Dish | Many-to-Many with Order |
| Order | ForeignKey to Table and Many-to-Many with Dish |

The Many-to-Many relationship between reservations and tables allows a reservation to include more than one table.

Each order belongs to one table but can contain multiple different dishes.

## Django Functionality

The project uses Django Class-Based Views for CRUD operations.

All four models have List, Detail, Create, Update, and Delete views. Deleting an object requires confirmation.

Other Django features used in the project include:

- ModelForms and custom form validation
- Custom validators
- Django ORM queries and relationships
- Pagination
- Filtering and ordering
- Template inheritance
- Built-in template tags and filters
- A custom template filter
- A custom 404 page

### Custom Template Filter

The `order_total` filter is defined in:

`project_apps/orders/templatetags/order_extras.py`

It calculates the sum of the current prices of the dishes included in an order.

The filter is used in the order list template. The order detail page receives a separately calculated `total_price` from `OrderDetailView`.

## Installation

The project was developed using Python 3.14 and Django 6.1.2.

### 1. Clone the repository

```bash
git clone https://github.com/chepmr/RestaurantFlow.git
cd RestaurantFlow
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

This creates the SQLite database and the required tables.

### 5. Run the server

```bash
python manage.py runserver
```

Open the application at:

http://127.0.0.1:8000/

## Using the Application

The project does not require predefined data or manual database setup.

After starting the server, you can create everything through the website.

A simple way to get started is:

1. Open **Tables** and create a restaurant table.
2. Open **Menu** and add a few dishes.
3. Create a reservation by selecting one or more tables.
4. Open **Orders**, select a table and choose dishes.
5. View the order details to see the selected dishes and total price.

All main sections are accessible from the navigation bar.

Django Admin is not required to use the application.

## Main URLs

| Page | URL |
|---|---|
| Home | `/` |
| Tables | `/reservations/tables/` |
| Reservations | `/reservations/list/` |
| Menu | `/menu/dishes/` |
| Orders | `/orders/` |

## Configuration

The project uses SQLite and is configured for local development.

No external database server is needed.

The Django secret key can be provided through the `DJANGO_SECRET_KEY` environment variable. If it is not set, Django generates a new key when the application starts. The generated key is not preserved between restarts.

The current settings use `DEBUG = True` and allow access through `localhost` and `127.0.0.1`.

For production use, these settings would need to be adjusted, including a persistent secret key, allowed hosts, and static file configuration.

## Testing

The application has been manually tested through the browser, including starting it with a new, empty SQLite database.

The checks included:

- Creating all four models through the interface
- Viewing, editing, and deleting records
- Form validation and error messages
- Reservation capacity and overlapping time checks
- Model relationships
- Order creation and status updates
- Total price calculations
- Delete confirmation and table deletion restrictions
- Navigation and the custom 404 page

The application was tested without using Django Admin or manually inserting database records.

Automated test coverage is not included in the current version.

## Current Limitations

RestaurantFlow is an educational project rather than a production-ready restaurant system.

At the moment, orders do not support separate quantities for the same dish. Order totals are calculated using the current menu prices, and historical prices are not stored separately.

The application also does not include online payments, customer authentication, or verification that a customer is physically present at a table.

These features are outside the scope of the current version.


## Final Testing and Verification

RestaurantFlow has been manually tested to verify its core functionality and compliance with the Django Basics exam requirements.

### Functional Testing

- Creating, viewing, updating, and deleting tables, reservations, dishes, and orders.
- Confirming deletions before removing records.
- Validating form inputs and displaying meaningful error messages.
- Checking table capacity and overlapping reservations.
- Verifying relationships between tables, reservations, orders, and dishes.
- Testing navigation between pages and the custom 404 error page.
- Confirming that orders can be created independently of reservations.

### Database and Setup

The application uses SQLite and does not require prepopulated data, fixtures, or Django Admin to create records.

Database migrations can be applied using:

```bash
python manage.py migrate
```

The development server can be started using:

```bash
python manage.py runserver
```

All main records can be created and managed directly through the application's web interface.

[GitHub Repository](https://github.com/chepmr/RestaurantFlow


## Author

**Atanas Naydenov**

SoftUni Django Basics Regular Exam — October 2026