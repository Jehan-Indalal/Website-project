let cart = JSON.parse(localStorage.getItem("cart")) || [];

function saveCart() {
  localStorage.setItem("cart", JSON.stringify(cart));
  const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);
  localStorage.setItem("total", total);
}

function getTotal() {
  return cart.reduce((sum, item) => sum + item.price * item.qty, 0);
}

function addToCart(name, price) {
  const existing = cart.find(item => item.name === name);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ name, price, qty: 1 });
  }
  saveCart();
  alert(name + " added to cart!");
}

function changeQty(name, delta) {
  const item = cart.find(i => i.name === name);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) {
    cart = cart.filter(i => i.name !== name);
  }
  saveCart();
  updateOrderPage();
}

function removeFromCart(name) {
  cart = cart.filter(i => i.name !== name);
  saveCart();
  updateOrderPage();
}

function updateOrderPage() {
  let orderList = document.getElementById("orderList");
  let totalBox = document.getElementById("total");

  if (!orderList || !totalBox) return;

  orderList.innerHTML = "";

  if (cart.length === 0) {
    orderList.innerHTML = '<p style="text-align:center;color:#999;">Your cart is empty.</p>';
  }

  cart.forEach(item => {
    orderList.innerHTML += `
      <div class="order-item">
        <p>${item.name}</p>
        <div class="qty-controls">
          <button class="qty-btn" onclick="changeQty('${item.name}', -1)">-</button>
          <span class="qty-value">${item.qty}</span>
          <button class="qty-btn" onclick="changeQty('${item.name}', 1)">+</button>
        </div>
        <p class="item-price">${item.price * item.qty} EGP</p>
        <button class="cart-delete-btn" onclick="removeFromCart('${item.name}')">
          <i class="fa-solid fa-trash"></i>
        </button>
      </div>
    `;
  });

  totalBox.innerText = getTotal();
}

function toggleVisa(show) {
  const visaFields = document.getElementById("visaFields");
  visaFields.style.display = show ? "block" : "none";
}

function confirmOrder() {
  const selected = document.querySelector('input[name="payment"]:checked');
  if (!selected) {
    alert("Please select a payment method (Cash or Visa).");
    return;
  }

  const fullName = document.getElementById('fullName').value.trim();
  const address  = document.getElementById('address').value.trim();
  const phone    = document.getElementById('phone').value.trim();

  if (!fullName || !address || !phone) {
    alert("Please fill in all user information.");
    return;
  }

  fetch('/confirm_order', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      full_name:      fullName,
      address:        address,
      phone:          phone,
      payment_method: selected.value,
      total:          getTotal()
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      localStorage.removeItem("cart");
      localStorage.removeItem("total");
      cart = [];
      alert("Order confirmed! Thank you!");
      window.location.href = "/";
    }
  });
}

window.onload = function () {
  cart = JSON.parse(localStorage.getItem("cart")) || [];
  updateOrderPage();
};
