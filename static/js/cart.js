/**
 * Add a product ID to the shopping cart.
 *
 * @param {number[]} cart - Current product IDs.
 * @param {number} productId - Product ID to add.
 * @returns {number[]} Updated cart.
 */
function addToCart(cart, productId) {
  if (cart.includes(productId)) {
    return cart;
  }

  return [...cart, productId];
}

if (typeof module !== 'undefined') {
  module.exports = { addToCart };
}
