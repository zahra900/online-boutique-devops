
let cartCount = 0;

async function displayProducts() {
    const productsContainer = document.getElementById("products");

    try {
        const response = await fetch("/api/products");

        if (!response.ok) {
            throw new Error("Failed to fetch products");
        }

        const products = await response.json();

        productsContainer.innerHTML = products.map(product => `
            <article class="product-card">
                <img src="${product.image}" alt="${product.name}">

                <div class="product-info">
                    <h3>${product.name}</h3>
                    <p class="price">$${product.price.toFixed(2)}</p>
                    <button onclick="addToCart(${product.id})">
                        Add to cart
                    </button>
                </div>
            </article>
        `).join("");

    } catch (error) {
        console.error(error);
        productsContainer.innerHTML =
            "<p>Unable to load products. Please try again later.</p>";
    }
}

function addToCart(productId) {
    cartCount++;
    document.getElementById("cart-count").textContent = cartCount;
}

// Initialize when running in the browser.
if (typeof document !== "undefined") {
    document.addEventListener("DOMContentLoaded", displayProducts);
}

// Export functions for unit tests.
if (typeof module !== "undefined" && module.exports) {
    module.exports = {
        displayProducts,
        addToCart
    };
}
