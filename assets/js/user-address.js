import { getCSRFToken } from "./helpers";

(function () {
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
                    confirmButtonText: "تایید",
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
                        confirmButtonText: "تایید",
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
})();
