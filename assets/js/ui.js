import { getCSRFToken } from "./helpers";

(function () {
    document.addEventListener("DOMContentLoaded", function () {
        const loadMoreBtn = document.getElementById("load-more-btn");
        if (!loadMoreBtn) return;

        let loading = false;
        loadMoreBtn.addEventListener("click", function () {
            if (loading) return;
            loading = true;

            const nextPage = loadMoreBtn.getAttribute("data-next-page");

            const categoryFilter =
                document.getElementById("categoryFilter").value || "";

            fetch(
                `${
                    window.infiniteScrollUrl
                }?page=${nextPage}&category=${encodeURIComponent(
                    categoryFilter
                )}`,
                {
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": getCSRFToken(),
                    },
                }
            )
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Failed to load more products.");
                    }
                    return response.text();
                })
                .then((html) => {
                    if (!html.trim()) {
                        loadMoreBtn.style.display = "none";
                        return;
                    }

                    const productListDiv =
                        document.getElementById("productList");
                    productListDiv.insertAdjacentHTML("beforeend", html);

                    loadMoreBtn.setAttribute(
                        "data-next-page",
                        parseInt(nextPage) + 1
                    );
                })
                .catch((err) => console.error(err))
                .finally(() => {
                    loading = false;
                });
        });
    });

    $(document).on("focus", ".phone-mask", function () {
        if (!$(this).data("inputmask")) {
            Inputmask("(9##) ### - ####", {
                placeholder: "_",
                showMaskOnHover: true,
                showMaskOnFocus: true,
            }).mask(this);
        }
    });

    document.addEventListener("DOMContentLoaded", function () {
        const form = document.getElementById("variantAttributeForm");
        if (form) {
            const radioInputs = form.querySelectorAll('input[type="radio"]');
            radioInputs.forEach(function (input) {
                input.addEventListener("change", function () {
                    form.submit();
                });
            });
        }
    });

    window.addEventListener("load", function () {
        const form = document.getElementById("filterForm");
        if (!form) return;

        // checkbox ve number input'lar
        form.querySelectorAll('input[type="checkbox"]').forEach((input) => {
            input.addEventListener("change", () => form.submit());
            input.addEventListener("input", () => form.submit());
        });
    });
})();
