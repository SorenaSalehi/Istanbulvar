import { getCSRFToken } from "./helpers";

(function () {
    /**
     * Expose a global function to add an item to the cart.
     *
     * @param {number} productId - The product's ID from your Django model
     * @param {number} count     - The quantity to add
     */
    window.addToCart = function (productId, count) {
        fetch(window.addToCartApiUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ product_id: productId, count: count }),
        })
            .then((response) => response.json())
            .then((data) => {
                Swal.fire({
                    title: data.title,
                    text: data.message,
                    icon: data.icon,
                    confirmButtonText: "تایید",
                });
                document.querySelectorAll(".cartCount").forEach(function (el) {
                    el.innerHTML = data.cart_count;
                });
                return fetch(window.cartPartial, {
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    },
                });
            })
            .then((response) => (response ? response.text() : null))
            .then((htmlSnippet) => {
                if (htmlSnippet) {
                    document
                        .querySelectorAll(".cartContainer")
                        .forEach(function (el) {
                            el.innerHTML = htmlSnippet;
                        });
                }
            })
            .catch((error) => {
                console.error(error);
                Swal.fire({
                    title: "Error",
                    text: "An unexpected error occurred.",
                    icon: "error",
                    confirmButtonText: "OK",
                });
            });
    };

    window.removeFromCart = function (productId, count) {
        fetch(window.removeFromCartApiUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ product_id: productId, count: count }),
        })
            .then((response) => response.json())
            .then((data) => {
                Swal.fire({
                    title: data.title,
                    text: data.message,
                    icon: data.icon,
                    confirmButtonText: "تایید",
                });
                document.querySelectorAll(".cartCount").forEach(function (el) {
                    el.innerHTML = data.cart_count;
                });
                return fetch(window.cartPartial, {
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    },
                });
            })
            .then((response) => (response ? response.text() : null))
            .then((htmlSnippet) => {
                if (htmlSnippet) {
                    document
                        .querySelectorAll(".cartContainer")
                        .forEach(function (el) {
                            el.innerHTML = htmlSnippet;
                        });
                }
            })
            .catch((error) => {
                console.error(error);
                Swal.fire({
                    title: "Error",
                    text: "An unexpected error occurred.",
                    icon: "error",
                    confirmButtonText: "OK",
                });
            });
    };
})();
