const API_BASE = 'http://127.0.0.1:8000/api/v1';


function getToken() { return localStorage.getItem('token'); }
function setToken(token) { localStorage.setItem('token', token); }
function clearToken() { localStorage.removeItem('token'); localStorage.removeItem('role'); }
function getRole() { return localStorage.getItem('role'); }
function setRole(role) { localStorage.setItem('role', role); }

// принимает опциональный freshToken
async function apiFetch(url, method = 'GET', body = null, freshToken = null) {
    const token = freshToken || getToken(); 
    const headers = { 'Content-Type': 'application/json' }; 
    if (token) {
        headers['Authorization'] = `Bearer ${token}`; 
    }

    try {
        const response = await fetch(url, {
            method: method,
            headers: headers,
            body: body ? JSON.stringify(body) : null,
        });

        const data = await response.json();

        if (!response.ok) {
            const msg = data.detail || data.message || 'Ошибка запроса';
            displayMessage(msg, 'error', 'auth-message-center');
            
            // если ошибка авторизации то  очищаем токеен
            if (response.status === 401 || response.status === 403) {
                clearToken();
                updateUI(false); 
            }
            return null;
        }

        return data;
    } catch (e) {
        displayMessage('Ошибка сети или сервера.', 'error', 'auth-message-center');
        return null;
    }
}
function displayMessage(message, type, targetId) {
    const msgElement = document.getElementById(targetId);
    if (!msgElement) return;

    msgElement.textContent = message;
    msgElement.className = `message ${type}`;
    msgElement.style.display = 'block';
    setTimeout(() => msgElement.style.display = 'none', 5000);
}

function updateUI(isLoggedIn) {
    const role = getRole();
    const mainContent = document.getElementById('main-content');
    const authFormsCenter = document.getElementById('auth-forms-center');
    const userControls = document.getElementById('user-controls');
    mainContent.style.display = 'none';
    authFormsCenter.style.display = 'none';
    userControls.style.display = 'none';
    const addProductSection = document.getElementById('add-product-section');
    if (addProductSection) {
        addProductSection.style.display = 'none';
        const showFormBtn = document.getElementById('show-add-product-form-btn');
        if (showFormBtn) {
            showFormBtn.textContent = '➕ Добавить новый товар';
        }
    }
    if (isLoggedIn) {
        // Авторизованный пользователь 
        authFormsCenter.style.display = 'none';
        userControls.style.display = 'flex';
        mainContent.style.display = 'block';
        if (role === 'ROLE_SELLER') {
            loadSellerLK();
        } else if (role === 'ROLE_CUSTOMER') {
            loadCustomerLK();
        }

    } else {
        // неавторизованный пользователь
        authFormsCenter.style.display = 'block';
        document.getElementById('login-section').style.display = 'block';
        document.getElementById('register-section').style.display = 'none';
    }
}

function authenticatedLoad(token, role) {
    updateUI(true); 

    if (role === 'ROLE_SELLER') {
        loadSellerLK(token); // Передаем свежий токен
    } else if (role === 'ROLE_CUSTOMER') {
        loadCustomerLK(token); // Передаем свежий токен
    }
}

