import { getCSRFToken } from "./helpers";

(function () {
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
})();
