
document.addEventListener("DOMContentLoaded", function () {
    const animatedElements = document.querySelectorAll(
        ".info-card, .skill-card, .project-card, .section-heading, .technology-badge"
    );

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if (!reducedMotion && "IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            function (entries, currentObserver) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        currentObserver.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.1,
                rootMargin: "0px 0px -20px 0px"
            }
        );

        animatedElements.forEach(function (element) {
            element.classList.add("fade-in");
            observer.observe(element);
        });
    }

    const menu = document.getElementById("mainMenu");
    const links = document.querySelectorAll(".navbar .nav-link");

    links.forEach(function (link) {
        link.addEventListener("click", function () {
            if (
                menu &&
                menu.classList.contains("show") &&
                typeof bootstrap !== "undefined"
            ) {
                bootstrap.Collapse.getOrCreateInstance(menu).hide();
            }
        });
    });

    function setActiveLink(target) {
        links.forEach(function (link) {
            link.classList.remove("active-link");
            link.removeAttribute("aria-current");
        });

        if (target) {
            target.classList.add("active-link");
            target.setAttribute("aria-current", "location");
        }
    }

    const path = window.location.pathname;

    if (path === "/contacts") {
        const contactLink = document.querySelector(
            '.navbar .nav-link[href="/contacts"]'
        );
        setActiveLink(contactLink);
    } else if (path === "/") {
        const homeLink = document.querySelector(
            '.navbar .nav-link[href="/"]'
        );
        setActiveLink(homeLink);

        const sections = document.querySelectorAll(
            "#about, #education, #skills, #technologies, #projects"
        );

        if ("IntersectionObserver" in window) {
            const sectionObserver = new IntersectionObserver(
                function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            const activeLink = document.querySelector(
                                '.navbar .nav-link[href$="#' +
                                entry.target.id + '"]'
                            );

                            setActiveLink(activeLink);
                        }
                    });
                },
                {
                    rootMargin: "-20% 0px -60% 0px"
                }
            );

            sections.forEach(function (section) {
                sectionObserver.observe(section);
            });
        }

        window.addEventListener("scroll", function () {
            if (window.scrollY < 120) {
                setActiveLink(homeLink);
            }
        }, { passive: true });
    }
});