async function loadSellerLK(freshToken = null) {
    document.getElementById('seller-tools').style.display = 'block';
    const lkInfo = document.getElementById('lk-info');
    const lkData = document.getElementById('lk-data');
    lkData.innerHTML = '';

    const profile = await apiFetch(`${API_BASE}/auth/profile`, 'GET', null, freshToken);
    if (profile) {
        document.getElementById('user-greeting').textContent = `Продавец: ${profile.login}`;
        lkInfo.innerHTML = `<h3>Личный кабинет Продавца</h3><p>Ваша роль: ${profile.role}</p>`;
    }
    

    const products = await apiFetch(`${API_BASE}/seller/products`);
    if (products) {
        lkData.innerHTML = '<h4>Ваши товары:</h4>';
        products.forEach(p => {
            const card = document.createElement('div');
            card.className = 'product-card';
            card.innerHTML = `<h4>${p.name} (ID: ${p.id})</h4><p>Цена: ${p.price} руб.</p><p>${p.description}</p>`;
            lkData.appendChild(card);
        });
    }
}
async function loadCustomerLK(freshToken = null) {
    document.getElementById('seller-tools').style.display = 'none';
    const lkInfo = document.getElementById('lk-info');
    const lkData = document.getElementById('lk-data');
    lkData.innerHTML = '';

    
    const profile = await apiFetch(`${API_BASE}/auth/profile`, 'GET', null, freshToken);
    if (profile) {
        document.getElementById('user-greeting').textContent = `Покупатель: ${profile.login}`;
        lkInfo.innerHTML = `<h3>Каталог товаров</h3><p>Ваша роль: ${profile.role}</p>`;
    }
    
    const products = await apiFetch(`${API_BASE}/products`);
    if (products) {
        products.forEach(p => {
            const card = document.createElement('div');
            card.className = 'product-card';
            card.innerHTML = `
                <h4>${p.name}</h4>
                <p>Цена: ${p.price} руб.</p>
                <p>${p.description}</p>
                <button class="secondary-btn" onclick="alert('Функционал корзины не реализован в рамках ЛР.')">Купить</button>
            `;
            lkData.appendChild(card);
        });
    }
}


// обрабы форм

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const login = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const data = await apiFetch(`${API_BASE}/auth/login`, 'POST', { login, password });
    if (data) {
        setToken(data.token);
        setRole(data.role);
        authenticatedLoad(data.token, data.role);
        displayMessage('Вход успешен!', 'success', 'auth-message-center');
    }
});

// рега
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const login = document.getElementById('reg-login').value;
    const password = document.getElementById('reg-password').value;
    const name = document.getElementById('reg-name').value;
    const email = document.getElementById('reg-email').value;
    const role = document.getElementById('reg-role').value;

    const data = await apiFetch(`${API_BASE}/auth/register`, 'POST', { login, password, name, email, role });
    if (data) {
        setToken(data.token);
        setRole(data.role);
        authenticatedLoad(data.token, data.role);
        displayMessage('Регистрация успешна! Вы авторизованы.', 'success', 'auth-message-center');
    }
});

document.getElementById('add-product-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('prod-name').value;
    const price = parseFloat(document.getElementById('prod-price').value);
    const description = document.getElementById('prod-desc').value;

    const product_data = {
        name,
        price,
        description,
        seller_id: 0, 
        id: 0, 
    };

    const data = await apiFetch(`${API_BASE}/seller/products`, 'POST', product_data);
    if (data) {
        displayMessage(`Товар "${data.name}" добавлен!`, 'success', 'auth-message-center');
        loadSellerLK(); // Обновляем список
        document.getElementById('add-product-section').style.display = 'none';
        document.getElementById('show-add-product-form-btn').textContent = '➕ Добавить новый товар';
    }
});


document.getElementById('logout-btn').addEventListener('click', () => {
    clearToken();
    updateUI(false);
    displayMessage('Вы успешно вышли.', 'success', 'auth-message-center');
});


document.getElementById('show-register-btn').addEventListener('click', () => {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'block';
    document.getElementById('auth-message-center').style.display = 'none';
});

document.getElementById('show-login-btn').addEventListener('click', () => {
    document.getElementById('register-section').style.display = 'none';
    document.getElementById('login-section').style.display = 'block';
    document.getElementById('auth-message-center').style.display = 'none';
});

document.addEventListener('DOMContentLoaded', () => {
    const showFormBtn = document.getElementById('show-add-product-form-btn');
    const formSection = document.getElementById('add-product-section');

    if (showFormBtn && formSection) {
        showFormBtn.addEventListener('click', () => {
            if (formSection.style.display === 'none' || formSection.style.display === '') {
                formSection.style.display = 'block';
                showFormBtn.textContent = '✖️ Скрыть форму';
            } else {
                formSection.style.display = 'none';
                showFormBtn.textContent = '➕ Добавить новый товар';
            }
        });
    }
    updateUI(!!getToken());
});