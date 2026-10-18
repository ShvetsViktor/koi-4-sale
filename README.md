# Koi4Sale – Django Koi Reservation Website

<!-- mockup goes here -->

**Live Website:** https://koi-for-sale-2e89f5c55c63.herokuapp.com/

## Overview

Koi4Sale is a full-stack web application for browsing individual Japanese koi and submitting reservation requests without creating a customer account or making an online payment.

The project is developed for the **Code Institute Level 5 Diploma in Web Application Development – Unit 3: Back End Development** assessment. It uses **Django**, a relational database, Django Templates, **Bootstrap 5.3**, custom CSS and vanilla JavaScript.

Each koi is represented as a unique product rather than a variation of a stock item. Visitors can browse available koi, view detailed product information and images, search and filter the catalogue, manage a client-side shopping cart and submit a reservation request.

The server validates product availability before creating customer and order records. When a reservation is successfully submitted, the selected koi are marked as reserved to prevent duplicate reservations.

Customer registration and authentication are intentionally excluded from the initial project scope. Authorised administrators manage products, images, customers and reservation requests through Django Admin.

The project is developed incrementally using GitHub Issues, milestones and automated testing. Testable functionality follows the **RED → GREEN → REFACTOR** development cycle where appropriate.

The previous Koi4Sale website, developed using Next.js, React and TypeScript, serves as a visual and UX reference. This project is a separate implementation using Django Templates, HTML, CSS, Bootstrap and vanilla JavaScript.

> **Project Status:** The backend and reservation functionality have been developed. The responsive frontend interface is currently being implemented and refined. Features are not considered complete until implemented and verified.

---

## Table of Contents

