(function () {
    document.addEventListener("DOMContentLoaded", function () {
        let checkoutButton = document.getElementById("checkoutButton");
        if (!checkoutButton) return;

        checkoutButton.addEventListener("click", function (event) {
            event.preventDefault();

            let kvkkCheckbox = document.getElementById("kvkkAgreement");
            if (!kvkkCheckbox || !kvkkCheckbox.checked) {
                Swal.fire({
                    text: "برای ادامه پرداخت، باید قرارداد فروش از راه دور و خط مشی رازداری را بپذیرید.",
                    icon: "info",
                    confirmButtonText: "تایید",
                });
                return;
            }

            let form = document.getElementById("checkoutForm");
            let formData = new FormData(form);

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
                        let modalBody =
                            document.getElementById("paymentModalBody");
                        modalBody.innerHTML = `
                    <script src="https://www.paytr.com/js/iframeResizer.min.js"><\/script>
                    <iframe src="https://www.paytr.com/odeme/guvenli/${data.token}" id="paytriframe" frameborder="0" scrolling="yes" style="width: 100%; height: 600px;"></iframe>
                    <script>iFrameResize({}, '#paytriframe');<\/script>
                    `;
                        let paymentModal = new bootstrap.Modal(
                            document.getElementById("paymentModal")
                        );
                        paymentModal.show();
                    } else if (data.error) {
                        Swal.fire({
                            text: data.error,
                            icon: "error",
                            confirmButtonText: "تایید",
                        });
                    } else if (data.message) {
                        Swal.fire({
                            text: data.message,
                            icon: "success",
                            confirmButtonText: "تایید",
                        });
                    }
                });
        });
    });
})();
