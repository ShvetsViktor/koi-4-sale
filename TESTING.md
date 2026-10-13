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
