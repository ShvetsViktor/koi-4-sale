# Koi4Sale – Django Koi Reservation Website

<!-- TODO: Add responsive website mockup. -->

**Live Website:** https://koi-for-sale-2e89f5c55c63.herokuapp.com/

## Overview

Koi4Sale is a full-stack web application for browsing individual Japanese koi and submitting reservation requests without creating a customer account or making an online payment.

The project is developed for the **Code Institute Level 5 Diploma in Web Application Development – Unit 3: Back End Development** assessment. It uses **Django**, a relational database, Django Templates, **Bootstrap 5.3**, custom CSS and vanilla JavaScript.

Each koi is represented as a unique product rather than a variation of a stock item. Visitors can browse available koi, view detailed product information and images, search and filter the catalogue, manage a client-side shopping cart and submit a reservation request.

The server validates product availability before creating an order and its associated order items, storing customer contact details directly in the order. When a reservation is successfully submitted, the selected koi are marked as reserved to prevent duplicate reservations.

Customer registration and authentication are intentionally excluded from the initial project scope. Authorised administrators manage products, images and reservation
requests, including customer contact information, through Django Admin.

The project is developed incrementally using GitHub Issues, milestones and automated testing. Testable functionality follows the **RED → GREEN → REFACTOR** development cycle where appropriate.

The previous Koi4Sale website, developed using Next.js, React and TypeScript, serves as a visual and UX reference. This project is a separate implementation using Django Templates, HTML, CSS, Bootstrap and vanilla JavaScript.

> **Project Status:** Completed and deployed. Core reservation functionality,
> responsive layouts, automated testing and project documentation have been finalised.

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
- Contact the seller directly by email.
- Use the website comfortably on mobile, tablet and desktop devices.

### Site Owner Goals

- Present available koi professionally and accurately.
- Maintain product details, photographs and availability.
- Store customer and reservation information in a relational database.
- Manage products and reservation requests through authenticated administration.
- Prevent duplicate reservations.
- Preserve historical order information.
- Provide customers with a straightforward way to make enquiries.
- Keep the application secure, maintainable and suitable for future development.

### Assessment Goals

- Develop a full-stack web application using Python and Django.
- Design and implement a relational database.
- Use Django ORM and meaningful relationships between models.
- Implement Create, Read, Update and Delete functionality.
- Process forms and validate submitted information on the server.
- Apply authentication and authorisation through Django Admin to protect administrative functionality without requiring customer accounts.
- Build a responsive frontend using HTML, custom CSS, Bootstrap and JavaScript.
- Implement automated testing for important application behaviour.
- Use Git and GitHub throughout development.
- Document UX decisions, database design, development and testing.
- Deploy the application with a production relational database.

### Why This Project Suits the Brief

Koi4Sale is suitable for the Unit 3 Back End Development assessment because its core functionality depends on persistent relational data and server-side business logic.

Categories, products, product images, orders and order items are connected through database relationships. Customer contact details are stored directly in reservation records.

The reservation workflow demonstrates an important business rule: the server must verify product availability before accepting a reservation request.

When a reservation is successfully created, the selected koi must become unavailable for further reservation.

Django Admin provides authenticated administrative functionality for managing application records.

The reservation form demonstrates server-side form processing and validation. A separate contact form is not required for the application's core reservation functionality.

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
- Clear delivery information.
- An accessible email address for enquiries.

The site owner needs:

- Reliable product availability management.
- Persistent customer and reservation records.
- Straightforward product administration.
- Protection against duplicate reservations.
- A simple way for customers to initiate contact.
- A maintainable application.

These requirements inform the project's functionality and UX decisions.

---

## User Stories and Prioritisation

User stories describe the needs of visitors, customers and administrators.

They are organised by functionality rather than assigned additional story numbers.

GitHub Issues and milestones are used to track implementation tasks, acceptance criteria and development progress. Issue titles follow the same naming conventions as the user stories documented here.

The project uses **MoSCoW prioritisation** to distinguish essential functionality from optional enhancements.

### MoSCoW Prioritisation

