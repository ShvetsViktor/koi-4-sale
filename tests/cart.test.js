const { addToCart } = require('../static/js/cart');

describe('Shopping Cart', () => {
  test('adds a product to an empty cart', () => {
    // Arrange: Create an empty shopping cart.
    const cart = [];

    // Act: Add a product with ID 1.
    const result = addToCart(cart, 1);

    // Assert: The cart should contain the product ID.
    expect(result).toEqual([1]);
  });
});
