// State Management
let cart = [];

// Navigation Switcher
function switchView(viewName) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));

    document.getElementById(`view-${viewName}`).classList.add('active');
    document.getElementById(`nav-${viewName}`).classList.add('active');

    if (viewName === 'cart') renderCart();
    if (viewName === 'admin') checkAdminStatus();
}

// Cart Actions
async function addToCart(productId) {
    const existing = cart.find(item => item.id === productId);

    if (existing) {
        existing.qty++;
    } else {
        const response = await fetch(`/api/products/${productId}`);

        if (!response.ok) {
            alert('Unable to retrieve product.');
            return;
        }

        const product = await response.json();

        cart.push({
            ...product,
            qty: 1
        });
    }

    updateCartBadge();
    alert('Item added to cart!');
}

function updateCartBadge() {
    const count = cart.reduce((acc, item) => acc + item.qty, 0);
    document.getElementById('cart-count').innerText = count;
}

function changeQty(id, delta) {
    const item = cart.find(i => i.id === id);
    if (item) {
        item.qty = parseInt(delta) || 1;
        renderCart();
    }
}

function removeFromCart(id) {
    cart = cart.filter(i => i.id !== id);
    renderCart();
    updateCartBadge();
}

// Render Cart View
function renderCart() {
    const tbody = document.getElementById('cart-items');
    const emptyMsg = document.getElementById('cart-empty');

    if (cart.length === 0) {
        tbody.innerHTML = '';
        emptyMsg.style.display = 'block';
        document.getElementById('cart-total').innerText = '$0.00';
        return;
    }

    emptyMsg.style.display = 'none';
    let total = 0;

    tbody.innerHTML = cart.map(item => {
        const subtotal = item.sell * item.qty;
        total += subtotal;
        return `
                    <tr>
                        <td>${escapeHTML(item.title)}</td>
                        <td>$${item.sell.toFixed(2)}</td>
                        <td class="qty-controls">
                            <input type="number" min="1" value="${item.qty}" onchange="changeQty(${item.id}, this.value)">
                        </td>
                        <td>$${subtotal.toFixed(2)}</td>
                        <td><button class="btn-remove" onclick="removeFromCart(${item.id})">Remove</button></td>
                    </tr>
                `;
    }).join('');

    document.getElementById('cart-total').innerText = `$${total.toFixed(2)}`;
}

// Security Validation & Sanitization Practice
function escapeHTML(str) {
    // Anti-XSS Sanitization
    return str.replace(/[&<>'"]/g,
        tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
}

async function handleCheckout(e) {
    document.getElementById('email-err').style.display = 'none';
    document.getElementById('phone-err').style.display = 'none';
    document.getElementById('suburb-err').style.display = 'none';

    e.preventDefault();
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }

    // Input fields
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const suburbInput = document.getElementById('suburb');

    // Sanitize input values
    const email = escapeHTML(emailInput.value.trim());
    const phone = escapeHTML(phoneInput.value.trim());
    const suburb = escapeHTML(suburbInput.value.trim());

    // Regex Checks (Data Validation Security practice)
    let isValid = true;

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        document.getElementById('email-err').style.display = 'block';
        isValid = false;
    } else {
        document.getElementById('email-err').style.display = 'none';
    }

    const phoneRegex = /^04\d{8}$/; // Simple Australian Mobile format verification
    if (!phoneRegex.test(phone)) {
        document.getElementById('phone-err').style.display = 'block';
        isValid = false;
    } else {
        document.getElementById('phone-err').style.display = 'none';
    }

    if (suburb === '') {
        document.getElementById('suburb-err').style.display = 'block';
        isValid = false;
    } else {
        document.getElementById('suburb-err').style.display = 'none';
    }

    if (!isValid) return;

    try {
        const response = await fetch('/api/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                phone: phone,
                suburb: suburb,
                cart: cart.map(item => ({
                    id: item.id,
                    qty: item.qty
                }))
            })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.error || 'Unable to complete sale.');
            return;
        }

        cart = [];
        updateCartBadge();
        renderCart();

        document.getElementById('checkout-form').reset();

        alert(`Sale Completed! Order ID: ${result.order_number}`);

    } catch (error) {
        console.error(error);
        alert('Unable to connect to the server.');
    }
}

