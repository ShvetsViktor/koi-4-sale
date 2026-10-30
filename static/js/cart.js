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
 * Calculate the total price of products in the shopping cart.
 *
 * @param {object[]} products - Product details returned by Django.
 * @returns {number} Total price in GBP.
 */
function calculateCartTotal(products) {
  return products.reduce(
    (total, product) => total + Math.round(Number(product.price) * 100),
    0,
  ) / 100;
}

/**
 * Update the displayed shopping cart total.
 *
 * @param {object[]} products - Products currently displayed in the cart.
 */
function updateCartTotal(products) {
  const totalElement = document.querySelector('#cart-total-price');

  if (totalElement) {
    totalElement.textContent = `£${calculateCartTotal(products).toFixed(2)}`;
  }
}

/**
 * Save shopping cart contents to localStorage.
 *
 * @param {number[]} cart - Product IDs to save.
 */
function saveCart(cart) {
  localStorage.setItem('koi4sale_cart', JSON.stringify(cart));
  updateCartCount();
}

/**
 * Clear all products from the shopping cart.
 */
function clearCart() {
  localStorage.removeItem('koi4sale_cart');
  updateCartCount();
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
 * Update cart item counters in the navigation.
 */
function updateCartCount() {
  const count = getCart().length;

  document.querySelectorAll('.cart-count').forEach((badge) => {
    badge.textContent = count;
    badge.hidden = count === 0;
  });
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
 * Toggle the reservation form and empty cart message based on cart contents.
 */
function updateCartEmptyState() {
  const form = document.querySelector('#reservation-form');
  const emptyCart = document.querySelector('#empty-cart');
  const hasProducts = getCart().length > 0;

  if (form) {
    form.hidden = !hasProducts && !form.querySelector('.alert-danger');
  }

  if (emptyCart) {
    emptyCart.hidden = hasProducts;
  }
}

/**
 * Render shopping cart products with images, names, prices and remove buttons.
 *
 * @param {object[]} products - Product details returned by Django.
 */
function renderCart(products) {
  const cartItems = document.querySelector('#cart-items');

  cartItems.innerHTML = '';

  updateCartTotal(products);

  products.forEach((product) => {
    const item = document.createElement('article');
    const image = document.createElement('img');
    const details = document.createElement('div');
    const name = document.createElement('h2');
    const price = document.createElement('p');
    const removeButton = document.createElement('button');

    item.className = 'cart-item';

    image.className = 'cart-item-image';
    image.src = product.image_url;
    image.alt = product.name;
    image.loading = 'lazy';

    details.className = 'cart-item-details';

    name.className = 'cart-item-name';
    name.textContent = product.name;

    price.className = 'cart-item-price';
    price.textContent = `£${product.price}`;

    removeButton.type = 'button';
    removeButton.className = 'btn btn-outline-secondary';
    removeButton.textContent = 'Remove';
    removeButton.dataset.removeId = product.id;

    removeButton.addEventListener('click', () => {
      const cart = getCart();
      const updatedCart = removeFromCart(cart, product.id);

      saveCart(updatedCart);
      item.remove();

      const remainingProducts = products.filter(
        (cartProduct) => updatedCart.includes(cartProduct.id),
      );

      updateCartTotal(remainingProducts);
      updateCartEmptyState();
    });

    details.append(name, price, removeButton);
    item.append(image, details);
    cartItems.appendChild(item);
  });
}

/**
 * Initialise the shopping cart page.
 */
async function initCartPage() {
  const form = document.querySelector('#reservation-form');
  const errorElement = document.querySelector('#cart-error');
  const retryButton = document.querySelector('#cart-retry');

  if (retryButton) {
    retryButton.onclick = initCartPage;
  }

  try {
    const products = await fetchCartProducts();

    renderCart(products);
    updateCartEmptyState();

    if (errorElement) {
      errorElement.hidden = true;
    }

    if (retryButton) {
      retryButton.hidden = true;
    }

    if (form && products.length > 0) {
      form.hidden = false;
      form.onsubmit = addCartItemsToForm;
    }
  } catch (error) {
    if (errorElement) {
      errorElement.textContent = 'Unable to load your cart. Please try again.';
      errorElement.hidden = false;
    }

    if (retryButton) {
      retryButton.hidden = false;
    }

    if (form) {
      form.hidden = true;
    }
  }
}

/**
 * Add shopping cart product IDs as hidden reservation form fields.
 */
function addCartItemsToForm() {
  const form = document.querySelector('#reservation-form');
  const cart = getCart();

  form.querySelectorAll('input[name="product_ids"]').forEach((input) => {
    input.remove();
  });

  cart.forEach((productId) => {
    const input = document.createElement('input');

    input.type = 'hidden';
    input.name = 'product_ids';
    input.value = productId;

    form.appendChild(input);
  });
}

/**
 * Handle an Add to Cart button click.
 *
 * @param {MouseEvent} event - Button click event.
 */
function handleAddToCart(event) {
  const button = event.currentTarget;
  const productId = Number(button.dataset.productId);
  const cart = getCart();
  const updatedCart = addToCart(cart, productId);

  saveCart(updatedCart);

  button.textContent = '✓ Added to Cart';
  button.classList.replace('btn-primary', 'btn-outline-secondary');
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
      button.textContent = '✓ Added to Cart';
      button.classList.replace('btn-primary', 'btn-outline-secondary');
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
    addCartItemsToForm,
    clearCart,
    updateCartEmptyState,
    calculateCartTotal,
  };
}
