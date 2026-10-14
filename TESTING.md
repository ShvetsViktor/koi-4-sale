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