| User Story                     | Priority    | Status      | Purpose                                                                                      |
| ------------------------------ | ----------- | ----------- | -------------------------------------------------------------------------------------------- |
| Browse Available Koi           | Must Have   | Implemented | Display koi available for reservation.                                                       |
| View Koi Details               | Must Have   | Implemented | Provide detailed product information and photographs.                                        |
| Filter Koi by Category         | Must Have   | Implemented | Allow visitors to browse koi by category.                                                    |
| Manage Shopping Cart           | Must Have   | Implemented | Allow visitors to manage selected koi.                                                       |
| Shopping Cart Indicator        | Should Have | Implemented | Display the number of selected products and provide quick access to the cart across devices. |
| Submit a Reservation Request   | Must Have   | Implemented | Process customer reservation requests.                                                       |
| Prevent Duplicate Reservations | Must Have   | Implemented | Prevent unavailable koi from being reserved again.                                           |
| Manage Products                | Must Have   | Implemented | Provide authenticated product administration.                                                |
| Manage Orders                  | Must Have   | Implemented | Provide authenticated reservation management.                                                |
| Responsive Navigation          | Must Have   | Implemented | Provide accessible navigation across screen sizes.                                           |
| Responsive Catalogue           | Must Have   | Implemented | Display product cards appropriately on different devices.                                    |
| Delivery Information           | Should Have | Implemented | Explain delivery arrangements and conditions.                                                |
| Contact Information            | Should Have | Implemented | Provide an email address and a direct email contact option.                                  |
| Search Koi                     | Should Have | Implemented | Help visitors find koi using search terms.                                                   |
| Frequently Asked Questions     | Could Have  | Planned     | Answer common customer questions.                                                            |
| Reservation Confirmation Email | Could Have  | Planned     | Send customers confirmation of their reservation request.                                    |
| Featured Koi Carousel          | Could Have  | Planned     | Highlight selected products on the home page.                                                |

All Must Have and Should Have user stories have been implemented.

The three Could Have user stories remain planned for future development
and are not included in the current release.

Final verification of implemented features is documented in
[TESTING.md](TESTING.md).

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
- Successful submission creates an order containing the customer's contact details.
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
- Cancelling an order restores its reserved products to `available`.

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
- The page explains the delivery process.
- The main delivery stages are presented clearly.
- Visitors can navigate to the Delivery page from the main navigation.
- The page is responsive on mobile and desktop devices.

#### Contact Information

As a **visitor**, I want to find the seller's contact details so that I can ask questions about koi, delivery or reservations.

**Acceptance Criteria**

- Visitors can access a dedicated Contact page.
- The seller's email address is clearly displayed.
- The email address is a clickable `mailto:` link.
- A **Send an Email** button provides a direct email contact option.
- The Contact page is accessible through the main navigation.
- The page displays correctly on mobile, tablet and desktop devices.

**Implementation Notes**

The Contact page provides a direct email contact method rather than a web-based enquiry form.

Visitors can copy the displayed email address or use the email links to open their preferred email application.

This approach was selected to keep the initial application focused on its core reservation functionality and avoid introducing an additional form-processing workflow.

A dedicated Django contact form may be considered as a future enhancement.

### Additional User Stories

#### Shopping Cart Indicator

As a **visitor**, I want to see how many koi are in my shopping cart without opening it so that I can keep track of my selections while browsing.

**Acceptance Criteria**

- The header displays the number of products currently in the cart.
- The indicator updates immediately when products are added or removed.
- The cart icon remains visible when the cart is empty.
- The item counter is hidden when the cart contains no products.
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
- Receive reservation requests from interested customers.
- Provide a direct email contact option for general enquiries.
- Maintain accurate product availability.
- Manage customer and reservation information efficiently.

#### User Objectives

- Discover available koi.
- Compare individual fish.
- Access reliable product information.
- Understand the reservation process.
- Submit a reservation request with confidence.
- Contact the seller when additional information is needed.

#### Design Principles

**Clarity**

Visitors should immediately understand what the website offers and which products are available.

**Confidence**

Product photographs, descriptions, prices and practical information should help visitors make informed decisions.

**Reliability**

Reservation requests must be validated on the server, and unavailable products must not be reserved again.