// Render Admin Sales View
async function renderAdmin() {
    const tbody = document.getElementById('admin-sales-list');
    const emptyMsg = document.getElementById('admin-empty');

    try {
        const response = await fetch('/api/admin/sales');

        if (!response.ok) {
            alert('Unable to load sales.');
            return;
        }

        const sales = await response.json();

        let revenue = 0;
        let cost = 0;

        if (sales.length === 0) {
            tbody.innerHTML = '';
            emptyMsg.style.display = 'block';
        } else {
            emptyMsg.style.display = 'none';

            tbody.innerHTML = sales.map(s => {
                revenue += s.totalSell;
                cost += s.totalCost;

                const itemsSummary = s.items
                    .map(i => `${i.qty}x ${escapeHTML(i.title)}`)
                    .join('<br>');

                const orderDate = new Date(s.createdAt + 'Z');

                const formattedDate = orderDate.toLocaleString('en-AU', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                });

                return `
    <tr>
        <td><strong>${s.orderId}</strong></td>
        <td>${formattedDate}</td>

                        <td>
                            <div>${escapeHTML(s.email)}</div>
                            <div style="font-size: 0.75rem; color: var(--text-muted);">
                                ${escapeHTML(s.phone)} | ${escapeHTML(s.suburb)}
                            </div>
                        </td>

                        <td style="font-size: 0.85rem;">
                            ${itemsSummary}
                        </td>

                        <td>$${s.totalCost.toFixed(2)}</td>
                        <td>$${s.totalSell.toFixed(2)}</td>

                        <td style="color: var(--success); font-weight: bold;">
                            +$${s.profit.toFixed(2)}
                        </td>
                    </tr>
                `;
            }).join('');
        }

        document.getElementById('stat-count').innerText = sales.length;
        document.getElementById('stat-revenue').innerText =
            `$${revenue.toFixed(2)}`;

        document.getElementById('stat-cost').innerText =
            `$${cost.toFixed(2)}`;

        document.getElementById('stat-profit').innerText =
            `$${(revenue - cost).toFixed(2)}`;

    } catch (error) {
        console.error(error);
        alert('Unable to connect to the server.');
    }
}

// Admin Authentication
async function handleAdminLogin() {
    const passwordInput = document.getElementById('admin-password');
    const errorMsg = document.getElementById('admin-login-error');

    const password = passwordInput.value;

    errorMsg.style.display = 'none';

    try {
        const response = await fetch('/api/admin/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                password: password
            })
        });

        if (!response.ok) {
            errorMsg.style.display = 'block';
            passwordInput.value = '';
            return;
        }

        document.getElementById('admin-login').style.display = 'none';
        document.getElementById('admin-dashboard').style.display = 'block';

        passwordInput.value = '';

        await renderAdmin();

    } catch (error) {
        console.error(error);
        alert('Unable to connect to the server.');
    }
}


async function checkAdminStatus() {
    try {
        const response = await fetch('/api/admin/status');
        const data = await response.json();

        if (data.loggedIn) {
            document.getElementById('admin-login').style.display = 'none';
            document.getElementById('admin-dashboard').style.display = 'block';

            await renderAdmin();
        } else {
            document.getElementById('admin-login').style.display = 'block';
            document.getElementById('admin-dashboard').style.display = 'none';
        }

    } catch (error) {
        console.error(error);
    }
}

async function handleAdminLogout() {
    try {
        const response = await fetch('/api/admin/logout', {
            method: 'POST'
        });

        if (!response.ok) {
            alert('Unable to log out.');
            return;
        }

        document.getElementById('admin-dashboard').style.display = 'none';
        document.getElementById('admin-login').style.display = 'block';
        document.getElementById('admin-password').value = '';

    } catch (error) {
        console.error(error);
        alert('Unable to connect to the server.');
    }
}