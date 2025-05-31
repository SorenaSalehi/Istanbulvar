import { getCSRFToken } from "./helpers";

(function () {
    /**
     * Expose a global function to add an item to the wishlist.
     * @param {number} productId
     */
    window.addToWishlist = function (productId) {
        fetch(window.addToWishlistApiUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ product_id: productId }),
        })
            .then((response) => response.json())
            .then((data) => {
                document
                    .querySelectorAll(`button.wishlist-toggle-${productId}`)
                    .forEach(function (btn) {
                        btn.setAttribute(
                            "onclick",
                            `removeFromWishlist(${productId})`
                        );
                        const icon = btn.querySelector("i");
                        if (icon) {
                            icon.className =
                                "ci-heart-filled fs-base animate-target";
                        }
                    });

                document
                    .querySelectorAll(".wishlistCount")
                    .forEach(function (el) {
                        el.innerHTML = data.wishlist_count;
                    });

                Swal.fire({
                    title: data.title,
                    text: data.message,
                    icon: data.icon,
                    confirmButtonText: "پایان",
                });

                fetch(window.wishlistPartialUrl, {
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    },
                })
                    .then((response) => response.text())
                    .then((htmlSnippet) => {
                        document
                            .querySelectorAll(".wishlistContainer")
                            .forEach(function (el) {
                                el.innerHTML = htmlSnippet;
                            });
                    });
            })
            .catch((error) => {
                console.error(error);
                Swal.fire({
                    title: "مشکل",
                    text: "یک مشکلی پیش آمده!",
                    icon: "error",
                    confirmButtonText: "تایید",
                });
            });
    };

    window.removeFromWishlist = function (productId) {
        fetch(window.removeFromWishlistApiUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ product_id: productId }),
        })
            .then((response) => response.json())
            .then((data) => {
                document
                    .querySelectorAll(`button.wishlist-toggle-${productId}`)
                    .forEach(function (btn) {
                        btn.setAttribute(
                            "onclick",
                            `addToWishlist(${productId})`
                        );
                        const icon = btn.querySelector("i");
                        if (icon) {
                            icon.className = "ci-heart fs-base animate-target";
                        }
                    });

                document
                    .querySelectorAll(".wishlistCount")
                    .forEach(function (el) {
                        el.innerHTML = data.wishlist_count;
                    });
                Swal.fire({
                    title: data.title,
                    text: data.message,
                    icon: data.icon,
                    confirmButtonText: "تایید",
                });

                fetch(window.wishlistPartialUrl, {
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    },
                })
                    .then((response) => response.text())
                    .then((htmlSnippet) => {
                        document
                            .querySelectorAll(".wishlistContainer")
                            .forEach(function (el) {
                                el.innerHTML = htmlSnippet;
                            });
                    });
            })
            .catch((error) => {
                console.error(error);
                Swal.fire({
                    title: "ارور",
                    text: "یک خطای غیر منتظره پیش آمده.",
                    icon: "error",
                    confirmButtonText: "تایید",
                });
            });
    };
})();
