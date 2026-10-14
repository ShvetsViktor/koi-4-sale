const { fetchCartProducts, renderCart, initCartPage, addCartItemsToForm } = require('../static/js/cart');

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

    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ products: [] }),
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
});
