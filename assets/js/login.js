import { getCSRFToken } from "./helpers";

(function () {
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
})();
