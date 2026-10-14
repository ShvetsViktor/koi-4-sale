const { addToCart, getCart, saveCart, handleAddToCart } = require('../static/js/cart');

describe('Shopping Cart UI', () => {
  beforeEach(() => {
    localStorage.clear();

    document.body.innerHTML = `
      <button data-product-id="1">Add to Cart</button>
    `;
  });

  test('adds a product to the cart when the button is clicked', () => {
    const button = document.querySelector('[data-product-id]');

    button.addEventListener('click', handleAddToCart);
    button.click();

    expect(getCart()).toEqual([1]);
  });
});
