# E-Bazaar

E-Bazaar is a production-minded Django marketplace for customers, sellers, and wholesalers. It began as a coursework prototype and has been rebuilt around a transactional commerce model: public catalog discovery, inventory-safe checkout, immutable order records, account self-service, seller inventory management, automated tests, and container deployment.

## What works

### Customer storefront

- Responsive home page, featured products, collections, and category navigation
- Product catalog with full-text-style search, category/price/stock filters, sorting, and pagination
- Product pages with live availability, variants, sale pricing, related products, and ratings
- Authenticated cart with one line per product, quantity limits, and server-side price calculation
- Wishlist, profile editing, and multiple saved delivery addresses
- Checkout using saved or new addresses, coupon validation, cash on delivery, or bank transfer
- Order history, private order details, status/payment visibility, and cancellation while eligible
- Verified-purchase reviews after delivery

### Commerce and inventory rules

- `DecimalField` is used for all money; totals are never accepted from the browser
- Checkout runs in a database transaction and locks the cart, coupon, and products
- Stock is revalidated and decremented only when an order is created
- A failed checkout leaves inventory, coupons, cart contents, and orders unchanged
- Order lines snapshot name, SKU, seller, unit price, and line total
- Delivery details are copied to the order so later address edits cannot rewrite history
- Eligible cancellation restores inventory exactly once
- Coupons support percentage/fixed discounts, minimum order amounts, schedules, and usage limits
- Free shipping applies at $100 after discounts; standard delivery is $10

### Seller and operations tooling

- Seller/wholesaler registration without unsafe automatic Django-admin access
- Seller dashboard with product, low-stock, unit-sales, and gross-sales summaries
- Seller-scoped product creation, editing, image upload, stock changes, and deactivation
- Seller view of orders containing their own product lines
- Customized Django admin for users, categories, collections, products, carts, orders, coupons, and reviews
- Health endpoint at `/health/`

### Engineering baseline

- Environment-based secrets and database configuration
- SQLite for zero-configuration local development; PostgreSQL through `DATABASE_URL`
- WhiteNoise static assets, Gunicorn, Docker, and Docker Compose
- GitHub Actions checks for configuration, migrations, and the test suite
- Idempotent demo-data command

## Local setup

Python 3.12 is recommended.

```bash
git clone https://github.com/AbdurRazzaqSiddiqui/E-Bazaar_WebApp_using_Django_Framework.git
cd E-Bazaar_WebApp_using_Django_Framework
python -m venv .venv
```

Activate the environment:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install, migrate, and seed:

```bash
pip install -r requirements-dev.txt
cp .env.example .env  # optional; export variables manually on Windows
cd ECommerce
python manage.py migrate
python manage.py seed_store
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

The development seed is idempotent and prints its credentials. Defaults:

| Purpose | Username | Password |
|---|---|---|
| Browse and checkout | `demo_customer` | `DemoStore123!` |
| Manage products | `demo_seller` | `DemoStore123!` |

Coupon `WELCOME10` gives 10% off an order of at least $50. Override the demo password with:

```bash
python manage.py seed_store --password "Your-Local-Demo-Password"
```

Create a real administrator separately:

```bash
python manage.py createsuperuser
```

## Docker setup

Docker Compose starts Django and PostgreSQL:

```bash
docker compose up --build
docker compose exec web python manage.py seed_store
```

The Compose credentials are development-only. Replace every secret before any shared or internet-facing deployment.

## Tests

From the repository root:

```bash
pip install -r requirements-dev.txt
cd ECommerce
python manage.py check
python manage.py makemigrations --check --dry-run
coverage run manage.py test
coverage report
```

The suite covers public catalog access, registration, cart ownership and quantity limits, transactional checkout, coupons, insufficient stock, cancellation/restocking, private orders, wishlists, verified reviews, and seller authorization.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DEBUG` | `True` | Enables Django development behavior |
| `SECRET_KEY` | Development-only fallback | Required when `DEBUG=False` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated Django hosts |
| `CSRF_TRUSTED_ORIGINS` | Empty | Comma-separated HTTPS origins behind a proxy |
| `DATABASE_URL` | Project SQLite file | PostgreSQL example: `postgresql://user:pass@host:5432/db` |
| `TIME_ZONE` | `UTC` | Django application time zone |
| `SECURE_SSL_REDIRECT` | `True` in production | Set false only when TLS is intentionally absent |
| `SESSION_COOKIE_SECURE` | Follows production mode | Set false only for deliberate local HTTP setups |
| `CSRF_COOKIE_SECURE` | Follows production mode | Set false only for deliberate local HTTP setups |
| `SECURE_HSTS_SECONDS` | `31536000` in production | HSTS duration; the local Compose file uses `0` |
| `DEFAULT_FROM_EMAIL` | `store@example.com` | Outbound sender identity |
| `LOG_LEVEL` | `INFO` | Root application log level |

## Production checklist

1. Set a long random `SECRET_KEY`, `DEBUG=False`, final `ALLOWED_HOSTS`, and HTTPS origins.
2. Use managed PostgreSQL and durable object storage for uploaded media.
3. Run `python manage.py check --deploy`, migrations, and `collectstatic` during release.
4. Put the app behind TLS, preserve proxy headers correctly, and back up the database and media.
5. Configure transactional email and monitoring for `/health/`, application errors, database saturation, disk, and order failures.
6. Add a real payment provider before accepting cards. The included checkout intentionally supports only cash on delivery and manual bank transfer; it never stores card data.

## Schema upgrade note

Migration `0019_commerce_rebuild` preserves user accounts and maps the original `user1/user2/user3` roles, but intentionally replaces the prototype catalog/cart/order tables. The legacy schema had no safe order-line relationship or monetary representation, and the committed raw MySQL `.ibd` files do not provide a portable migration path. Back up any meaningful database and write a project-specific import before upgrading a populated legacy installation.

## Security notice for the original repository

The coursework version committed a Django secret and a MySQL root password. They have been removed from the current source, but Git history remains public. Treat both as compromised: rotate the database password anywhere it was reused and issue a new production Django secret. Removing a value in a later commit does not remove it from repository history.

## Project structure

```text
ECommerce/
├── ECommerce/                 # settings, ASGI/WSGI, root URLs
├── EBazaar/
│   ├── management/commands/   # repeatable demo catalog
│   ├── migrations/            # schema history and commerce rebuild
│   ├── static/EBazaar/        # storefront CSS, JS, and legacy image assets
│   ├── templates/EBazaar/     # storefront, account, order, and seller UI
│   ├── admin.py               # store operations admin
│   ├── forms.py               # validated customer and seller forms
│   ├── models.py              # catalog, cart, coupon, order, and review domain
│   ├── services.py            # atomic checkout and cancellation logic
│   ├── tests.py               # application test suite
│   └── views.py               # public, customer, and seller workflows
└── manage.py
```

## Deliberate scope

This version is a complete deployable MVP, not a claim that commerce software is ever “finished.” Taxes, carrier quotes, refunds, card processing, seller payouts, fraud controls, returns, notifications, and marketplace commission rules depend on the country and business model. The current boundaries are explicit so those integrations can be added without compromising order or inventory integrity.