**Simplicity**

The initial application does not require customer registration or online payment.

General enquiries are handled through direct email links rather than an additional web form.

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
- Shopping Cart Indicator.

These features improve product discovery, navigation and communication.

#### Could Have — Optional Enhancements

- Frequently Asked Questions.
- Reservation Confirmation Email.
- Featured Koi Carousel.

These features are planned as potential future enhancements
and are not included in the current release.

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

#### Scope Exclusions

The initial application does not include:

- Customer registration.
- Online payments.
- A dedicated web-based contact form.
- Automated processing of general email enquiries.

Customer reservation requests are processed through the Django reservation form.

General enquiries are handled through the seller's displayed email address and `mailto:` links.

The scope is managed using MoSCoW prioritisation and GitHub Issues.

A feature is not considered complete solely because its backend functionality exists. User-facing behaviour must also be implemented and verified.

### 3. Structure — How Is Information Organised?

The Structure plane defines the information architecture and user interaction flows.

#### Information Architecture

The customer-facing structure is:

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
└── Contact
    └── Email Contact
```

Administrative functionality is accessed separately through authenticated Django Admin.

#### Breadcrumb Navigation

Breadcrumb navigation provides an additional way for visitors to understand their location within the website.

The breadcrumbs follow the page hierarchy:

- Catalogue: Home → Catalogue
- Product Details: Home → Catalogue → Product Name

Parent pages are displayed as links, allowing visitors to navigate backwards through the website hierarchy.

The current page is displayed as text rather than a link.

Breadcrumbs are implemented using a reusable Django template:

`templates/includes/breadcrumbs.html`

The component receives the current page label and optional parent page information through Django template context.

Breadcrumbs are used where they improve navigation within the product catalogue. They are not required on every informational page.

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

#### Secondary User Flow — General Enquiry

Visitors who need additional information can:

1. Open the Contact page from the main navigation.
2. Read the displayed email address.
3. Copy the address or select **Send an Email**.
4. Compose their enquiry using their preferred email application.

The website does not collect or store general enquiries through a separate contact form.

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

- Required reservation information is missing.
- Submitted reservation information is invalid.
- A selected koi is no longer available.
- A reservation cannot be completed.
- A requested product does not exist.
- A search or category filter returns no results.

The Contact page does not perform server-side enquiry validation because it does not submit a web form.

#### Reservation User Flow Diagram

The diagram illustrates the main reservation process,
including successful submission and validation failures.

```mermaid
flowchart TD
    A["Home / Catalogue"] --> B["Browse, Search or Filter Koi"]
    B --> C["View Product Details"]
    C --> D["Add to Cart"]
    D --> E["Review Cart"]
    E --> F["Enter Contact Details"]
    F --> G["Submit Reservation Request"]
    G --> H{"Form Valid?"}

    H -->|No| I["Display Validation Errors"]
    I --> F

    H -->|Yes| J{"Products Available?"}

    J -->|No| K["Display Availability Error"]
    K --> E

    J -->|Yes| L["Create Order and Order Items"]
    L --> M["Mark Products as Reserved"]
    M --> N["Display Reservation Confirmation"]

    style A fill:#1f2937,color:#ffffff,stroke:#fe5a08
    style N fill:#1f2937,color:#ffffff,stroke:#fe5a08
    style I fill:#7f1d1d,color:#ffffff
    style K fill:#7f1d1d,color:#ffffff
