const { getCart, handleAddToCart, initCartButtons } = require('../static/js/cart');

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

  test('initialises Add to Cart buttons', () => {
    document.body.innerHTML = `
    <button data-product-id="1">Add to Cart</button>
    <button data-product-id="2">Add to Cart</button>
  `;

    initCartButtons();

    document.querySelector('[data-product-id="1"]').click();
    document.querySelector('[data-product-id="2"]').click();

    expect(getCart()).toEqual([1, 2]);
  });

  test('updates button text after adding a product to the cart', () => {
    const button = document.querySelector('[data-product-id]');

    initCartButtons();
    button.click();

    expect(button.textContent).toBe('✓ Added to Cart');
  });

  test('shows Added to Cart for products already in the cart', () => {
    localStorage.setItem('koi4sale_cart', '[1]');

    initCartButtons();

    const button = document.querySelector('[data-product-id="1"]');

    expect(button.textContent).toBe('✓ Added to Cart');
  });
});
