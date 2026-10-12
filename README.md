# Koi4Sale – Django Koi Reservation Website

<!-- Add responsive mockup after the main interface is completed -->

**Live Website:** To be added after deployment.

## Overview

Koi4Sale is a full-stack web application for browsing and reserving individual Japanese koi.
The project is being developed for the Code Institute Unit 3 Back End Development assessment. It uses Django and a relational database to provide persistent data storage, server-side business logic, CRUD functionality, form processing, and administrative management.
Each koi is represented as an individual product rather than a product variation. Visitors can browse currently available koi, view detailed information and images, search or filter the catalogue, add koi to a client-side shopping cart, and submit a reservation request without creating an account.
When a reservation request is successfully submitted, the application creates the required customer and order records in the database and changes the selected koi from available to reserved. This prevents reserved koi from continuing to appear as available for reservation.
Customer registration and authentication are intentionally outside the scope of the initial project. Django's authentication system is used for administrative access, allowing authorised staff to manage products, images, product information, customers and orders through the Django Admin interface.
The application is being developed incrementally using Test-Driven Development (TDD) where appropriate. Important business behaviours are first described through automated tests, followed by the minimum implementation required to make the test pass and subsequent refactoring.
The existing Koi4Sale website previously developed using Next.js is used only as a visual and UX reference. This project is a new implementation built with Django Templates, HTML, CSS, Bootstrap and vanilla JavaScript.

---

## Table of Contents

