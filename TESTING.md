# Testing

## Django Admin CRUD Testing

| Test                 | Expected Result                                       | Actual Result                       | Status |
| -------------------- | ----------------------------------------------------- | ----------------------------------- | ------ |
| View product         | Existing product details are displayed                | Product details displayed correctly | PASS   |
| Create product       | New product is saved to the database                  | Product created successfully        | PASS   |
| Update product       | Updated information is saved                          | Changes persisted successfully      | PASS   |
| Reserve product      | Reserved product disappears from the public catalogue | Product no longer displayed         | PASS   |
| Restore availability | Product reappears in the public catalogue             | Product displayed again             | PASS   |
| Delete product       | Product is deleted after confirmation                 | Test product deleted successfully   | PASS   |

## Admin Access Control

Access to product management is restricted through Django Admin permissions.

Automated tests verify that:

- Anonymous visitors cannot access product administration.
- Authenticated users without staff permissions cannot access product administration.
- Administrators can access product management.

## US09 — Search Koi by Name or Variety

### Automated Testing

Search functionality is tested using Django's built-in TestCase framework.

The following automated tests were implemented:

| Test                                      | Description                                                        | Result |
| ----------------------------------------- | ------------------------------------------------------------------ | ------ |
| test_search_by_product_name               | Verifies that searching by product name returns matching koi       | PASS   |
| test_search_by_category_name              | Verifies that searching by variety returns matching koi            | PASS   |
| test_search_excludes_unavailable_products | Verifies that reserved koi are excluded from search results        | PASS   |
| test_search_no_results                    | Verifies that a message appears when no koi match the search query | PASS   |

Run the search tests using:

    python3 manage.py test products.tests.ProductSearchTests

All four automated tests passed.

### Manual Testing

| Test                        | Expected Result                                         | Actual Result     | Status  |
| --------------------------- | ------------------------------------------------------- | ----------------- | ------- |
| Search by name              | Matching koi are displayed                              | Pass verification | PENDING |
| Search by variety           | Koi matching the selected variety are displayed         | Pass verification | PENDING |
| Case-insensitive search     | Lowercase and uppercase queries return matching results | Pass verification | PENDING |
| Search unavailable koi      | Reserved koi are excluded from results                  | Pass verification | PENDING |
| Search with no matches      | An appropriate message is displayed                     | Pass verification | PENDING |
| Search with category filter | Results satisfy both search and category conditions     | Pass verification | PENDING |

## Reservation Form Validation

The reservation form uses HTML5 validation and Django's `ReservationForm` to validate customer contact details before creating an order.

Server-side validation ensures that invalid customer information cannot be saved to the database.

### Automated Testing

Reservation form validation is tested using Django's built-in TestCase framework.

| Test                          | Expected Result                                          | Status |
| ----------------------------- | -------------------------------------------------------- | ------ |
| Required fields               | Empty required fields are rejected                       | PASS   |
| Invalid email                 | Invalid email addresses are rejected                     | PASS   |
| Phone containing letters      | Phone numbers containing letters are rejected            | PASS   |
| Valid UK phone number         | Valid UK phone number is accepted                        | PASS   |
| International phone number    | Number with spaces and leading + is accepted             | PASS   |
| Short phone number            | Numbers containing fewer than 7 digits are rejected      | PASS   |
| Long phone number             | Numbers containing more than 15 digits are rejected      | PASS   |
| Phone with special characters | Numbers containing unsupported characters are rejected   | PASS   |
| Invalid reservation           | No order is created when validation fails                | PASS   |
| Corrected email               | Reservation succeeds after correcting an invalid email   | PASS   |
| Preserve form values          | Previously entered values remain after validation errors | PASS   |

Phone number validation is implemented using `ReservationForm.clean_phone()`.

The validation allows:

- Digits (`0–9`).
- Spaces.
- An optional leading `+`.

Phone numbers must contain between 7 and 15 digits.

The following examples demonstrate the validation rules:

| Phone Number       | Expected Result | Status |
| ------------------ | --------------- | ------ |
| `07123456789`      | Accepted        | PASS   |
| `+44 7123 456789`  | Accepted        | PASS   |
| `abc123456`        | Rejected        | PASS   |
| `123456`           | Rejected        | PASS   |
| `1234567890123456` | Rejected        | PASS   |
| `07123-456789`     | Rejected        | PASS   |

### Contact Page

The Contact page provides customers with a way to contact Koi4Sale
regarding product availability, reservations, and delivery.

| Test                    | Expected Result                                  | Result |
| ----------------------- | ------------------------------------------------ | ------ |
| Open Contact page       | Page loads successfully                          | PASS   |
| Contact navigation link | Opens the Contact page                           | PASS   |
| Active navigation state | Contact link is highlighted                      | PASS   |
| Email address link      | Opens the default email application              | PASS   |
| Send an Email button    | Opens the default email application              | PASS   |
| Responsive layout       | Content displays correctly on mobile and desktop | PASS   |
| Keyboard navigation     | Interactive elements are keyboard accessible     | PASS   |

**Automated testing:**

- Contact page returns HTTP 200.
- Correct Django template is rendered.
- Contact page heading is displayed.
- Contact information and email link are present.

**Test command:**

`python3 manage.py test tests.django.test_contact`

### Manual Testing

| Test                       | Expected Result                                | Actual Result                    | Status  |
| -------------------------- | ---------------------------------------------- | -------------------------------- | ------- |
| Submit empty fields        | Browser prevents submission                    | Not yet recorded                 | PENDING |
| Submit invalid email       | Validation error appears below the email field | Error displayed correctly        | PASS    |
| Preserve entered details   | Form values remain after validation failure    | Values preserved                 | PASS    |
| Preserve cart contents     | Selected koi remain in the cart                | Cart contents preserved          | PASS    |
| Correct invalid email      | Reservation succeeds after correction          | Reservation created successfully | PASS    |
| Enter letters in phone     | Phone validation error is displayed            | Not yet verified manually        | PENDING |
| Enter valid UK number      | Phone number is accepted                       | Not yet verified                 | PENDING |
| Enter international number | Number beginning with `+` is accepted          | Not yet verified                 | PENDING |
| Enter fewer than 7 digits  | Phone number is rejected                       | Not yet verified                 | PENDING |
| Enter more than 15 digits  | Phone number is rejected                       | Not yet verified                 | PENDING |
| Enter special characters   | Phone number is rejected                       | Not yet verified                 | PENDING |

### Validation Error Handling

When server-side validation fails:

- The reservation is not created.
- The form is displayed again with validation errors.
- Previously entered customer details are preserved.
- Selected koi remain in the shopping cart.
- Customers can correct their details and resubmit the reservation.

Validation errors are displayed beneath the corresponding form fields.

The reservation form also displays a general error message informing customers that their submitted information requires correction.

### Testing Commands

Run the reservation form tests:

    python3 manage.py test orders.tests.ReservationFormTests

Run the reservation workflow tests:

    python3 manage.py test orders.tests.ReservationViewTests

Run all Django tests:

    python3 manage.py test

Run JavaScript tests:

    npm test

All automated Django and JavaScript tests passed following the implementation of phone number validation.
