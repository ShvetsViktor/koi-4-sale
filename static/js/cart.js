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

/**
 * Fetch product details for items saved in the shopping cart.
 *
 * @returns {Promise<object[]>} Product details from the server.
 */
async function fetchCartProducts() {
  const cart = getCart();

  if (cart.length === 0) {
    return [];
  }

  const params = new URLSearchParams();

  cart.forEach((id) => {
    params.append('ids', id);
  });

  const response = await fetch(`/cart/products/?${params.toString()}`);

  if (!response.ok) {
    throw new Error('Failed to fetch cart products.');
  }

  const data = await response.json();

  return data.products;
}

/**
 * Render shopping cart products with their names and prices.
 *
 * @param {object[]} products - Product details returned by Django.
 */
function renderCart(products) {
  const cartItems = document.querySelector('#cart-items');

  cartItems.innerHTML = '';

  products.forEach((product) => {
    const item = document.createElement('div');
    const name = document.createElement('h2');
    const price = document.createElement('p');

    name.textContent = product.name;
    price.textContent = `£${product.price}`;

    item.append(name, price);
    cartItems.appendChild(item);
  });
}

/**
 * Initialise the shopping cart page.
 */
async function initCartPage() {
  const products = await fetchCartProducts();

  renderCart(products);
}

/**
 * Handle an Add to Cart button click.
 *
 * @param {MouseEvent} event - Button click event.
 */
function handleAddToCart(event) {
  const productId = Number(event.currentTarget.dataset.productId);

  const cart = getCart();
  const updatedCart = addToCart(cart, productId);

  saveCart(updatedCart);
  event.currentTarget.textContent = 'Added to Cart';
}

/**
 * Initialise Add to Cart buttons.
 */
function initCartButtons() {
  const buttons = document.querySelectorAll('[data-product-id]');
  const cart = getCart();

  buttons.forEach((button) => {
    const productId = Number(button.dataset.productId);

    if (cart.includes(productId)) {
      button.textContent = 'Added to Cart';
    }

    button.addEventListener('click', handleAddToCart);
  });
}

if (typeof module !== 'undefined') {
  module.exports = {
    addToCart,
    removeFromCart,
    saveCart,
    getCart,
    handleAddToCart,
    initCartButtons,
    fetchCartProducts,
    renderCart,
    initCartPage,
  };
}
