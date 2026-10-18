# Koi4Sale – Testing

## Overview

Koi4Sale was tested using Django's built-in test framework, Jest and manual checks. Automated tests verify application logic, while manual checks assess user-facing behaviour and administration. The results below distinguish completed checks from those still awaiting verification.

## Automated Testing

### Django

Run the complete Django test suite:

```bash
python3 manage.py test
```

Latest result:

```text
Found 70 test(s).
System check identified no issues (0 silenced).
Ran 70 tests in 28.658s
OK
```

Django tests cover areas including product search, reservation form validation, reservation workflows, access permissions and page rendering.

### JavaScript

Install dependencies and run Jest:

```bash
npm install
npm test
```

Latest result:

```text
PASS tests/cart-ui.test.js
PASS tests/cart-page.test.js
PASS tests/cart.test.js

Test Suites: 3 passed, 3 total
Tests:       19 passed, 19 total
Snapshots:   0 total
```

### Results

| Test suite | Passed | Failed | Result |
| --- | ---: | ---: | --- |
| Django | 70 | 0 | PASS |
| Jest | 19 | 0 | PASS |
| **Total** | **89** | **0** | **PASS** |

## User Story Testing

The table summarises verification of the 14 implemented user stories. Automated results are supported by the passing test suites above. `PENDING` identifies manual checks not yet recorded as completed. Screenshots of implemented features are provided in the main README's Features section.

| User Story | Verification | Result |
| --- | --- | --- |
| Browse Available Koi | Check catalogue displays available products and excludes reserved products. | PENDING manual check |
| View Koi Details | Check product information, images and add-to-cart action. | PENDING manual check |
| Filter Koi by Category | Check category filtering and matching results. | PENDING manual check |
| Search Koi | Django search tests passed; manually check name, variety, case-insensitive and no-result searches. | Automated PASS; manual PENDING |
| Responsive Catalogue | Check product grid and images on mobile, tablet and desktop. | PENDING |
| Manage Shopping Cart | Jest cart tests passed; check add, remove, totals and persistence in a browser. | Automated PASS; manual PENDING |
| Shopping Cart Indicator | Check count updates and desktop/mobile visibility. | Automated PASS; manual PENDING |
| Submit a Reservation Request | Django validation/workflow tests passed; valid submission and correction of an invalid email were checked manually. | Automated PASS; partial manual PASS |
| Prevent Duplicate Reservations | Verify unavailable koi cannot be reserved again. | Automated PASS; manual PENDING |
| Manage Products | Create, view, update and delete products in Django Admin; check availability changes in catalogue. | Manual PASS |
| Manage Orders | Check order status updates and product availability after cancellation. | PENDING manual check |
| Responsive Navigation | Check menu, links and cart access across screen sizes. | PENDING |
| Delivery Information | Check page content, four delivery steps and catalogue link. | PENDING final check |
| Contact Information | Check page, email links, active navigation and keyboard access. | Manual PASS (previously recorded) |

The FAQ page, featured koi carousel and reservation confirmation email are deferred *Could Have* features and are excluded from current-release testing.

### Recorded Manual Checks

The following checks were already completed during development:

| Area | Check | Recorded result |
| --- | --- | --- |
| Django Admin | View, create, update and delete a product. | PASS |
| Django Admin | Mark a product reserved and confirm it disappears from the catalogue. | PASS |
| Django Admin | Restore product availability and confirm it reappears. | PASS |
| Reservation form | Invalid email displays an error. | PASS |
| Reservation form | Form values and cart contents remain after validation fails. | PASS |
| Reservation form | Corrected email allows a successful reservation. | PASS |
| Contact | Page loads, links open email application, navigation and keyboard access work. | PASS |

The following reservation form checks have **not** yet been recorded manually: empty required fields; letters in phone number; valid UK and international phone numbers; phone numbers shorter than 7 or longer than 15 digits; unsupported phone characters. Automated form-validation tests passed.

## Responsive Testing

Check the homepage, catalogue, product details, cart, reservation form, Delivery and Contact pages at mobile, tablet and desktop widths. Verify readable text, correctly sized images, usable navigation, accessible cart controls and no unintended horizontal scrolling.

| Device / viewport | Result |
| --- | --- |
| Mobile | PENDING |
| Tablet | PENDING |
| Desktop | PENDING |

## Browser Compatibility

| Browser | Result |
| --- | --- |
| Chrome | PENDING |
| Safari | PENDING |
| Firefox | PENDING |
| Edge | PENDING |

Record the browser version and device used when these checks are completed.

## Accessibility Testing

| Check | Result |
| --- | --- |
| Keyboard navigation and visible focus across all pages | PENDING final review |
| Form labels and validation messages | PENDING final review |
| Image alternative text | PENDING final review |
| Heading hierarchy and semantic HTML | PENDING final review |
| Colour contrast | PENDING final review |

## Code Validation

| Tool / check | Result | Evidence |
| --- | --- | --- |
| HTML validation | PENDING | Add result or screenshot |
| CSS validation | PENDING | Add result or screenshot |
| Python linting / style checks | PENDING | Add command and result |
| JavaScript linting / style checks | PENDING | Add command and result |
| Django deployment checks (`python3 manage.py check --deploy`) | PENDING | Add result and explain any environment-specific warnings |

## Lighthouse Testing

Record results from Chrome DevTools Lighthouse for representative pages after testing the deployed site.

| Page | Performance | Accessibility | Best Practices | SEO |
| --- | --- | --- | --- | --- |
| Home | PENDING | PENDING | PENDING | PENDING |
| Catalogue | PENDING | PENDING | PENDING | PENDING |
| Product Details | PENDING | PENDING | PENDING | PENDING |

## Bugs and Fixes

### Outdated Homepage Hero Test Assertion — Resolved

**Issue:** After the homepage hero heading was updated, `test_homepage_displays_hero_section` still expected the previous heading, causing one of the 70 Django tests to fail.

**Fix:** Updated the test assertion to match the current heading, `Beautiful Koi, Raised with Care`.

**Retest:** All 70 Django tests passed. All 19 Jest tests also passed.

### Other Bugs

Add further confirmed bugs and fixes here if identified during final manual testing or validation. Do not record unverified issues as resolved.

## Final Testing Summary

**Automated tests:** 89 passed, 0 failed.

**Manual testing:** Product CRUD, selected reservation-form behaviours and Contact page checks have recorded PASS results. Other user journeys, responsive layouts, browser compatibility, accessibility and validator results still require final verification.

The testing documentation will be updated with actual results and evidence before final submission.
