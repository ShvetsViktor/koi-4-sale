const { fetchCartProducts } = require('../static/js/cart');

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
});
