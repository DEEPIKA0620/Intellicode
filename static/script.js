// ===============================
// IntelliCode UI Enhancements
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    // -----------------------------
    // Smooth scroll to results
    // -----------------------------
    const resultCard =
        document.querySelector(".result-card") ||
        document.querySelector(".explanation-card");

    if (resultCard) {
        resultCard.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }

    // -----------------------------
    // Disable button while submitting
    // -----------------------------
    document.querySelectorAll("form").forEach(form => {

        form.addEventListener("submit", function () {

            const btn = form.querySelector(
                "button[type='submit'], input[type='submit']"
            );

            if (btn) {
                btn.disabled = true;

                if (btn.tagName === "BUTTON") {
                    btn.dataset.original = btn.innerHTML;
                    btn.innerHTML = "⏳ Processing...";
                } else {
                    btn.dataset.original = btn.value;
                    btn.value = "Processing...";
                }
            }

        });

    });

    // -----------------------------
    // Show selected filename
    // -----------------------------
    document.querySelectorAll("input[type='file']").forEach(input => {

        input.addEventListener("change", function () {

            if (this.files.length === 0) return;

            let filename = this.nextElementSibling;

            if (!filename || !filename.classList.contains("selected-file")) {

                filename = document.createElement("p");
                filename.className = "selected-file";
                this.parentNode.appendChild(filename);

            }

            filename.innerHTML =
                "📄 Selected File: <strong>" +
                this.files[0].name +
                "</strong>";

        });

    });

    // -----------------------------
    // Fade in cards
    // -----------------------------
    document.querySelectorAll(
        ".analytics-card, .explanation-card, .history-section"
    ).forEach(card => {

        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";

        setTimeout(() => {

            card.style.transition = "0.6s ease";

            card.style.opacity = "1";
            card.style.transform = "translateY(0)";

        }, 150);

    });

    // -----------------------------
    // Back To Top Button
    // -----------------------------
    const topBtn = document.createElement("button");

    topBtn.innerHTML = "⬆";

    topBtn.id = "topBtn";

    document.body.appendChild(topBtn);

    topBtn.style.display = "none";

    window.addEventListener("scroll", function () {

        topBtn.style.display =
            window.scrollY > 300 ? "block" : "none";

    });

    topBtn.onclick = function () {

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    };

});