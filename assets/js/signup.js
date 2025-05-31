import { getCSRFToken } from "./helpers";

(function () {
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
                    "X-CSRFToken": getCSRFToken,
                },
                body: JSON.stringify({ email: email }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        messageBox.innerHTML =
                            "<div class='alert alert-success'>تبریک میگم. به خوانواده استانبول وار خوش اومدین</div>";
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
})();
