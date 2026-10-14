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

/**
 * Remove a product ID from the shopping cart.
 *
 * @param {number[]} cart - Current product IDs.
 * @param {number} productId - Product ID to remove.
 * @returns {number[]} Updated cart.
 */
function removeFromCart(cart, productId) {
  return cart.filter((id) => id !== productId);
}

/**
 * Save shopping cart contents to localStorage.
 *
 * @param {number[]} cart - Product IDs to save.
 */
function saveCart(cart) {
  localStorage.setItem('koi4sale_cart', JSON.stringify(cart));
}

/**
 * Retrieve shopping cart contents from localStorage.
 *
 * @returns {number[]} Saved product IDs.
 */
function getCart() {
  return JSON.parse(localStorage.getItem('koi4sale_cart') || '[]');
}

if (typeof module !== 'undefined') {
  module.exports = { addToCart, removeFromCart, saveCart, getCart };
}
