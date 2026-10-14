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

  test('does not add the same product twice', () => {
    // Arrange: The cart already contains product 1.
    const cart = [1, 2];

    // Act: Attempt to add product 1 again.
    const result = addToCart(cart, 1);

    // Assert: The cart must not contain duplicates.
    expect(result).toEqual([1, 2]);
  });
});
