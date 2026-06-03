
// Password visibility toggles
function initPasswordToggles() {
    const toggles = [
        { buttonId: "toggle-password", inputId: "password" },
        { buttonId: "toggle-confirm-password", inputId: "confirm_password" },
    ];

    toggles.forEach(({ buttonId, inputId }) => {
        const button = document.getElementById(buttonId);
        const input = document.getElementById(inputId);
        if (button && input) {
            button.addEventListener("click", () => {
                input.type = input.type === "password" ? "text" : "password";
            });
        }
    });
}

// Show/hide user type specific fields on registration
function initUserTypeToggle() {
    const userTypeSelect = document.getElementById("user_type");
    if (!userTypeSelect) return;

    const candidateFields = document.getElementById("candidate-fields");
    const employerFields = document.getElementById("employer-fields");

    userTypeSelect.addEventListener("change", () => {
        const selected = userTypeSelect.value;
        candidateFields.style.display = selected === "candidate" ? "block" : "none";
        employerFields.style.display = selected === "employer" ? "block" : "none";

        setFieldsRequired(candidateFields, selected === "candidate");
        setFieldsRequired(employerFields, selected === "employer");
    });
}

// Set required attribute on all inputs and selects within a container
function setFieldsRequired(container, isRequired) {
    container.querySelectorAll("input, select").forEach(field => {
        if (isRequired) {
            field.setAttribute("required", "");
        } else {
            field.removeAttribute("required");
        }
    });
}

function showFormError(message) {
    const existing = document.getElementById("form-popup");
    if (existing) existing.remove();

    const popup = document.createElement("div");
    popup.id = "form-popup";
    popup.className = "form-popup";

    const text = document.createElement("p");
    text.textContent = message;

    const closeButton = document.createElement("button");
    closeButton.textContent = "✕";
    closeButton.className = "form-popup-close";
    closeButton.addEventListener("click", () => popup.remove());

    popup.appendChild(text);
    popup.appendChild(closeButton);
    document.body.appendChild(popup);
}

// Client side password match validation on registration
function initPasswordMatchValidation() {
    const form = document.querySelector("form");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm_password");
    if (!form || !password || !confirmPassword) return;

    form.addEventListener("submit", (e) => {
        if (password.value !== confirmPassword.value) {
            e.preventDefault();
            showFormError("Passwords do not match.");
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initPasswordToggles();
    initUserTypeToggle();
    initPasswordMatchValidation();
    initCandidateProfileModal();
    initEmployerDashboardModal();
    initJobApplicationModal();
    initRemoveApplicationModal();
});

function initCandidateProfileModal() {
    const modal = document.getElementById("candidate-edit-modal");
    if (!modal) return;

    const openButton = document.querySelector('[data-modal-open="candidate-edit-modal"]');
    const closeButtons = modal.querySelectorAll("[data-modal-close]");

    const openModal = () => {
        modal.hidden = false;
        modal.setAttribute("aria-hidden", "false");
        document.body.classList.add("modal-open");
    };

    const closeModal = () => {
        modal.hidden = true;
        modal.setAttribute("aria-hidden", "true");
        document.body.classList.remove("modal-open");
    };

    if (openButton) {
        openButton.addEventListener("click", openModal);
    }

    closeButtons.forEach((button) => {
        button.addEventListener("click", closeModal);
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !modal.hidden) {
            closeModal();
        }
    });
}

function initEmployerDashboardModal() {
    const modal = document.getElementById("employer-edit-modal");
    if (!modal) return;

    const openButton = document.querySelector('[data-modal-open="employer-edit-modal"]');
    const closeButtons = modal.querySelectorAll("[data-modal-close]");

    const openModal = () => {
        modal.hidden = false;
        modal.setAttribute("aria-hidden", "false");
        document.body.classList.add("modal-open");
    };

    const closeModal = () => {
        modal.hidden = true;
        modal.setAttribute("aria-hidden", "true");
        document.body.classList.remove("modal-open");
    };

    if (openButton) {
        openButton.addEventListener("click", openModal);
    }

    closeButtons.forEach((button) => {
        button.addEventListener("click", closeModal);
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !modal.hidden) {
            closeModal();
        }
    });
}

function initJobApplicationModal() {
    const modal = document.getElementById("job-application-modal");
    if (!modal) return;

    const openButton = document.querySelector('[data-modal-open="job-application-modal"]');
    const closeButtons = modal.querySelectorAll("[data-modal-close]");

    const openModal = () => {
        modal.hidden = false;
        modal.setAttribute("aria-hidden", "false");
        document.body.classList.add("modal-open");
    };

    const closeModal = () => {
        modal.hidden = true;
        modal.setAttribute("aria-hidden", "true");
        document.body.classList.remove("modal-open");
    };

    if (openButton) {
        openButton.addEventListener("click", openModal);
    }

    closeButtons.forEach((button) => {
        button.addEventListener("click", closeModal);
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !modal.hidden) {
            closeModal();
        }
    });
}

let pendingRemoveApplicationForm = null;

function initRemoveApplicationModal() {
    const modal = document.getElementById("remove-application-modal");
    if (!modal) return;

    const closeButtons = modal.querySelectorAll("[data-remove-application-close]");
    const confirmButton = document.getElementById("remove-application-confirm-btn");

    const closeModal = () => {
        pendingRemoveApplicationForm = null;
        modal.hidden = true;
        modal.setAttribute("aria-hidden", "true");
        document.body.classList.remove("modal-open");
    };

    closeButtons.forEach((button) => {
        button.addEventListener("click", closeModal);
    });

    if (confirmButton) {
        confirmButton.addEventListener("click", () => {
            if (pendingRemoveApplicationForm) {
                pendingRemoveApplicationForm.submit();
            }
        });
    }

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !modal.hidden) {
            closeModal();
        }
    });
}

function openRemoveApplicationModal(button) {
    const modal = document.getElementById("remove-application-modal");
    if (!modal) return;

    pendingRemoveApplicationForm = button.closest(".remove-application-form");
    modal.hidden = false;
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("modal-open");
}