1. [Project Goals](#project-goals)
2. [Target Audience](#target-audience)
3. [User Stories and Prioritisation](#user-stories-and-prioritisation)
4. [Five Planes of UX](#five-planes-of-ux)
5. [Database Design](#database-design)
6. [Development Process](#development-process)
7. [Features](#features)
8. [Testing](#testing)
9. [Bugs](#bugs)
10. [Technologies Used](#technologies-used)
11. [Deployment](#deployment)
12. [Attribution, Credits and Acknowledgements](#attribution-credits-and-acknowledgements)
13. [Repository Structure](#repository-structure)
14. [Future Improvements](#future-improvements)

---

## Project Goals

### User Goals

- Understand what Koi4Sale offers and which fish are available.
- Browse individual koi and examine prices, characteristics and photographs.
- Search for koi using relevant product information.
- Filter koi by category.
- Add and remove koi from a shopping cart.
- Review selected products and the total price.
- Submit a reservation request without creating an account.
- Receive clear confirmation or validation feedback.
- Access delivery information and contact details.
- Use the website comfortably on mobile, tablet and desktop devices.

### Site Owner Goals

- Present available koi professionally and accurately.
- Maintain product details, photographs and availability.
- Store customer and reservation information in a relational database.
- Manage products and reservation requests through authenticated administration.
- Prevent duplicate reservations.
- Preserve historical order information.
- Keep the application secure, maintainable and suitable for future development.

### Assessment Goals

- Develop a full-stack web application using Python and Django.
- Design and implement a relational database.
- Use Django ORM and meaningful relationships between models.
- Implement Create, Read, Update and Delete functionality.
- Process forms and validate submitted information on the server.
- Apply authentication and authorisation where appropriate.
- Build a responsive frontend using HTML, custom CSS, Bootstrap and JavaScript.
- Implement automated testing for important application behaviour.
- Use Git and GitHub throughout development.
- Document UX decisions, database design, development and testing.
- Deploy the application with a production relational database.

### Why This Project Suits the Brief

Koi4Sale is suitable for the Unit 3 Back End Development assessment because its core functionality depends on persistent relational data and server-side business logic.

Products, product images, customers, orders and order items are connected through database relationships.

The reservation workflow demonstrates an important business rule: the server must verify product availability before accepting a reservation request.

When a reservation is successfully created, the selected koi must become unavailable for further reservation.

Django Admin provides authenticated administrative functionality for managing application records.

---

## Target Audience

The primary target audience consists of customers in the United Kingdom who are interested in purchasing individual Japanese koi.

### Experienced Koi Keepers

Customers who already maintain koi ponds and want to compare individual fish by size, variety, appearance and price.

### New Koi Keepers

Customers who need clear product descriptions, photographs and practical information before making a reservation.

### Customers Seeking Direct Contact

Customers who prefer to reserve a fish before arranging payment, collection or delivery directly with the seller.

### User Needs and Business Needs

Customers need:

- Accurate information about available koi.
- Clear photographs and product characteristics.
- Simple navigation.
- An understandable reservation process.
- Confidence that unavailable koi cannot be reserved.
- Clear delivery and contact information.

The site owner needs:

- Reliable product availability management.
- Persistent customer and reservation records.
- Straightforward product administration.
- Protection against duplicate reservations.
- A maintainable application.

These requirements inform the project's functionality and UX decisions.

---

## User Stories and Prioritisation

User stories describe the needs of visitors, customers and administrators.

They are organised by functionality rather than assigned additional story numbers.

GitHub Issues and milestones are used to track implementation tasks, acceptance criteria and development progress. Issue titles follow the same naming conventions as the user stories documented here.

The project uses **MoSCoW prioritisation** to distinguish essential functionality from optional enhancements.

### MoSCoW Prioritisation

| User Story                     | Priority    | Purpose                                                                                      |
| ------------------------------ | ----------- | -------------------------------------------------------------------------------------------- |
| Browse Available Koi           | Must Have   | Display koi available for reservation.                                                       |
| View Koi Details               | Must Have   | Provide detailed product information and photographs.                                        |
| Filter Koi by Category         | Must Have   | Allow visitors to browse koi by category.                                                    |
| Manage Shopping Cart           | Must Have   | Allow visitors to manage selected koi.                                                       |
| Shopping Cart Indicator        | Should Have | Display the number of selected products and provide quick access to the cart across devices. |
| Submit a Reservation Request   | Must Have   | Process customer reservation requests.                                                       |
| Prevent Duplicate Reservations | Must Have   | Prevent unavailable koi from being reserved again.                                           |
| Manage Products                | Must Have   | Provide authenticated product administration.                                                |
| Manage Orders                  | Must Have   | Provide authenticated reservation management.                                                |
| Responsive Navigation          | Must Have   | Provide accessible navigation across screen sizes.                                           |
| Responsive Catalogue           | Must Have   | Display product cards appropriately on different devices.                                    |
| Delivery Information           | Should Have | Explain delivery arrangements and conditions.                                                |
| Contact Information            | Should Have | Provide contact details and enquiry options.                                                 |
| Search Koi                     | Should Have | Help visitors find koi using search terms.                                                   |
| Frequently Asked Questions     | Could Have  | Answer common customer questions.                                                            |
| Reservation Confirmation Email | Could Have  | Send customers confirmation of their reservation request.                                    |
| Featured Koi Carousel          | Could Have  | Highlight selected products on the home page.                                                |

### Core User Stories

#### Browse Available Koi

As a **visitor**, I want to browse currently available koi so that I can see which fish I can reserve.

**Acceptance Criteria**

- Only available koi appear as reservable catalogue items.
- Reserved, sold and unavailable koi are excluded from the available catalogue.
- Each product provides a link to its detail page.
- An empty catalogue displays a useful message.

#### View Koi Details

As a **visitor**, I want to view photographs and detailed information about an individual koi so that I can decide whether to reserve it.

**Acceptance Criteria**

- The product detail page displays the koi's name, price and description.
- Available product photographs are displayed.
- Important characteristics are displayed where recorded.
- Available koi can be added to the cart.
- Invalid product URLs return an appropriate 404 response.

#### Filter Koi by Category

As a **visitor**, I want to filter koi by category so that I can browse fish belonging to a particular variety or group.

**Acceptance Criteria**

- Visitors can select a category to filter the catalogue.
- Only products belonging to the selected category are displayed.
- Unavailable products are excluded from reservable results.
- Visitors can return to the complete available catalogue.
- An appropriate message is displayed when a category contains no available products.

#### Manage Shopping Cart

As a **visitor**, I want to add and remove koi from my shopping cart so that I can prepare a reservation request.

**Acceptance Criteria**

- Available koi can be added to the cart.
- The same koi cannot be added more than once.
- Cart contents persist while the visitor continues browsing.
- The cart displays selected products, images and prices.
- The total price is calculated and displayed.
- Products can be removed without creating an account.

#### Submit a Reservation Request

As a **customer**, I want to submit my contact details and selected koi so that I can request a reservation without paying online.

**Acceptance Criteria**

- Required customer information is collected through a form.
- Submitted information is validated on the server.
- Product availability is checked before creating the reservation.
- Successful submission creates related customer and order records.
- Selected products are associated with the created order.
- Successfully reserved products change from `available` to `reserved`.
- Confirmation explains that a reservation request has been received.

#### Prevent Duplicate Reservations

As a **customer**, I want unavailable koi to be rejected during submission so that I do not receive a misleading reservation confirmation.

**Acceptance Criteria**

- Product availability is checked on the server.
- Unavailable koi cannot be successfully reserved again.
- Failed validation does not leave partially created reservation records.
- The customer receives a clear error message.

#### Manage Products

As an **authorised administrator**, I want to manage koi records so that the catalogue contains accurate product information.

**Acceptance Criteria**

- Administrative functionality requires authentication and appropriate permissions.
- Product records can be created and viewed.
- Existing products can be updated.
- Products can be deleted where appropriate.
- Product images and related information can be managed.
- Product availability can be changed.

#### Manage Orders

As an **authorised administrator**, I want to manage reservation requests so that customer orders can be processed.

**Acceptance Criteria**

- Administrative functionality requires authentication and appropriate permissions.
- Orders and associated customer information can be viewed.
- Products associated with an order can be identified.
- Order status can be updated.
- Product availability remains consistent with reservation rules.

#### Responsive Navigation

As a **visitor**, I want navigation that adapts to my device so that I can easily access important pages.

**Acceptance Criteria**

- Navigation is usable on mobile, tablet and desktop.
- Desktop navigation displays visible links to important pages.
- Mobile navigation provides an accessible collapsible menu.
- The logo links to the home page.
- The current page is visually identifiable.
- Navigation supports keyboard interaction.

#### Responsive Catalogue

As a **visitor**, I want the product catalogue to adapt to my screen size so that I can browse koi comfortably on any device.

**Acceptance Criteria**

- Product cards adapt to available screen width.
- Images maintain appropriate proportions.
- Product information remains readable.
- Important actions remain accessible.
- The catalogue does not introduce unnecessary horizontal scrolling.

#### Delivery Information

As a **visitor**, I want to understand the delivery arrangements so that I can decide whether purchasing a koi is practical for me.

**Acceptance Criteria**

- Delivery information is accessible through the website.
- Available delivery or collection arrangements are explained.
- Relevant limitations or conditions are clearly communicated.

#### Contact Information

As a **visitor**, I want to contact the seller so that I can ask questions before submitting a reservation.

**Acceptance Criteria**

- Contact information is easy to locate.
- Visitors have a clear method of contacting the seller.
- Any contact form includes appropriate validation and feedback.

### Additional User Stories

#### Shopping Cart Indicator

As a **visitor**, I want to see how many koi are in my shopping cart without opening it so that I can keep track of my selections while browsing.

**Acceptance Criteria**

- The header displays the number of products currently in the cart.
- The indicator updates immediately when products are added or removed.
- The indicator is hidden when the cart is empty.
- The cart icon remains visible on mobile devices when the navigation menu is collapsed.
- The cart icon provides direct access to the shopping cart.
- The indicator remains accurate after reloading the page.
- The cart indicator is accessible on mobile and desktop devices.

#### Search Koi

As a **visitor**, I want to search available koi using relevant information so that I can find suitable fish more quickly.

**Acceptance Criteria**

- Visitors can submit a search query.
- Search results contain products matching the query.
- Unavailable products are not presented as reservable results.
- An appropriate message is displayed when no products match.
- Visitors can return to the complete available catalogue.

#### Frequently Asked Questions

As a **visitor**, I want answers to common questions so that I can understand the reservation process and koi purchasing arrangements.

**Acceptance Criteria**

- Frequently asked questions are accessible from the website.
- Questions and answers are clearly organised.
- Information is relevant to the purchasing and reservation process.

#### Reservation Confirmation Email

As a **customer**, I want to receive an email confirming my reservation request so that I have a record of the products I requested.

**Acceptance Criteria**

- A confirmation email is sent after a successful reservation request.
- The email includes relevant reservation information.
- The email clearly identifies the reservation as a request rather than a completed purchase.
- No confirmation email is sent for an unsuccessful reservation.
- Email delivery failures are handled appropriately.

#### Featured Koi Carousel

As a **visitor**, I want to see highlighted koi on the home page so that I can discover interesting available fish.

**Acceptance Criteria**

- Featured products are displayed on the home page.
- Product images and information are presented clearly.
- Featured items link to their product detail pages.
- The component remains usable on different screen sizes.

---

## Five Planes of UX

The project follows Jesse James Garrett's **Five Planes of User Experience** framework.

The framework connects user and business needs to the final visual interface.

The five planes are:

1. **Strategy** — Why does the website exist?
2. **Scope** — What functionality and content are required?
3. **Structure** — How is information organised?
4. **Skeleton** — How are interface elements arranged?
5. **Surface** — What does the finished interface look like?

Each plane builds upon the decisions made at the previous level.

### 1. Strategy — Why Does the Website Exist?

The purpose of Koi4Sale is to make browsing and reserving individual koi straightforward while providing the site owner with reliable control over products and reservations.

#### Business Objectives

- Present individual koi professionally.
- Make currently available fish easy to discover.
- Receive reservation enquiries from interested customers.
- Maintain accurate product availability.
- Manage customer and reservation information efficiently.

#### User Objectives

- Discover available koi.
- Compare individual fish.
- Access reliable product information.
- Understand the reservation process.
- Submit a reservation request with confidence.

#### Design Principles

**Clarity**

Visitors should immediately understand what the website offers and which products are available.

**Confidence**

Product photographs, descriptions, prices and practical information should help visitors make informed decisions.

**Reliability**

Reservation requests must be validated on the server, and unavailable products must not be reserved again.

**Simplicity**

The initial application does not require customer registration or online payment.

### 2. Scope — What Must the Website Provide?

The Scope plane translates business and user objectives into functional and content requirements.

#### Must Have — Essential Functionality

- Browse Available Koi.
- View Koi Details.
- Filter Koi by Category.
- Manage Shopping Cart.
- Submit a Reservation Request.
- Prevent Duplicate Reservations.
- Manage Products.
- Manage Orders.
- Responsive Navigation.
- Responsive Catalogue.

These functions form the core of the application.

#### Should Have — Supporting Functionality

- Delivery Information.
- Contact Information.
- Search Koi.

These features improve product discovery and help visitors make informed reservation decisions.

#### Could Have — Optional Enhancements

- Frequently Asked Questions.
- Reservation Confirmation Email.
- Featured Koi Carousel.

These enhancements provide additional value but should not delay completion of the essential functionality.

#### Content Requirements

The website should provide:

- Product names and descriptions.
- Product prices.
- Product sizes and relevant characteristics.
- Product photographs.
- Availability information.
- Delivery information.
- Contact information.
- Reservation guidance.

The scope is managed using MoSCoW prioritisation and GitHub Issues.

A feature is not considered complete solely because its backend functionality exists. User-facing behaviour must also be implemented and verified.

### 3. Structure — How Is Information Organised?

The Structure plane defines the information architecture and user interaction flows.

#### Information Architecture

The planned customer-facing structure is:

```text
Koi4Sale
│
├── Home
│
├── Catalogue
│   ├── Category Filtering
│   ├── Search
│   └── Product Details
│
├── Cart
│   └── Reservation Request
│       └── Confirmation
│
├── Delivery Information
│
├── Contact
│
└── Frequently Asked Questions
```

Administrative functionality is accessed separately through authenticated Django Admin.

#### Breadcrumb Navigation

Breadcrumb navigation provides an additional way for visitors to understand
their location within the website.

The breadcrumbs follow the page hierarchy:

- Catalogue: Home → Catalogue
- Product Details: Home → Catalogue → Product Name

Parent pages are displayed as links, allowing visitors to navigate backwards
through the website hierarchy.

The current page is displayed as text rather than a link.

Breadcrumbs are implemented using a reusable Django template:

`templates/includes/breadcrumbs.html`

The component receives the current page label and optional parent page
information through Django template context.

#### Primary User Flow — Reservation

The main customer journey follows these steps:

1. Open the home page or catalogue.
2. Browse, search or filter available koi.
3. Open an individual product page.
4. Review photographs, characteristics and price.
5. Add one or more koi to the cart.
6. Review selected products and the total.
7. Enter contact information.
8. Submit a reservation request.
9. Receive confirmation or validation feedback.

#### Reservation Terminology

The interface must distinguish a reservation request from a completed purchase.

Preferred terminology includes:

- **Add to Cart**
- **View Cart**
- **Request Reservation**
- **Reservation Request Received**

The application should not suggest that payment has been completed when no payment has occurred.

#### Error Handling

Users should receive clear feedback when:

- Required form information is missing.
- Submitted information is invalid.
- A selected koi is no longer available.
- A reservation cannot be completed.
- A requested product does not exist.
- A search or category filter returns no results.

<!-- TODO: Add the final user-flow diagram. -->

### 4. Skeleton — Where Do Elements Go?

The Skeleton plane defines the arrangement of navigation, content and interactive elements before final visual styling.

Wireframes will be used to document the layout of important pages.

#### Global Navigation

**Desktop**

- The logo appears on the left.
- Navigation links appear horizontally on the right.
- A shopping cart icon with an item counter provides direct access to the cart.
- A hamburger menu is not displayed on desktop.

**Mobile**

- The brand logo remains visible on the left.
- A shopping cart icon remains visible even when the navigation menu is collapsed.
- The cart counter displays the number of selected products.
- A hamburger button opens the collapsed navigation.
- Navigation links remain readable and easy to select.

#### Shared Footer

The footer is implemented as a reusable Django template.

- The brand logo links to the home page.
- Copyright information includes the current year.
- Desktop layouts position the logo and copyright information horizontally.
- Mobile layouts stack the footer elements vertically.
- The page layout keeps the footer at the bottom of the viewport when content is short.

#### Home Page

**Desktop Layout**

- A prominent hero section introduces the website.
- The main heading and description appear beside a large koi photograph.
- A primary **Shop Koi** button leads to the catalogue.
- The hero uses a two-column layout with text on the left and a koi photograph on the right.
- The primary call-to-action links directly to the product catalogue.

**Mobile Layout**

- Hero content is arranged vertically.
- The main heading and calls-to-action appear before the image.
- Text remains readable without horizontal scrolling.
- Buttons are large enough for comfortable touch interaction.

#### Catalogue

- Products are displayed using a responsive grid.
- Product photographs are visually prominent.
- Product names, prices and important characteristics are clearly displayed.
- Each product provides a route to its detail page.
- Category filtering and search controls are positioned where visitors can easily find them.
- The number of columns adapts to screen width.

#### Product Details

- Product photographs are easy to examine.
- Product information is organised logically.
- Price and availability are clearly visible.
- The Add to Cart action is prominent for available products.
- Content remains readable on mobile devices.

#### Cart and Reservation Form

- Selected koi are displayed with photographs and prices.
- The total price is clearly presented.
- Products can be removed from the cart.
- The reservation form uses clearly labelled fields.
- Validation errors appear near relevant inputs where appropriate.
- Confirmation explains the next steps.

<!-- TODO: Add desktop and mobile wireframes. -->

### 5. Surface — What Does the Interface Look Like?

The Surface plane defines the visual identity of the application.

The previous Koi4Sale website serves as a visual reference, while the Django implementation uses Bootstrap components and custom CSS.

#### Colour Palette

| Design Element     | Colour    | Purpose                                        |
| ------------------ | --------- | ---------------------------------------------- |
| Primary Background | `#111827` | Dark navy background.                          |
| Primary Accent     | `#fe5a08` | Buttons, highlights and important actions.     |
| Primary Text       | `#ffffff` | Main headings and text on dark surfaces.       |
| Secondary Text     | `#9ca3af` | Supporting descriptions.                       |
| Surface Background | `#1f2937` | Cards, form controls and contrasting surfaces. |

These colours represent the intended design and will be reviewed during accessibility and contrast testing.

#### Typography

The website uses the Inter variable font, self-hosted in WOFF2 format.

Inter was selected for its readability, clean appearance and suitability
for responsive interfaces.

The font is applied consistently across headings, body text, navigation
and interface components.

The project includes the font's SIL Open Font License 1.1.

Typography should provide:

- Clear heading hierarchy.
- Readable body text.
- Consistent font sizes.
- Appropriate line spacing.
- Strong contrast between text and backgrounds.

#### Visual Hierarchy

The home page should guide attention through:

1. Brand identity.
2. Main value proposition.
3. Primary Shop Koi action.
4. Koi photography.
5. Available or featured products.

#### Responsive Design

Bootstrap 5.3 provides the responsive grid and navigation components.

The layout adapts to:

- Mobile devices.
- Tablets.
- Desktop screens.

The current navigation uses Bootstrap's `lg` breakpoint at 992px.

The breakpoint may be adjusted if testing shows that another layout works better.

The home page hero uses a two-column layout on larger screens and stacks
its content vertically on smaller screens.

The catalogue uses Bootstrap's responsive grid utilities to adjust the
number of product columns according to viewport width.

Mobile container spacing was customised to provide more comfortable
horizontal padding.

The shared footer adapts its layout to the available screen width.

#### Accessibility

The interface should include:

- Semantic HTML landmarks.
- Meaningful image alternative text.
- Keyboard-accessible navigation.
- Visible keyboard focus indicators.
- Accessible form labels.
- Appropriate colour contrast.
- Clear validation messages.
- Responsive content without unnecessary horizontal scrolling.

<!-- TODO: Add final screenshots and visual testing evidence. -->

### UX Review Checklist

Before completing a frontend user story, the implementation should be reviewed against all five UX planes.

| Plane     | Review Question                                                 |
| --------- | --------------------------------------------------------------- |
| Strategy  | Does the feature solve a genuine user or business need?         |
| Scope     | Is the feature required for the MVP or an optional enhancement? |
| Structure | Can users find and complete the relevant interaction?           |
| Skeleton  | Does the layout work on mobile, tablet and desktop?             |
| Surface   | Is the interface visually consistent, readable and accessible?  |

UX decisions should be revisited when testing reveals usability problems.

---

## Database Design

Koi4Sale uses a relational database designed around unique koi products and reservation requests.

The database design includes the following entities:

- `Product`
- `ProductImage`
- `ProductHighlight`
- `Customer`
- `Order`
- `OrderItem`

The final Entity Relationship Diagram must be checked against the implemented Django models before submission.

<!-- TODO: Add the final ERD image. -->

### Database Relationships

The principal relationships include:

- A product can have multiple images.
- Each product image belongs to one product.
- A customer can have multiple orders.
- Each order belongs to one customer.
- An order contains selected products through order items.
- Product highlights are associated with their relevant products.

The final documentation will describe foreign keys, cardinality, deletion rules and database constraints.

### Product Availability

Each koi is represented by one `Product` record.

Product status determines whether a koi is available for reservation.

The planned status values are:

- `available`
- `reserved`
- `sold`
- `unavailable`

Product status acts as the source of truth for availability.

The reservation workflow changes a successfully reserved product from:

```text
available → reserved
```

The application should not maintain a duplicate availability boolean without a specific requirement.

### Reservation Integrity

Product availability is checked on the server when a reservation request is submitted.

The reservation process must ensure that:

- Unavailable products are rejected.
- Related customer and order records are created consistently.
- Successfully reserved products are marked as reserved.
- Failed requests do not leave partially created orders.

The final documentation will describe the transaction and concurrency safeguards used in the implementation.

---

## Development Process

The application is developed incrementally using GitHub Issues, milestones and small commits.

Testable functionality follows a Test-Driven Development approach where appropriate.

### Test-Driven Development

The development cycle is:

```text
RED → GREEN → REFACTOR
```

**RED**

1. Define the expected behaviour.
2. Write an automated test.
3. Run the test.
4. Confirm that it fails for the expected reason.

**GREEN**

1. Implement the minimum functionality required.
2. Run the test.
3. Confirm that the test passes.

**REFACTOR**

1. Improve the implementation where appropriate.
2. Preserve the expected behaviour.
3. Run the relevant tests again.

### Version Control

Development changes are committed in small, meaningful stages.

Tests and implementation may be committed separately to provide a clear development history.

Where tests are added after implementation, they are treated as retrospective test coverage rather than presented as a completed RED phase.

### Frontend Development

Frontend functionality is reviewed against the Five Planes of UX.

Django tests are used to verify rendered templates and application behaviour.

JavaScript tests verify client-side functionality.

Visual styling and responsive behaviour are also checked through manual browser testing.

A successful Django template test does not by itself prove that the interface behaves correctly in a browser.

#### Unplanned UX Improvements

During responsive testing, an additional usability issue was identified:
the shopping cart link was hidden inside the collapsed mobile navigation,
making it difficult for visitors to see whether products had been added.

To address this issue, a shopping cart indicator was introduced as an
additional Should Have feature.

The implementation uses:

- A Bootstrap Icons `cart3` SVG icon in the header.
- A counter showing the number of products stored in `localStorage`.
- JavaScript to update the counter when cart contents change.
- CSS positioning to display the counter above the cart icon.
- Responsive navigation that keeps the cart accessible on mobile devices.

The same cart indicator is used on desktop and mobile.

This improvement was added during development in response to usability
testing rather than being part of the original project scope.

### Reusable Frontend Components

The frontend uses reusable Django template components to maintain
consistency across pages.

Shared components include:

- `base.html` — common document structure and page layout.
- `includes/header.html` — branding and responsive navigation.
- `includes/footer.html` — branding and copyright information.
- `includes/breadcrumbs.html` — contextual page navigation.

Individual pages extend the base template and include shared components
where appropriate.

Bootstrap 5.3 provides responsive layout utilities, while custom CSS
defines the website's visual identity.

The frontend follows a mobile-first approach, with layouts progressively
adapting to larger viewport widths.

### Development Milestones

<!-- TODO: Add the final GitHub milestone names, descriptions and completion status. -->

**Current Development Stage:** Frontend and User Experience.

The current focus is responsive navigation, shared layout and page presentation.

---

## Features

This section will be expanded as functionality is implemented and verified.

### Implemented / Under Verification

- Django models and relational data storage.
- Product catalogue backend.
- Category filtering functionality.
- Product search functionality.
- Product image storage using Cloudinary.
- Customer and reservation records.
- Server-side reservation processing.
- Client-side shopping cart.
- Responsive shopping cart icon with a live item counter.
- Persistent cart count based on browser localStorage.
- Direct access to the cart from the mobile header without opening the navigation menu.
- JavaScript cart tests.
- Shared Django base template.
- Responsive header with custom SVG branding.
- Bootstrap collapsible mobile navigation.
- Reusable breadcrumb navigation.
- Responsive home page hero with koi photography.
- Responsive product catalogue grid.
- Shared responsive footer with SVG branding.
- Sticky footer layout for pages with limited content.
- Self-hosted Inter variable font.
- Custom dark colour scheme and orange brand accent.
- Automated tests for shared template assets.
- Automated tests for navigation markup.
- Primary product image selection with a database uniqueness constraint.
- Primary Cloudinary images in the catalogue, cart and reservation confirmation.
- Static placeholder images when no primary image is available.

### In Progress

- Final catalogue styling.
- Product detail page styling.
- Cart and reservation form presentation.
- Delivery, contact and FAQ page presentation.
- Complete responsive and accessibility testing.

### Optional Features

- Reservation confirmation email.
- Featured koi carousel.

Features will be moved into the implemented section only after they have been completed and verified.

<!-- TODO: Add screenshots and descriptions of completed features. -->

---

## Testing

Testing is performed throughout development.

Automated tests verify important application behaviour, while manual testing checks complete user journeys and visual presentation.

Detailed test cases, expected and actual results, screenshots and bug retesting will be documented in a separate **TESTING.md** file.

### Automated Testing

#### Django Tests

Django tests cover:

- Models.
- Views.
- Forms.
- Business rules.
- Reservation processing.
- Authentication and authorisation.
- Rendered template output.

Run the Django test suite:

```bash
python3 manage.py test
```

Shared template tests are located in:

```text
tests/django/
```

Run the base template tests:

```bash
python3 manage.py test tests.django.test_base
```

Run the navigation tests:

```bash
python3 manage.py test tests.django.test_header
```

These tests verify rendered HTML and expected attributes.

They do not establish that Bootstrap assets load successfully in a real browser or that responsive components behave correctly.

#### JavaScript Tests

Jest is used to test client-side cart functionality.

Install JavaScript dependencies:

```bash
npm install
```

Run JavaScript tests:

```bash
npm test
```

### Manual Testing

Manual testing will cover:

- Navigation between pages.
- Mobile navigation behaviour.
- Product browsing.
- Category filtering.
- Product search.
- Product details.
- Cart interactions.
- Reservation form submission.
- Validation errors.
- Reservation confirmation.
- Unavailable product handling.
- Breadcrumb navigation and parent-page links.
- Logo links in the header and footer.
- Footer positioning on pages with limited content.

### Responsive Testing

The website will be tested at mobile, tablet and desktop viewport widths.

Testing will verify:

- Layout adaptation.
- Readable text.
- Appropriate image scaling.
- Accessible navigation.
- Usable forms.
- Absence of unintended horizontal scrolling.
- Hero image and text stacking on mobile devices.
- Header logo scaling across viewport widths.
- Footer layout adaptation.
- Breadcrumb readability on narrow screens.

### Accessibility Testing

Accessibility checks will include:

- Keyboard navigation.
- Focus visibility.
- Image alternative text.
- Form labels.
- Colour contrast.
- Semantic HTML.
- Accessible navigation controls.
- Breadcrumb navigation landmarks and current-page identification.

### Code Validation and Quality

Planned checks include:

- HTML validation.
- CSS validation.
- JavaScript code quality.
- Python code quality.
- Browser compatibility.
- Chrome DevTools Lighthouse.

### Testing Evidence

<!-- TODO: Add actual test results, screenshots, validator reports and browser coverage. -->

---

## Bugs

Significant bugs discovered during development will be documented with:

1. Description of the problem.
2. Cause of the problem.
3. Steps taken to resolve it.
4. Retesting results.

### Known Bugs

<!-- TODO: Add verified bugs and fixes. -->

---

## Technologies Used

### Languages and Frameworks

- Python
- Django
- PostgreSQL
- HTML5
- CSS3
- JavaScript
- Bootstrap 5.3

### Application and Infrastructure

- Django Templates
- Django ORM
- Django Admin
- Cloudinary
- WhiteNoise
- Gunicorn
- Heroku

### Testing Tools

- Django Test Framework
- Jest
- Chrome DevTools
- Lighthouse

### Development Tools

- Visual Studio Code
- Git
- GitHub
- GitHub Issues
- GitHub Milestones
- Photopea — SVG image editing.

### Bootstrap

Bootstrap 5.3 is loaded through a Content Delivery Network.

The project does not require Bootstrap to be installed as a Python dependency.

Bootstrap provides:

- Responsive grid utilities.
- Navigation components.
- Collapsible mobile navigation.
- Buttons and form styling.
- Reusable layout utilities.

Custom CSS is used to establish the visual identity of Koi4Sale.

<!-- TODO: Add exact dependency versions from requirements.txt and package.json. -->

---

## Deployment

**Live Website:** https://koi-for-sale-2e89f5c55c63.herokuapp.com/

Koi4Sale is deployed on Heroku.

The production environment uses a relational database, Cloudinary for uploaded images and WhiteNoise for static files.

### Local Development

Follow these steps to run the application locally.

#### 1. Clone the Repository

```bash
git clone https://github.com/ShvetsViktor/koi-4-sale.git
cd koi-4-sale
```

#### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

#### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

The application uses environment variables for sensitive configuration.

Required values include:

- Django secret key.
- Database connection information.
- Cloudinary credentials.

Local configuration uses `env.py` according to the project's Django settings.

Sensitive configuration must not be committed to Git.

Production configuration is managed through Heroku Config Vars.

#### 5. Apply Database Migrations

```bash
python3 manage.py migrate
```

#### 6. Start the Development Server

```bash
DEBUG=True python3 manage.py runserver
```

The application will be available at:

`http://127.0.0.1:8000/`

Django debugging is disabled by default.

Setting `DEBUG=True` enables debugging for the current command without modifying the shared settings module.

Debugging must remain disabled in production.

#### 7. Run Automated Tests

Django:

```bash
python3 manage.py test
```

JavaScript:

```bash
npm install
npm test
```

### Production Deployment — Heroku

The final deployment guide will document the exact steps used to deploy the application.

The process includes:

1. Creating a Heroku application.
2. Configuring a production PostgreSQL database.
3. Setting the required environment variables.
4. Configuring production security settings.
5. Installing application dependencies.
6. Starting Gunicorn using the Procfile.
7. Applying database migrations.
8. Collecting static files.
9. Verifying the deployed application.

<!-- TODO: Add the complete, reproducible Heroku deployment instructions. -->

### Development and Production Environments

The application uses the same Django settings module for development and production.

The `DEBUG` environment variable controls debugging behaviour.

- `DEBUG=True` enables local debugging.
- `DEBUG=False` disables debugging.
- Debugging is disabled by default when the variable is not provided.

Production credentials are stored in Heroku Config Vars.

Sensitive configuration files are excluded from version control.

### Static Files — WhiteNoise

Koi4Sale uses Django's static files framework and WhiteNoise to serve static assets in production.

Static assets include:

- Custom CSS.
- JavaScript.
- Favicons.
- Default product images.

The project uses the following Django settings:

- `STATIC_URL` defines the URL prefix.
- `STATICFILES_DIRS` identifies the source static directory.
- `STATIC_ROOT` specifies the collection destination.
- `WhiteNoiseMiddleware` enables static asset delivery.
- `CompressedManifestStaticFilesStorage` provides compressed and versioned files.

Static assets are referenced in templates using Django's `{% static %}` template tag.

Collect static files using:

```bash
python3 manage.py collectstatic --noinput
```

During deployment, Heroku collects the static files for production use.

WhiteNoise serves collected files when `DEBUG=False`.

The generated `staticfiles/` directory is excluded from version control.

Bootstrap is loaded separately through a CDN.

### Product Image Storage — Cloudinary

Koi4Sale uses Cloudinary for persistent storage and delivery of uploaded product photographs.

Heroku's filesystem is ephemeral, meaning uploaded files cannot be relied upon to persist between deployments or dyno restarts.

Cloudinary provides external image storage independent of the application filesystem.

#### Cloudinary Configuration

The application uses the Cloudinary Python SDK and Django integration.

Credentials are configured using the `CLOUDINARY_URL` environment variable.

Example format:

```text
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

Actual credentials are stored in local configuration and Heroku Config Vars.

They must not be committed to the repository.

#### Product Images

Product photographs are managed through the `ProductImage` model.

Each image belongs to a specific product through a foreign key relationship.

The image field uses Cloudinary's `CloudinaryField`:

```python
image = CloudinaryField(
    "image",
    folder="koi4sale/products"
)
```

Uploaded images are organised under the configured Cloudinary folder.

A product can have multiple photographs.

One image may be designated as the primary image.

Each product can have one primary image, identified by is_primary=True. A database constraint prevents multiple primary images from being assigned to the same product.

The primary image is displayed in the catalogue, shopping cart and reservation confirmation. The product detail page displays all available photographs.

If no primary image is available, the application displays a static placeholder.

#### Fallback Images

Products without uploaded photographs display a default placeholder.

The placeholder is stored at:

```text
static/images/default.png
```

It is served through Django's static files configuration and WhiteNoise.

The fallback does not require a separate `ProductImage` database record.

#### Production Behaviour

Uploaded photographs are delivered through Cloudinary rather than Heroku's filesystem.

This allows images to remain available after application redeployment or dyno restarts.

Image upload and retrieval have been tested in local development and the deployed Heroku environment.

---

## Attribution, Credits and Acknowledgements

### Original Koi4Sale Design

The author's previous Koi4Sale website, developed with Next.js, React and TypeScript, provides visual and UX inspiration.

The Django project is a separate implementation using server-rendered templates, Bootstrap and vanilla JavaScript.

### Frameworks and Libraries

- **Django** — Python web framework.
- **Bootstrap 5.3** — responsive layout and interface components.
- **Cloudinary** — persistent product image storage.
- **WhiteNoise** — static asset delivery.
- **Jest** — JavaScript testing.

### Code Attribution

Custom application code is written and adapted for this project.

External code, tutorials, documentation, images and other resources will be attributed where applicable.

### Fonts

- **Inter** — designed by Rasmus Andersson and contributors.
  Used for typography throughout the website.
  The font is self-hosted in WOFF2 format and distributed
  under the SIL Open Font License 1.1 (OFL-1.1).
  Source: https://github.com/rsms/inter
  License: [`LICENSE.txt`](static/fonts/LICENSE.txt)

### Icons

- **Bootstrap Icons** — The `cart3` SVG icon used in the responsive navigation is provided by Bootstrap Icons and licensed under the MIT License. [Bootstrap Icons](https://icons.getbootstrap.com/icons/cart3/).

### Graphics

- [Photopea](https://www.photopea.com/) — used to edit SVG graphics.

---

## Repository Structure

The project is organised as follows:

```koi-4-sale/
├── config/                 # Django project configuration
├── orders/                 # Cart and reservation functionality
├── products/               # Product catalogue and images
├── static/
│   ├── css/                # Custom styles
│   ├── fonts/              # Self-hosted Inter font and licence
│   ├── images/             # Logo, hero and placeholder images
│   └── js/                 # Client-side JavaScript
├── templates/
│   ├── includes/
│   │   ├── breadcrumbs.html
│   │   ├── footer.html
│   │   └── header.html
│   ├── base.html
│   └── home.html
├── tests/
│   └── django/             # Django template tests
├── manage.py
├── requirements.txt
├── package.json
├── Procfile
├── README.md
└── TESTING.md
```

The repository excludes local virtual environments, generated static files, database files and sensitive configuration.

---

## Future Improvements

The following features may be considered after the MVP has been completed.

### Advanced Search and Filtering

Extend the existing catalogue search and category filtering with additional options such as size, price and other product characteristics.

### Featured Koi Carousel

Highlight selected products on the home page to improve product discovery.

### Reservation Confirmation Email

Send customers an email containing their reservation details and information about the next steps.

### Improved Reservation Management

Expand administrative functionality for managing reservation requests and customer communication.

### Additional Automated Testing

Introduce further browser-based tests to verify complete user journeys and responsive interactions.

### Accessibility Improvements

Continue refining keyboard navigation, contrast, form accessibility and usability based on testing results.

These improvements are not considered part of the completed application unless they are implemented and verified.
