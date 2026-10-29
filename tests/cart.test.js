const {
  addToCart,
  removeFromCart,
  saveCart,
  getCart,
  calculateCartTotal,
} = require('../static/js/cart');

describe('Shopping Cart', () => {
  test('adds a product to an empty cart', () => {
    // Arrange: Create an empty shopping cart.
    const cart = [];

    // Act: Add a product with ID 1.
    const result = addToCart(cart, 1);

    // Assert: The cart should contain the product ID.
    expect(result).toEqual([1]);
  });

  test('does not add the same product twice', () => {
    // Arrange: The cart already contains product 1.
    const cart = [1, 2];

    // Act: Attempt to add product 1 again.
    const result = addToCart(cart, 1);

    // Assert: The cart must not contain duplicates.
    expect(result).toEqual([1, 2]);
  });

  test('removes a product from the cart', () => {
    // Arrange: Create a cart containing three products.
    const cart = [1, 2, 3];

    // Act: Remove product with ID 2.
    const result = removeFromCart(cart, 2);

    // Assert: Only the selected product should be removed.
    expect(result).toEqual([1, 3]);
  });

  test('saves cart contents to localStorage', () => {
    // Arrange: Create a cart containing two products.
    const cart = [1, 2];

    // Act: Save the cart to browser storage.
    saveCart(cart);

    // Assert: Verify that product IDs were saved.
    expect(localStorage.getItem('koi4sale_cart')).toBe('[1,2]');
  });

  test('retrieves cart contents from localStorage', () => {
    // Arrange: Store two product IDs in localStorage.
    localStorage.setItem('koi4sale_cart', '[1,2]');

    // Act: Retrieve the saved cart.
    const result = getCart();

    // Assert: The original array should be restored.
    expect(result).toEqual([1, 2]);
  });
});

describe('Cart Total', () => {
  test('calculates the total price of cart products', () => {
    const products = [
      { id: 1, price: '250.00' },
      { id: 2, price: '175.50' },
      { id: 3, price: '100.00' },
    ];

    expect(calculateCartTotal(products)).toBe(525.50);
  });

  test('returns zero for an empty cart', () => {
    expect(calculateCartTotal([])).toBe(0);
  });
});