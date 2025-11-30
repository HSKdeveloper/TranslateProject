
// Navbar blur effect
document.addEventListener("scroll", function() {
        const nav = document.querySelector(".navbar-blur");
        if (!nav) return;
        if (window.scrollY > 50) {
                nav.style.background = "rgba(255, 255, 255, 0.6)";
                nav.style.backdropFilter = "blur(15px)";
                nav.style.webkitBackdropFilter = "blur(15px)";
        } else {
                nav.style.background = "rgba(255, 255, 255, 0.1)";
                nav.style.backdropFilter = "blur(0px)";
                nav.style.webkitBackdropFilter = "blur(0px)";
        }
});

// About boxes animation on scroll
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top < window.innerHeight - 80 &&
        rect.bottom > 0
    );
}

function animateAboutBoxes() {
    const boxes = document.querySelectorAll('.about-box');
    boxes.forEach((box, idx) => {
        if (isInViewport(box)) {
            setTimeout(() => {
                box.classList.add('show-animate');
            }, idx * 250);
        }
    });
}

window.addEventListener('scroll', animateAboutBoxes);
document.addEventListener('DOMContentLoaded', animateAboutBoxes);

