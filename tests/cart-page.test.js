const { fetchCartProducts, renderCart, initCartPage } = require('../static/js/cart');

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
});