```

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
- A secondary **Shipping Info** link leads to the Delivery page.
- The hero uses a two-column layout with text on the left and a koi photograph on the right.

**Mobile Layout**

- Hero content is arranged vertically.
- The main heading and calls-to-action appear before the image.
- Text remains readable without horizontal scrolling.
- Interactive elements are suitable for touch interaction.

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

#### Delivery Page

The Delivery page provides a dedicated informational layout.

- A prominent hero introduces the delivery process.
- Supporting text explains the importance of careful handling.
- A delivery-related image supports the content.
- A primary button links to the delivery steps.
- Four numbered cards explain the main stages:
  1. Order Confirmation.
  2. Preparation.
  3. Packing and Shipping.
  4. Receiving Your Koi.
- The layout adapts to mobile and desktop devices.

#### Contact Page

The Contact page uses a simple, responsive layout.

- A **Get in Touch** heading identifies the page.
- A short introductory paragraph explains its purpose.
- A contact information card displays the seller's email address.
- The email address is clickable.
- A prominent **Send an Email** button provides a second contact option.
- The content is aligned with the main page container.
- The content width is limited on larger screens to improve readability.
- On smaller screens, the content uses the available width.

The page deliberately avoids a separate enquiry form to keep the contact process straightforward.

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

Inter was selected for its readability, clean appearance and suitability for responsive interfaces.

The font is applied consistently across headings, body text, navigation and interface components.

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
5. Clear navigation towards the product catalogue.

Informational pages use a consistent heading hierarchy, supporting text and clearly identified actions.

#### Responsive Design

Bootstrap 5.3 provides the responsive grid and navigation components.

The layout adapts to:

- Mobile devices.
- Tablets.
- Desktop screens.

The current navigation uses Bootstrap's `lg` breakpoint at 992px.

The breakpoint may be adjusted if testing shows that another layout works better.

The home page hero uses a two-column layout on larger screens and stacks its content vertically on smaller screens.

The catalogue uses Bootstrap's responsive grid utilities to adjust the number of product columns according to viewport width.

Mobile container spacing was customised to provide more comfortable horizontal padding.

The shared footer adapts its layout to the available screen width.

The Contact page uses a constrained content width on larger screens while maintaining alignment with the main page container.

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
- Descriptive links and buttons.

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

The database contains five Django models:

- `Category`
- `Product`
- `ProductImage`
- `Order`
- `OrderItem`

The database stores product information, categories, product images, customer contact details and reservation records.

Product data allows visitors to browse and compare individual koi, while order data enables the seller to process reservation requests and maintain a record of previous reservations.

Customer contact information is stored directly in the `Order` model. A separate customer model is not required because visitors can submit reservation requests without creating an account.

### Entity Relationship Diagram

![Koi4Sale Entity Relationship Diagram](assets/readme/images/erd.png)

### Database Relationships

The database uses the following relationships:

- **Category → Product:** One category can contain multiple products. Each product belongs to one category.
- **Product → ProductImage:** One product can have multiple images. Each image belongs to one product.
- **Order → OrderItem:** One reservation request can contain multiple order items.
- **Product → OrderItem:** Each order item references one product.

The relationships are implemented using Django `ForeignKey` fields.

Deleting a category containing products is prevented using `on_delete=models.PROTECT`.

Deleting a product automatically deletes its associated images through `on_delete=models.CASCADE`.

Deleting an order automatically deletes its order items.

Deleting a product referenced by an order item is prevented using `on_delete=models.PROTECT`, preserving the integrity of reservation records.

### Product Availability

Each koi is represented by one `Product` record.

Product status determines whether a koi is available for reservation.

The available status values are:

- `available`
- `reserved`
- `sold`
- `unavailable`

Product status acts as the source of truth for availability.

The reservation workflow changes a successfully reserved product from:

    available → reserved

The application does not require a duplicate availability boolean.

When an order is cancelled, its reserved products are returned
to `available`, allowing them to be reserved again.

### Database Constraints

The application uses database constraints to maintain data integrity.

**Primary Product Image**

Each product can have only one image marked as primary.

The `ProductImage` model uses a conditional `UniqueConstraint` to prevent multiple primary images for the same product.

**Unique Products Within an Order**

The `OrderItem` model uses a `UniqueConstraint` on the combination of `order` and `product`.

This prevents the same product from appearing more than once within a single reservation request.

### Reservation Integrity

Product availability is checked on the server when a reservation request is submitted.

The reservation process ensures that:

- Unavailable products are rejected.
- Related order and order item records are created consistently.
- Successfully reserved products are marked as reserved.
- Failed requests do not leave partially created orders.

Database transactions are used to maintain consistency during reservation processing.

The application stores the product price in `OrderItem` when a reservation is created.

This preserves the price associated with the reservation even if the product price changes later.

### Security Considerations

Security was considered throughout the development of Koi4Sale to protect customer information, prevent unauthorised access and maintain the integrity of reservation records.

#### Sensitive Configuration

Sensitive information, including the Django secret key, database credentials and Cloudinary credentials, is stored in environment variables rather than directly in the source code.

Local configuration files containing secrets are excluded from version control using `.gitignore`.

Production credentials are managed through Heroku Config Vars.

#### Authentication and Authorisation

Administrative functionality is provided through Django Admin.

Access to product and reservation management requires authentication and appropriate staff permissions.

Customer registration is not required because visitors only need to provide contact information when submitting a reservation request.

#### Form Validation and CSRF Protection

The reservation form uses Django's server-side validation to check submitted customer information.

Django's CSRF protection is used to protect form submissions against cross-site request forgery.

Product availability is checked on the server rather than relying solely on information displayed in the browser.

#### Database Integrity

Reservation processing uses database transactions to ensure that related records are created consistently.

Product availability is checked before a reservation is accepted.

Successfully reserved products are marked as reserved, preventing them from being reserved again.

If a reservation fails, the transaction prevents partially created reservation records.

#### Production Configuration

Django debugging is disabled by default and remains disabled in the production environment.

Sensitive configuration values are not included in the public GitHub repository.

Uploaded product images are stored using Cloudinary rather than relying on Heroku's temporary filesystem.

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

During responsive testing, an additional usability issue was identified: the shopping cart link was hidden inside the collapsed mobile navigation, making it difficult for visitors to see whether products had been added.

To address this issue, a shopping cart indicator was introduced as an additional Should Have feature.

The implementation uses:

- A Bootstrap Icons `cart3` SVG icon in the header.
- A counter showing the number of products stored in `localStorage`.
- JavaScript to update the counter when cart contents change.
- CSS positioning to display the counter above the cart icon.
- Responsive navigation that keeps the cart accessible on mobile devices.

The same cart indicator is used on desktop and mobile.

This improvement was added during development in response to usability testing rather than being part of the original project scope.

#### Contact Page Scope Adjustment

The initial Contact user story proposed a Django enquiry form with server-side validation and submission processing.

During development, the scope was reviewed against the project's primary objectives and available development time.

The decision was made to provide direct email contact instead of introducing a separate enquiry-processing workflow.

The revised implementation includes:

- A dedicated Contact page.
- A visible email address.
- A clickable `mailto:` email link.
- A **Send an Email** button.
- Responsive styling.
- Integration with the main navigation.
- Automated tests for page rendering and contact information.

The reservation form remains the application's primary example of customer-facing Django form processing and server-side validation.

This scope adjustment preserves a clear way for customers to contact the seller while prioritising completion and testing of the core reservation functionality.

The corresponding GitHub Issue and acceptance criteria were updated to reflect the implemented feature.

### Optional Feature Scope Review

During development, the project scope was reviewed to prioritise
the completion and testing of the core reservation functionality.

The Frequently Asked Questions page and Featured Koi Carousel
were deferred to future development.

Both remain classified as Could Have features under MoSCoW
prioritisation and are not required for the current release.

### Reusable Frontend Components

The frontend uses reusable Django template components to maintain consistency across pages.

Shared components include:

- `base.html` — common document structure and page layout.
- `includes/header.html` — branding and responsive navigation.
- `includes/footer.html` — branding and copyright information.
- `includes/breadcrumbs.html` — contextual page navigation.
- `includes/hero.html` — reusable hero section for informational pages.

Individual pages extend the base template and include shared components where appropriate.

Bootstrap 5.3 provides responsive layout utilities, while custom CSS defines the website's visual identity.

The frontend follows a mobile-first approach, with layouts progressively adapting to larger viewport widths.

### Development Milestones

Development was organised into five GitHub milestones to track
implementation progress and maintain a structured workflow.

| Milestone                                  | Description                                                                                                                 | GitHub Progress          |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| Milestone 1 — Project Setup & Deployment   | Configure the Django project, development environment, database and initial Heroku deployment.                              | 100% — 1/1 issues closed |
| Milestone 2 — Database & Product Catalogue | Implement the relational database, product models, catalogue, category filtering and product administration.                | 100% — 5/5 issues closed |
| Milestone 3 — Reservation System           | Implement the shopping cart, reservation processing, validation, duplicate reservation prevention and order management.     | 100% — 6/6 issues closed |
| Milestone 4 — Frontend & User Experience   | Develop responsive Django templates, navigation, search, contact information, delivery information and frontend components. | 100% — 7/7 issues closed |
| Milestone 5 — Testing & Documentation      | Verify application functionality, test user stories and prepare assessment documentation.                                   | 100% — 3/3 issues closed |

GitHub milestone percentages reflect the completion of assigned issues
rather than independent verification of every application requirement.

Although all issues assigned to Milestone 5 are closed, final
cross-browser testing, validation and documentation review are
being completed separately.

The remaining work includes final frontend refinement,
responsive testing and preparation of assessment evidence.

---

## Features

This section presents the main features implemented in Koi4Sale.

Each feature is linked to the relevant user stories described in
[User Stories and Prioritisation](#user-stories-and-prioritisation).

Screenshots demonstrate the implemented interface, while functional
verification and test results are documented in [TESTING.md](TESTING.md).

### Home Page

The home page introduces Koi4Sale and explains the purpose of the website.

A responsive hero section features koi photography and provides direct
navigation to the product catalogue and delivery information.

**Related User Stories:** Responsive Navigation.

![Koi4Sale Home Page](assets/readme/images/home.png)

### Product Catalogue

The catalogue displays individual koi available for reservation.

Visitors can search for products, filter by category and navigate
to individual product detail pages. The responsive grid adapts
to different screen sizes.

**Related User Stories:** Browse Available Koi, Filter Koi by Category,
Search Koi, Responsive Catalogue.

![Product Catalogue](assets/readme/images/catalogue.png)

### Product Details

Each product has a dedicated page displaying its photographs,
price, description and available characteristics.

Visitors can examine an individual koi and add it to their
shopping cart when the product is available.

**Related User Stories:** View Koi Details.

![Product Details](assets/readme/images/product-details.png)

### Shopping Cart

The shopping cart allows visitors to review selected koi,
remove products and view the total price before submitting
a reservation request.

Cart contents are stored in browser localStorage, allowing
selections to persist while navigating between pages.

**Related User Stories:** Manage Shopping Cart.

![Shopping Cart](assets/readme/images/cart.png)

### Reservation Form

The reservation form collects customer contact information
without requiring registration or online payment.

Submitted information and product availability are validated
on the server. Successful reservations are stored in the
database, and selected products are marked as reserved.

**Related User Stories:** Submit a Reservation Request,
Prevent Duplicate Reservations.

![Reservation Form](assets/readme/images/reservation-form.png)

### Reservation Confirmation

After a successful reservation, customers are shown a
confirmation page containing their reservation number,
selected products and total price.

The page explains that the request has been received and
that no online payment has been taken.

**Related User Stories:** Submit a Reservation Request.

![Reservation Confirmation](assets/readme/images/reservation-confirmation.png)

### Delivery Information

The Delivery page explains the koi transportation process
through four clearly organised stages.

A Browse Our Koi button provides a direct route back to
the product catalogue.

**Related User Stories:** Delivery Information.

![Delivery Page](assets/readme/images/delivery.png)

### Contact Information

The Contact page displays the seller's email address and
provides a direct email contact option.

Visitors can use the clickable email address or the
Send an Email button to open their preferred email application.

**Related User Stories:** Contact Information.

![Contact Page](assets/readme/images/contact.png)

### Responsive Navigation

The shared header provides navigation across desktop,
tablet and mobile devices.

A shopping cart icon remains accessible on mobile when
the navigation menu is collapsed. Its counter updates
when products are added or removed.

**Related User Stories:** Responsive Navigation,
Shopping Cart Indicator.

![Responsive Navigation](assets/readme/images/responsive-navigation.png)

### Django Administration

Django Admin provides authenticated administrative
management of products, categories, product images
and reservation requests.

Administrators can create, view, update and delete
records where permitted, manage product availability
and update reservation statuses.

**Related User Stories:** Manage Products, Manage Orders.

![Django Administration](assets/readme/images/django-admin.png)

### Planned Future Enhancements

The following optional features remain planned for future development:

- Frequently Asked Questions page.
- Reservation confirmation email.
- Featured koi carousel.

These features are classified as Could Have in the
MoSCoW prioritisation and are not part of the current release.

---

## Testing

Koi4Sale was developed using automated and manual testing to verify
application functionality, database integrity, usability and
responsive behaviour.

Automated tests cover Django models, views, forms, reservation
processing and JavaScript shopping cart functionality.

Manual testing evaluates complete user journeys, responsive layouts,
browser compatibility and accessibility.

Detailed test cases, expected and actual results, validation reports,
screenshots and bug fixes are documented in [TESTING.md](TESTING.md).

### Automated Testing

#### Django Tests

Django's built-in testing framework is used to verify:

- Database models and relationships.
- Product catalogue and filtering.
- Product search.
- Product image handling.
- Reservation form validation.
- Reservation creation and cancellation.
- Duplicate reservation prevention.
- Administrative access and permissions.
- Rendered templates and navigation.
- Delivery and Contact pages.

Run the complete Django test suite:

```bash
python3 manage.py test
```

#### JavaScript Tests

Jest is used to test client-side shopping cart functionality,
including product selection, localStorage persistence and
cart interactions.

Install dependencies:

```bash
npm install
```

Run the JavaScript test suite:

```bash
npm test
```

### Manual Testing

Manual testing covers the main customer journeys:

- Browsing, searching and filtering available koi.
- Viewing product details and photographs.
- Adding and removing products from the cart.
- Submitting valid and invalid reservation requests.
- Preventing reservations of unavailable products.
- Viewing reservation confirmation.
- Navigating between website pages.
- Using the Delivery and Contact pages.
- Managing products and reservations through Django Admin.

### Responsive and Accessibility Testing

The application is tested across mobile, tablet and desktop
viewport sizes.

Testing includes:

- Responsive layouts and navigation.
- Image scaling and content readability.
- Keyboard navigation and visible focus.
- Form labels and validation feedback.
- Colour contrast and semantic HTML.
- Absence of unintended horizontal scrolling.

### Code Validation

The final application is checked using appropriate validation
and code-quality tools, including:

- HTML validation.
- CSS validation.
- Python code-quality checks.
- JavaScript code-quality checks.
- Chrome DevTools Lighthouse.

### Test Results

Final automated test counts, manual testing outcomes,
browser compatibility results and validation reports
are recorded in [TESTING.md](TESTING.md).

### Bugs and Fixes

Issues identified during development are documented together
with their causes, resolutions and retesting results.

See [TESTING.md](TESTING.md) for detailed bug reports.

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
- Home and delivery page images.

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

Each product can have one primary image, identified by `is_primary=True`. A database constraint prevents multiple primary images from being assigned to the same product.

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

### AI-Assisted Content

ChatGPT (OpenAI) was used to assist with the creation and
visual styling of the Entity Relationship Diagram (ERD).

The diagram represents the database models and relationships
implemented in the Django application.

The decorative koi illustrations were generated as part
of the diagram and were not sourced from external websites.

---

## Repository Structure

The project is organised as follows:

```text
koi-4-sale/
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
│   ├── contact.html
│   ├── delivery.html
│   └── home.html
├── tests/
│   └── django/
│       ├── test_contact.py
│       └── test_delivery.py
├── manage.py
├── requirements.txt
├── package.json
├── Procfile
├── README.md
└── TESTING.md
```

The diagram shows the principal directories and selected files rather than every file in the repository.

The repository excludes local virtual environments, generated static files, database files and sensitive configuration.

---

## Future Improvements

The following features may be considered after the MVP has been completed.

### Contact Form

Introduce a dedicated Django contact form to allow visitors to submit enquiries directly through the website.

Possible functionality includes:

- Name, email, subject and message fields.
- Server-side validation.
- Email delivery or database storage.
- Success and error messages.
- Spam protection.
- Automated submission tests.

The current Contact page already provides direct email contact, so this enhancement is not required for the initial release.

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
