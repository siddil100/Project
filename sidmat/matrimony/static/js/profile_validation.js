function setupFormValidation(formId) {
    const form = document.querySelector(`#${formId}`);

    form.addEventListener("submit", function (event) {
        let hasError = false; // Flag to track if any errors occurred

        const nameField = document.querySelector(`#${formId} #id_name`);
        const genderField = document.querySelector(`#${formId} #id_gender`);
        const occupationField = document.querySelector(`#${formId} #id_occupation`);
        const emailField = document.querySelector(`#${formId} #id_email`);
        const religionField = document.querySelector(`#${formId} #id_religion`);
        const sectField = document.querySelector(`#${formId} #id_sect`);

        // Clear previous error messages
        clearErrorMessages();

        // Validate name (no white spaces allowed, only alphabets)
        const nameValue = nameField.value.trim();
        if (nameValue === "") {
            displayErrorMessage(nameField, "Name is required.");
            hasError = true;
        } else if (!/^[a-zA-Z]+$/.test(nameValue)) {
            displayErrorMessage(nameField, "Name should contain only alphabets.");
            hasError = true;
        } else if (/^\s|\s$/.test(nameField.value)) {
            displayErrorMessage(nameField, "Name should not start or end with spaces.");
            hasError = true;
        }

        // Validate gender (must be selected)
        const genderValue = genderField.value;
        if (genderValue === "") {
            displayErrorMessage(genderField, "Gender must be selected.");
            hasError = true;
        }

        // Validate occupation (alphabets only and below 30 characters)
        const occupationValue = occupationField.value.trim();
        if (!/^[a-zA-Z\s]*$/.test(occupationValue) || occupationValue.length > 30) {
            displayErrorMessage(occupationField, "Occupation should contain alphabets only and be below 30 characters.");
            hasError = true;
        }

        // Validate email format
        const emailValue = emailField.value.trim();
        if (!isValidEmail(emailValue)) {
            displayErrorMessage(emailField, "Invalid email format.");
            hasError = true;
        }

        // Validate religion (must be selected)
        const religionValue = religionField.value;
        if (religionValue === "") {
            displayErrorMessage(religionField, "Religion must be selected.");
            hasError = true;
        }

        // Validate sect (must be selected)
        const sectValue = sectField.value;
        if (sectValue === "") {
            displayErrorMessage(sectField, "Sect must be selected.");
            hasError = true;
        }

        // Prevent form submission if there are errors
        if (hasError) {
            event.preventDefault();
        }
    });

    function isValidEmail(email) {
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        return emailPattern.test(email);
    }

    function displayErrorMessage(field, message) {
        const errorElement = document.createElement("p");
        errorElement.className = "error-message";
        errorElement.textContent = message;
        field.parentElement.appendChild(errorElement);
    }

    function clearErrorMessages() {
        const errorMessages = document.querySelectorAll(".error-message");
        errorMessages.forEach(function (errorMessage) {
            errorMessage.remove();
        });
    }
}

// Call the setupFormValidation function with the form ID "newpro"
document.addEventListener("DOMContentLoaded", function () {
    setupFormValidation("newpro");
});
