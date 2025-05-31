import { getCSRFToken } from "./helpers";

(function () {
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
})();
