"use strict";

(function () {
    /**
     * Helper function to get the CSRF token from cookies (required by Django).
     */
    function getCSRFToken() {
        let cookieValue = null;
        const name = "csrftoken";
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }
        return cookieValue;
    }

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
                    confirmButtonText: "Tamam",
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
                    title: "Hata",
                    text: "Beklenmeyen bir hata oluştu.",
                    icon: "error",
                    confirmButtonText: "Tamam",
                });
            });
    };

    /**
     * Expose a global function to remove an item from the wishlist.
     * @param {number} productId
     */
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
                    confirmButtonText: "Tamam",
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
                    title: "Hata",
                    text: "Beklenmeyen bir hata oluştu.",
                    icon: "error",
                    confirmButtonText: "Tamam",
                });
            });
    };

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
                    confirmButtonText: "Tamam",
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

    /**
     * Expose a global function to remove an item from the cart.
     *
     * @param {number} productId - The product's ID from your Django model
     * @param {number} count     - The quantity to remove
     */
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
                    confirmButtonText: "Tamam",
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

    window.loadOrderDetails = function loadOrderDetails(orderId) {
        const url = window.orderDetail;

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ order_id: orderId }),
        })
            .then((response) => {
                if (!response.ok)
                    throw new Error("Network response was not OK");
                return response.text();
            })
            .then((html) => {
                const container = document.getElementById("orderDetails");
                container.innerHTML = html;

                const bsOffcanvas =
                    bootstrap.Offcanvas.getOrCreateInstance(container);
                bsOffcanvas.show();
            })
            .catch((err) => {
                console.error("Failed to load order detail:", err);
            });
    };

    // When the auth modal is shown, load the login form
    $("#loginModel").on("show.bs.modal", function (event) {
        const button = $(event.relatedTarget);
        const redirectUrl = button.data("redirect-url");
        let requestData = {};

        if (redirectUrl) {
            requestData.next = redirectUrl;
        }

        $.ajax({
            url: "/login/",
            method: "GET",
            data: requestData,
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
            success: function (response) {
                if (response.status === "redirect") {
                    window.location.href = response.redirect_url;
                    return;
                }
                $("#authenticateContent").html(response);
            },
            error: function () {
                $("#authenticateContent").html(
                    "<p>An error occurred while loading the login form. Please try again later.</p>"
                );
            },
        });
    });

    // When the auth modal is shown, load the address form
    $("#addressModel").on("show.bs.modal", function (event) {
        const button = $(event.relatedTarget);
        const redirectUrl = button.data("redirect-url");
        let requestData = {};

        if (redirectUrl) {
            requestData.next = redirectUrl;
        }

        $.ajax({
            url: "/add_new_address/",
            method: "GET",
            data: requestData,
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
            success: function (response) {
                if (response.status === "redirect") {
                    window.location.href = response.redirect_url;
                    return;
                }
                $("#addressModelContent").html(response);
            },
            error: function () {
                $("#addressModelContent").html(
                    "<p>An error occurred while loading the login form. Please try again later.</p>"
                );
            },
        });
    });

    // Handle login by code form
    $(document).on("submit", "#loginByCodeForm", function (e) {
        e.preventDefault();

        $.ajax({
            url: "/login_by_code/",
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
            data: $(this).serialize(),
            success: function (response) {
                if (response.status === "redirect") {
                    window.location.href = response.redirect_url;
                    return;
                }
                $("#authenticateContent").html(response);
            },
            error: function () {
                $("#authenticateContent").html(
                    "<p>An error occurred while processing your request. Please try again later.</p>"
                );
            },
        });
    });

    // Handle verification code form
    $(document).on("submit", "#verifyCodeForm", function (e) {
        e.preventDefault();

        $.ajax({
            url: "/verify_code/",
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
            data: $(this).serialize(),
            success: function (response) {
                if (response.status === "redirect") {
                    console.log("redirect_url");
                    console.log(response.redirect_url);
                    window.location.href = response.redirect_url;
                    return;
                }
                $("#authenticateContent").html(response);
            },
            error: function () {
                $("#authenticateContent").html(
                    "<p>An error occurred while processing your request. Please try again later.</p>"
                );
            },
        });
    });

    // Handle normal login form
    $(document).on("submit", "#loginForm", function (e) {
        e.preventDefault();

        $.ajax({
            url: "/login/",
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
            data: $(this).serialize(),
            success: function (response) {
                if (response.status === "redirect") {
                    window.location.href = response.redirect_url;
                    return;
                }
                $("#authenticateContent").html(response);
            },
            error: function () {
                $("#authenticateContent").html(
                    "<p>An error occurred while processing your request. Please try again later.</p>"
                );
            },
        });
    });

    //     در این نسخه داخل همان فرمِ ورود/ثبت‌نام، دو حالت تعریف شده:

    // وارد کردن شماره

    // وارد کردن کد

    // و بعد از ارسال شماره به سرور، با جاوااسکریپت فقط متن عنوان و فیلدها عوض می‌شود:

    $("#authForm").on("submit", function (e) {
        e.preventDefault();
        const isCodeStage = !$("#codeGroup").hasClass("d-none");

        if (!isCodeStage) {
            // مرحله ارسال شماره
            $.ajax({
                url: '{% url "signup" %}', // یا مسیر مناسب پروژه‌ات
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() },
                data: {
                    phone_number: $("#phone_number").val(),
                    next: $("input[name=next]").val(),
                },
                success: function (resp) {
                    if (resp.status === "sms_sent") {
                        // تغییر عنوان
                        $("#stepTitle").text("کد تایید را وارد کنید :");
                        // نمایش فیلد کد و مخفی کردن فیلد شماره
                        $("#phoneGroup").addClass("d-none");
                        $("#codeGroup").removeClass("d-none");
                        // تغییر متن دکمه
                        $("#submitButton").text("تایید کد");
                    } else if (resp.status === "error") {
                        alert("فرمت شماره اشتباه است یا مشکلی پیش آمده.");
                    } else if (resp.status === "redirect") {
                        window.location.href = resp.redirect_url;
                    }
                },
                error: function () {
                    alert("خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.");
                },
            });
        } else {
            // مرحله تایید کد
            $.ajax({
                url: '{% url "verifyCode" %}', // یا مسیر مناسب پروژه‌ات
                method: "POST",
                headers: { "X-CSRFToken": getCSRFToken() },
                data: {
                    phone_number: $("#phone_number").val(),
                    code: $("#verify_code").val(),
                    next: $("input[name=next]").val(),
                },
                success: function (resp) {
                    if (resp.status === "verified") {
                        window.location.href = resp.redirect_url;
                    } else {
                        alert("کد اشتباه یا منقضی شده است.");
                    }
                },
                error: function () {
                    alert("خطا در تأیید کد. دوباره تلاش کنید.");
                },
            });
        }
    });

    // Handle signup form
    $(document).on("submit", "#signupForm", function (e) {
        e.preventDefault();

        $.ajax({
            url: "/signup/",
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
            data: $(this).serialize(),
            success: function (response) {
                if (response.status === "redirect") {
                    window.location.href = response.redirect_url;
                    return;
                }
                $("#authenticateContent").html(response);
            },
            error: function () {
                $("#authenticateContent").html(
                    "<p>An error occurred while processing your request. Please try again later.</p>"
                );
            },
        });
    });

    // Switch to "login by code" form
    $(document).on("click", "#loginByCodeLink", function (e) {
        e.preventDefault();
        const redirectUrl = $(this).data("redirect-url");
        let requestData = {};

        if (redirectUrl) {
            requestData.next = redirectUrl;
        }

        $.ajax({
            url: "/login_by_code/",
            method: "GET",
            data: requestData,
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
            success: function (response) {
                if (response.status === "redirect") {
                    window.location.href = response.redirect_url;
                    return;
                }
                $("#authenticateContent").html(response);
            },
            error: function () {
                $("#authenticateContent").html(
                    "<p>An error occurred while loading form. Please try again later.</p>"
                );
            },
        });
    });

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
        var checkoutButton = document.getElementById("checkoutButton");
        if (!checkoutButton) return;

        checkoutButton.addEventListener("click", function (event) {
            event.preventDefault();

            var kvkkCheckbox = document.getElementById("kvkkAgreement");
            if (!kvkkCheckbox || !kvkkCheckbox.checked) {
                Swal.fire({
                    text: "Ödemeye devam etmek için Mesafeli Satış Sözleşmesi'ni ve Gizlilik politikasini onaylamanız gerekir.",
                    icon: "info",
                    confirmButtonText: "Tamam",
                });
                return;
            }

            var form = document.getElementById("checkoutForm");
            var formData = new FormData(form);

            fetch(window.checkOut, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.token) {
                        var modalBody =
                            document.getElementById("paymentModalBody");
                        modalBody.innerHTML = `
                    <script src="https://www.paytr.com/js/iframeResizer.min.js"><\/script>
                    <iframe src="https://www.paytr.com/odeme/guvenli/${data.token}" id="paytriframe" frameborder="0" scrolling="yes" style="width: 100%; height: 600px;"></iframe>
                    <script>iFrameResize({}, '#paytriframe');<\/script>
                    `;
                        var paymentModal = new bootstrap.Modal(
                            document.getElementById("paymentModal")
                        );
                        paymentModal.show();
                    } else if (data.error) {
                        Swal.fire({
                            text: data.error,
                            icon: "error",
                            confirmButtonText: "Tamam",
                        });
                    } else if (data.message) {
                        Swal.fire({
                            text: data.message,
                            icon: "success",
                            confirmButtonText: "Tamam",
                        });
                    }
                });
        });
    });

    function setCurrentAddress(addressId) {
        fetch(window.setCurrentAddress, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ selected_address: addressId }),
        })
            .then((response) => response.json())
            .then((data) => {
                Swal.fire({
                    title: data.title,
                    text: data.message,
                    icon: data.icon,
                    confirmButtonText: "Tamam",
                });
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
    }

    document
        .querySelectorAll('input[name="selected_address"]')
        .forEach(function (input) {
            input.addEventListener("change", function () {
                const addressId = this.value;
                setCurrentAddress(addressId);
            });
        });

    window.deleteAddressFunc = function (addressId) {
        fetch(window.deleteAddress, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ address_id: addressId }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "success") {
                    Swal.fire({
                        title: data.title,
                        text: data.message,
                        icon: data.icon,
                        confirmButtonText: "Tamam",
                    });
                    document.getElementById("address").innerHTML =
                        data.updated_html;
                } else {
                    Swal.fire({
                        title: data.title,
                        text: data.message,
                        icon: data.icon,
                        confirmButtonText: "OK",
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

    document
        .getElementById("newsletterForm")
        .addEventListener("submit", function (e) {
            e.preventDefault();

            const email = document.getElementById("newsletterEmail").value;
            const messageBox = document.getElementById("newsletterMessage");

            fetch(window.newsletterAdd, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}",
                },
                body: JSON.stringify({ email: email }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        messageBox.innerHTML =
                            "<div class='alert alert-success'>Teşekkürler. kaydınız başarılı</div>";
                    } else {
                        messageBox.innerHTML =
                            "<div class='alert alert-danger'>" +
                            data.message +
                            "</div>";
                    }
                })
                .catch((error) => {
                    messageBox.innerHTML =
                        "<div class='alert alert-danger'>bir hata oluştu!</div>";
                });
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
