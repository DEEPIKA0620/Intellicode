// ================================
// IntelliCode UI Enhancements
// ================================

// Fade in cards
document.addEventListener("DOMContentLoaded", () => {

    const cards = document.querySelectorAll(
        ".analytics-card, .prediction-card, .history-section, .explanation-card, .python-analysis-card, .metrics-card"
    );

    cards.forEach((card, index) => {
        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";

        setTimeout(() => {
            card.style.transition = "all 0.6s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, index * 100);
    });

});

// Button click animation
document.querySelectorAll("button").forEach(button => {

    button.addEventListener("click", () => {

        button.style.transform = "scale(0.96)";

        setTimeout(() => {
            button.style.transform = "scale(1)";
        }, 150);

    });

});

// Back to Top button
const topBtn = document.createElement("button");
topBtn.innerHTML = "↑";
topBtn.id = "topBtn";

document.body.appendChild(topBtn);

topBtn.style.display = "none";

window.addEventListener("scroll", () => {

    if (window.scrollY > 300) {
        topBtn.style.display = "block";
    } else {
        topBtn.style.display = "none";
    }

});

topBtn.onclick = () => {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
};