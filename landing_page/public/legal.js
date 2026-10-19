// Legal pages: theme toggle, header border on scroll, footer year, and
// highlighting the current section in the table of contents.
(function () {
  const root = document.documentElement;

  const header = document.querySelector(".site-header");
  const onScroll = () => header && header.classList.toggle("scrolled", window.scrollY > 8);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const current =
        root.dataset.theme ||
        (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      const next = current === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try {
        localStorage.setItem("dartic-theme", next);
      } catch (e) {}
    });
  }

  const year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  // Close the mobile TOC after picking a section.
  const details = document.querySelector(".legal-toc details");
  document.querySelectorAll(".legal-toc a").forEach((a) =>
    a.addEventListener("click", () => {
      if (details && window.matchMedia("(max-width: 900px)").matches) details.open = false;
    }),
  );

  if (!("IntersectionObserver" in window)) return;
  const links = new Map(
    [...document.querySelectorAll(".legal-toc a")].map((a) => [a.getAttribute("href").slice(1), a]),
  );
  const visible = new Set();
  const observer = new IntersectionObserver(
    (entries) => {
      for (const e of entries) e.isIntersecting ? visible.add(e.target.id) : visible.delete(e.target.id);
      const first = [...links.keys()].find((id) => visible.has(id));
      if (!first) return;
      links.forEach((a, id) => a.setAttribute("aria-current", String(id === first)));
    },
    { rootMargin: "-80px 0px -55% 0px" },
  );
  document.querySelectorAll(".legal-body section[id]").forEach((s) => observer.observe(s));
})();
