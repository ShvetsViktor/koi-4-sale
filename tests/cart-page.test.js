const {
  fetchCartProducts,
  renderCart,
  initCartPage,
  addCartItemsToForm,
  getCart,
  clearCart,
} = require('../static/js/cart');

describe('Shopping Cart Page', () => {
  beforeEach(() => {
    localStorage.clear();
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('fetches product details for saved cart IDs', async () => {
    localStorage.setItem('koi4sale_cart', '[5,6]');

    // Mock fetch() to return a Promise with predefined data instead of making a real HTTP request.
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        products: [
          { id: 5, name: 'Kohaku', price: '150.00' },
          { id: 6, name: 'Showa', price: '200.00' },
        ],
      }),
    });

    const products = await fetchCartProducts();

    expect(global.fetch).toHaveBeenCalledWith('/cart/products/?ids=5&ids=6');

    expect(products).toHaveLength(2);
    expect(products[0].name).toBe('Kohaku');
  });

  test('renders product names and prices in the cart', () => {
    document.body.innerHTML = '<div id="cart-items"></div>';

    const products = [
      {
        id: 5,
        name: 'Japanese Kohaku',
        price: '150.00',
        status: 'available',
      },
      {
        id: 6,
        name: 'Japanese Showa',
        price: '200.00',
        status: 'available',
      },
    ];

    renderCart(products);

    const cartItems = document.querySelector('#cart-items');

    expect(cartItems.textContent).toContain('Japanese Kohaku');
    expect(cartItems.textContent).toContain('150.00');
    expect(cartItems.textContent).toContain('Japanese Showa');
    expect(cartItems.textContent).toContain('200.00');
  });

  test('renders a remove button for each cart product', () => {
    document.body.innerHTML = '<div id="cart-items"></div>';

    const products = [
      {
        id: 5,
        name: 'Japanese Kohaku',
        price: '150.00',
        status: 'available',
      },
      {
        id: 6,
        name: 'Japanese Showa',
        price: '200.00',
        status: 'available',
      },
    ];

    renderCart(products);

    const removeButtons = document.querySelectorAll('#cart-items [data-remove-id]');

    expect(removeButtons).toHaveLength(2);
    expect(removeButtons[0].dataset.removeId).toBe('5');
    expect(removeButtons[1].dataset.removeId).toBe('6');
  });

  test('loads and displays cart products', async () => {
    document.body.innerHTML = '<div id="cart-items"></div>';

    localStorage.setItem('koi4sale_cart', '[5]');

    // Mock fetch() to return a Promise with predefined data instead of making a real HTTP request.
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        products: [
          {
            id: 5,
            name: 'Japanese Kohaku',
            price: '150.00',
            status: 'available',
          },
        ],
      }),
    });

    await initCartPage();

    expect(global.fetch).toHaveBeenCalledWith('/cart/products/?ids=5');

    const cartItems = document.querySelector('#cart-items');

    expect(cartItems.textContent).toContain('Japanese Kohaku');
    expect(cartItems.textContent).toContain('150.00');
  });

  test('removes a product from the cart when Remove is clicked', () => {
    document.body.innerHTML = '<div id="cart-items"></div>';

    localStorage.setItem('koi4sale_cart', '[5,6]');

    const products = [
      {
        id: 5,
        name: 'Japanese Kohaku',
        price: '150.00',
        status: 'available',
      },
      {
        id: 6,
        name: 'Japanese Showa',
        price: '200.00',
        status: 'available',
      },
    ];

    renderCart(products);

    const removeButton = document.querySelector('[data-remove-id="5"]');

    removeButton.click();

    expect(JSON.parse(localStorage.getItem('koi4sale_cart'))).toEqual([6]);

    const cartItems = document.querySelector('#cart-items');

    expect(cartItems.textContent).not.toContain('Japanese Kohaku');
    expect(cartItems.textContent).toContain('Japanese Showa');
  });

  test('updates cart total when a product is removed', () => {
    document.body.innerHTML = `
      <div id="cart-items"></div>
      <div id="cart-total-price"></div>
    `;

    localStorage.setItem('koi4sale_cart', '[1,2]');

    const products = [
      { id: 1, name: 'Kohaku', price: '250.00', image_url: '/kohaku.jpg' },
      { id: 2, name: 'Sanke', price: '175.50', image_url: '/sanke.jpg' },
    ];

    renderCart(products);

    expect(document.querySelector('#cart-total-price').textContent)
      .toBe('£425.50');

    document.querySelector('[data-remove-id="1"]').click();

    expect(document.querySelector('#cart-total-price').textContent)
      .toBe('£175.50');
  });

  test('adds cart product IDs to the reservation form', () => {
    document.body.innerHTML = `
    <form id="reservation-form"></form>
  `;

    localStorage.setItem('koi4sale_cart', '[5,6]');

    addCartItemsToForm();

    const inputs = document.querySelectorAll('#reservation-form input[name="product_ids"]');

    expect(inputs).toHaveLength(2);
    expect(inputs[0].value).toBe('5');
    expect(inputs[1].value).toBe('6');
  });

  test('adds product IDs when the reservation form is submitted', () => {
    document.body.innerHTML = `
    <div id="cart-items"></div>
    <form id="reservation-form"></form>
  `;

    localStorage.setItem('koi4sale_cart', '[5,6]');

    // Mock fetch() to return a Promise with predefined data instead of making a real HTTP request.
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        products: [
          { id: 5, name: 'Japanese Kohaku', price: '150.00' },
          { id: 6, name: 'Japanese Showa', price: '200.00' },
        ],
      }),
    });

    return initCartPage().then(() => {
      const form = document.querySelector('#reservation-form');

      form.dispatchEvent(
        new Event('submit', {
          bubbles: true,
          cancelable: true,
        })
      );

      const inputs = form.querySelectorAll('input[name="product_ids"]');

      expect(inputs).toHaveLength(2);
      expect(inputs[0].value).toBe('5');
      expect(inputs[1].value).toBe('6');
    });
  });

  test('clears the shopping cart', () => {
    localStorage.setItem('koi4sale_cart', '[5,6]');

    clearCart();

    expect(getCart()).toEqual([]);
  });

  test('hides the reservation form when the cart is empty', async () => {
    document.body.innerHTML = `
    <div id="cart-items"></div>
    <div id="empty-cart" hidden></div>
    <form id="reservation-form" hidden></form>
  `;

    await initCartPage();

    expect(document.querySelector('#reservation-form').hidden).toBe(true);
    expect(document.querySelector('#empty-cart').hidden).toBe(false);
  });

  test('shows empty cart message after removing the last product', () => {
    document.body.innerHTML = `
    <div id="cart-items"></div>
    <div id="empty-cart" hidden></div>
    <form id="reservation-form"></form>
  `;

    localStorage.setItem('koi4sale_cart', '[5]');

    renderCart([{ id: 5, name: 'Japanese Kohaku', price: '150.00' }]);

    document.querySelector('[data-remove-id="5"]').click();

    expect(getCart()).toEqual([]);
    expect(document.querySelector('#cart-items').children).toHaveLength(0);
    expect(document.querySelector('#reservation-form').hidden).toBe(true);
    expect(document.querySelector('#empty-cart').hidden).toBe(false);
  });

  test('displays £0.00 after removing the last product', () => {
    document.body.innerHTML = `
      <div id="cart-items"></div>
      <div id="cart-total-price"></div>
      <div id="empty-cart" hidden></div>
      <form id="reservation-form"></form>
    `;

    localStorage.setItem('koi4sale_cart', '[1]');

    const products = [
      { id: 1, name: 'Kohaku', price: '250.00', image_url: '/kohaku.jpg' },
    ];

    renderCart(products);

    document.querySelector('[data-remove-id="1"]').click();

    expect(document.querySelector('#cart-total-price').textContent)
      .toBe('£0.00');
  });
});