1. [Project Goals](#project-goals)
2. [Target Audience](#target-audience)
3. [User Stories](#user-stories)
4. [Five Planes of UX](#five-planes-of-ux)
5. [Database Design](#database-design)
6. [Development Process](#development-process)
7. [Features](#features)
8. [Testing](#testing)
9. [Bugs](#bugs)
10. [Technologies Used](#technologies-used)
11. [Deployment](#deployment)
12. [Attribution, Credits and Acknowledgements](#attribution-credits-and-acknowledgements)
13. [Repo Structure](#repo-structure)
14. [Future Improvements](#future-improvements)

---

## Project Goals

### User Goals

- Browse koi currently available for reservation.
- View detailed information and images for an individual koi.
- Search and filter available koi.
- Add selected koi to a shopping cart.
- Review and modify the cart before checkout.
- Submit a reservation request without creating an account.
- Receive clear feedback when a reservation request is successfully submitted.
- Use the website comfortably on mobile, tablet and desktop devices.

### Site Owner Goals

- Present available koi professionally.
- Store product, customer and order information in a relational database.
- Manage individual koi and their availability.
- Add and manage multiple images for individual koi.
- Manage reservation requests.
- Prevent the same koi from being reserved by multiple customers.
- Maintain historical order information.
- Manage application data securely through authenticated administrative access.
- Keep the application maintainable and suitable for future development.

### Assessment Goals

- Build a full-stack web application using Python and Django.
- Design and implement a relational database appropriate to the project domain.
- Use Django ORM to create and manipulate persistent application data.
- Implement meaningful relationships between database entities.
- Provide Create, Read, Update and Delete functionality.
- Implement server-side form handling and validation.
- Use Django authentication and authorisation where appropriate.
- Build the front end using HTML, custom CSS, Bootstrap and vanilla JavaScript.
- Use automated testing to verify important application behaviour.
- Use Git and GitHub throughout development.
- Document UX decisions, database design, development, testing and deployment.
- Deploy the completed application with a production relational database.

### Why this project suits the brief

Koi4Sale is suited to the Unit 3 Back End Development brief because its core functionality depends on persistent relational data and server-side business logic.
Products, product images, product highlights, customers, orders and order items have defined relationships. Users interact with this data through the catalogue and reservation process, while authorised administrators can manage application records through authenticated administrative functionality.
The reservation workflow also provides a meaningful business rule: when an available koi is included in a successfully submitted order, its availability status must change so that it cannot be reserved again.

---

## Target Audience

The target audience includes:

- Koi enthusiasts looking for individual fish to purchase.
- Existing koi keepers looking for specific varieties, sizes or price ranges.
- New koi keepers comparing available fish before making an enquiry.
- Customers who prefer to reserve a fish before completing the final purchase directly with the seller.

---

## User Stories

### US1 — Browse Available Koi

As a visitor, I want to browse koi that are currently available so that I can see which fish I can reserve.
**Acceptance Criteria:**

- The catalogue displays products with an `available` status.
- Reserved koi are not displayed as available for reservation.
- Sold koi are not displayed as available for reservation.
- Unavailable koi are not displayed as available for reservation.
- Each catalogue item provides a clear route to its product detail page.
- A clear message is displayed if no available koi are found.

---

### US2 — View Koi Details

As a visitor, I want to view detailed information about an individual koi so that I can decide whether it is suitable for me.
**Acceptance Criteria:**

- The product detail page displays the koi's main information.
- The product price is clearly displayed.
- Product images are displayed where available.
- Product highlights or important characteristics are displayed where available.
- A visitor can add an available koi to the cart.
- A non-existent product URL returns an appropriate 404 response.

---

### US3 — Search and Filter Koi

As a visitor, I want to search or filter available koi so that I can find suitable fish more quickly.
**Acceptance Criteria:**

- Visitors can search the catalogue using relevant product information.
- Search results contain only matching products.
- Products that are not available are not returned as purchasable catalogue results.
- A clear message is displayed when no products match the search or filter.

---

### US4 — Manage Shopping Cart

As a visitor, I want to add and remove koi from my shopping cart so that I can prepare my reservation request before checkout.
**Acceptance Criteria:**

- An available koi can be added to the cart.
- The same koi cannot be added to the cart more than once.
- Items can be removed from the cart.
- The cart displays the selected koi.
- The cart displays the current total price.
- Cart contents remain available while the visitor continues browsing the website.

---

### US5 — Submit a Reservation Request

As a customer, I want to submit my contact details and selected koi so that I can request a reservation without creating an account.
**Acceptance Criteria:**

- Checkout displays the selected koi.
- Required customer information is collected through a form.
- Invalid or incomplete form data is rejected.
- Product availability is checked by the server before the reservation is created.
- A successful submission creates the required customer and order records.
- Each selected koi is associated with the created order.
- A successful reservation changes the selected koi from `available` to `reserved`.
- The customer receives clear confirmation that the request was submitted.

---

### US6 — Prevent Duplicate Reservations

As a customer, I want unavailable koi to be rejected during checkout so that I cannot submit a reservation for a fish that has already been reserved.
**Acceptance Criteria:**

- Product availability is checked on the server during checkout.
- A koi that is no longer available cannot be successfully reserved.
- An unsuccessful reservation does not leave a partially created order.
- The customer receives a clear message explaining that one or more selected koi are no longer available.

---

### US7 — Manage Products

As an authorised administrator, I want to manage koi records so that the catalogue contains accurate and current information.
**Acceptance Criteria:**

- Administrative functionality requires authentication.
- An authorised administrator can create product records.
- Existing product records can be viewed.
- Existing product records can be edited.
- Product records can be deleted where appropriate.
- Product availability status can be changed.
- Related product information can be managed.

---

### US8 — Manage Orders

As an authorised administrator, I want to view and manage reservation requests so that customer orders can be processed.
**Acceptance Criteria:**

- Administrative functionality requires authentication.
- Orders can be located and viewed.
- Customer information associated with an order can be viewed.
- Products associated with an order can be viewed.
- Order status can be updated.
- Reservation status and product availability remain consistent with the application's business rules.

---

### US9 — Use the Website on Different Devices

As a visitor, I want to use the website comfortably on different screen sizes so that I can browse and reserve koi using my preferred device.
**Acceptance Criteria:**

- Navigation remains usable on mobile, tablet and desktop.
- Product cards adapt to available screen width.
- Product detail content remains readable on smaller screens.
- Cart and checkout remain usable on mobile devices.
- Forms remain readable and easy to complete.
- The website does not introduce unnecessary horizontal scrolling.

---

## Five Planes of UX

The Five Planes of UX are being used to organise design decisions from the overall purpose of the application through to its final interface.

### Strategy

The strategy of Koi4Sale is to make browsing and reserving individual koi simple while giving the site owner reliable control over product availability and reservation requests.
The project is based on three priorities:

- **Clarity:** visitors should quickly understand which koi are currently available.
- **Confidence:** visitors should have enough information and imagery to make an informed reservation decision.
- **Reliability:** reservation requests must be processed consistently and unavailable koi must not be presented as available for reservation.

### Scope

The planned project scope includes:

- Available koi catalogue.
- Individual koi detail pages.
- Product images.
- Product highlights.
- Search and filtering.
- Client-side shopping cart.
- Checkout without customer registration.
- Customer data collection.
- Reservation request creation.
- Automatic product reservation.
- Administrative product management.
- Administrative order management.
- Responsive interface.
- Form validation.
- Automated testing of important business logic.
- Custom error handling.

### Structure

The main customer journey is:

1. **Browse available koi**
2. **Search or filter catalogue**
3. **View individual koi**
4. **Add koi to cart**
5. **Review cart**
6. **Complete checkout**
7. **Submit reservation request**
8. **Receive confirmation**
   Administrative functionality provides a separate authenticated workflow for managing products and reservation requests.

### Skeleton / Wireframes

Wireframes will be added as the interface structure is finalised.

### Surface

The visual design will use the existing Koi4Sale website as a visual reference while being reimplemented specifically for the Django application.
The intended interface is:

- Clean.
- Product-focused.
- Image-led.
- Easy to navigate.
- Responsive.
- Accessible.
- Consistent across catalogue, product, cart and checkout pages.

---

## Database Design

The application uses a relational database designed around individual koi products and reservation requests.
The current Entity Relationship Diagram contains six main entities:

- `Product`
- `ProductImage`
- `ProductHighlight`
- `Customer`
- `Order`
- `OrderItem`
<!-- Add final ERD image here -->

### Database Relationships

To be documented after the Django models are finalised.

### Product Availability

Each koi is represented by one `Product` record.
The planned product states are:

- `available`
- `reserved`
- `sold`
- `unavailable`
  Product status is intended to act as the single source of truth for availability rather than maintaining a separate boolean availability field.
  The reservation workflow will change a successfully reserved product from:

```text
available → reserved
```

## Further status behaviour will be documented as the order workflow is implemented.

## Development Process

The application is being developed incrementally using small Test-Driven Development cycles where appropriate.
The basic development cycle is:

```text
RED → GREEN → REFACTOR
```

1. Define an expected behaviour.
2. Write an automated test for that behaviour.
3. Run the test and confirm that it fails for the expected reason.
4. Implement the minimum functionality required.
5. Run the test and confirm that it passes.
6. Refactor where appropriate while keeping the tests passing.
7. Commit the completed behaviour to version control.
   Development stages will be documented here as the application is implemented.

---

## Features

## Features will be documented as they are implemented and verified.

## Testing

Testing documentation will be expanded throughout development rather than added only after the application is complete.
Planned testing includes:

- Django model tests.
- Django view tests.
- Form validation tests.
- Business logic tests.
- Reservation workflow tests.
- Authentication and authorisation tests.
- Manual user-flow testing.
- Responsive testing.
- Accessibility testing.
- HTML validation.
- CSS validation.
- JavaScript linting.
- Python code quality checks.
- Lighthouse testing.

### Automated Testing

Automated test evidence and instructions will be added as tests are implemented.

### Manual Testing

## Manual testing results will be recorded as functionality is completed.

## Bugs

Bugs discovered during development will be documented here with their cause, fix and retest result.

### Known Bugs

## No known bugs are currently documented.

## Technologies Used

### Main Technologies

- Python
- Django
- PostgreSQL
- HTML5
- CSS3
- JavaScript

### Libraries

- Bootstrap
  Additional libraries will be documented if they are introduced.

### Development Tools

- Visual Studio Code
- Git
- GitHub
- Chrome DevTools

---

## Deployment

Deployment instructions will be documented after the production environment has been configured.
The final application will use a deployed Django application connected to a relational production database.

### Local Development

## Local installation and development instructions will be added once the initial project configuration is complete.

## Attribution, Credits and Acknowledgements

### Existing Koi4Sale Project

The visual design and user experience of this Django project are based partly on the author's existing Koi4Sale website.
The Django version is a new implementation and does not use the existing Next.js, React or TypeScript application as its application architecture.

### Libraries and Tools

Libraries and external tools will be documented here as they are introduced.

### Code Attribution

Custom application code is written and adapted for this project.
External code, tutorials, libraries and other sources will be attributed where applicable.

### Support and Learning Resources

## Resources used during development will be documented here.

## Repo Structure

## The final repository structure will be documented after the initial Django project and applications have been created.

## Future Improvements

Features intentionally excluded from the initial project scope may be documented here after the MVP has been completed.
