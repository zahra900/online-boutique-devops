
const { displayProducts, addToCart, resetCart } = require("../public/app");

describe("Frontend server functions", () => {
    let productsContainer;
    let cartCountElement;
    let fetchMock;

    beforeEach(() => {
        document.body.innerHTML = `
            <div id="products"></div>
            <span id="cart-count">0</span>
        `;

        productsContainer = document.getElementById("products");
        cartCountElement = document.getElementById("cart-count");

        fetchMock = jest.fn();
        global.fetch = fetchMock;

        resetCart();
        jest.clearAllMocks();
    });

    afterEach(() => {
        jest.restoreAllMocks();
    });

    describe("displayProducts", () => {
        test("fetches and displays products successfully", async () => {
            const products = [
                {
                    id: 1,
                    name: "Headphones",
                    price: 59.99,
                    image: "/images/headphones.jpg"
                },
                {
                    id: 2,
                    name: "Keyboard",
                    price: 89.50,
                    image: "/images/keyboard.jpg"
                }
            ];

            fetchMock.mockResolvedValue({
                ok: true,
                json: jest.fn().mockResolvedValue(products)
            });

            await displayProducts();

            expect(fetchMock).toHaveBeenCalledWith("/api/products");
            expect(productsContainer.innerHTML).toContain("Headphones");
            expect(productsContainer.innerHTML).toContain("Keyboard");
            expect(productsContainer.innerHTML).toContain("$59.99");
            expect(productsContainer.innerHTML).toContain("$89.50");
            expect(
                productsContainer.querySelectorAll(".product-card")
            ).toHaveLength(2);
        });

        test("displays an error message when the API returns an error", async () => {
            fetchMock.mockResolvedValue({
                ok: false
            });

            jest.spyOn(console, "error").mockImplementation(() => {});

            await displayProducts();

            expect(productsContainer.textContent).toContain(
                "Unable to load products. Please try again later."
            );
        });

        test("displays an error message when fetch rejects", async () => {
            fetchMock.mockRejectedValue(new Error("Network error"));

            jest.spyOn(console, "error").mockImplementation(() => {});

            await displayProducts();

            expect(productsContainer.textContent).toContain(
                "Unable to load products. Please try again later."
            );
        });
    });

    describe("addToCart", () => {
        test("increments the cart count", () => {
            addToCart(1);

            expect(cartCountElement.textContent).toBe("1");
        });

        test("increments the cart count for multiple products", () => {
            addToCart(1);
            addToCart(2);
            addToCart(3);

            expect(cartCountElement.textContent).toBe("3");
        });
    });
});