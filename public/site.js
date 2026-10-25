// Nav turns solid once the hero is behind you (home only).
const nav = document.querySelector(".nav");
if (document.body.classList.contains("home") && nav) {
  const hero = document.querySelector(".hero");
  const onScroll = () => nav.classList.toggle("solid", window.scrollY > hero.offsetHeight - 80);
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

// Plates fade up as you reach them.
const plates = [...document.querySelectorAll(".plate")];
if ("IntersectionObserver" in window) {
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
  }), { rootMargin: "0px 0px -8% 0px" });
  plates.forEach((p) => io.observe(p));
} else {
  plates.forEach((p) => p.classList.add("in"));
}

// Lightbox.
const lb = document.querySelector(".lightbox");
const data = document.getElementById("plates");
if (lb && data) {
  const items = JSON.parse(data.textContent);
  const img = lb.querySelector("img");
  const cap = lb.querySelector("figcaption");
  let cur = 0;
  const show = (i) => {
    cur = (i + items.length) % items.length;
    const it = items[cur];
    img.src = it.src;
    img.alt = `Plate ${it.no}`;
    cap.innerHTML = `<span class="no">${it.no}</span><span>${it.cap}</span><span>${it.set}</span>`;
    [cur + 1, cur - 1].forEach((j) => { const n = items[(j + items.length) % items.length]; if (n) new Image().src = n.src; });
  };
  const open = (i) => { show(i); lb.showModal(); document.body.style.overflow = "hidden"; };
  const close = () => { lb.close(); };
  lb.addEventListener("close", () => {
    document.body.style.overflow = "";
    document.getElementById("p" + (cur + 1))?.scrollIntoView({ block: "center" });
  });
  plates.forEach((p) => p.querySelector(".open").addEventListener("click", () => open(Number(p.dataset.n) - 1)));
  lb.querySelector(".lbprev").addEventListener("click", () => show(cur - 1));
  lb.querySelector(".lbnext").addEventListener("click", () => show(cur + 1));
  lb.querySelector(".lbclose").addEventListener("click", close);
  lb.addEventListener("click", (e) => { if (e.target === lb || e.target.tagName === "FIGURE") close(); });
  addEventListener("keydown", (e) => {
    if (!lb.open) return;
    if (e.key === "ArrowRight") show(cur + 1);
    if (e.key === "ArrowLeft") show(cur - 1);
  });
  let x0 = null;
  lb.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1));
    x0 = null;
  });
  // Arriving from the Index of Works with #p7 scrolls to that plate.
  const m = location.hash.match(/^#p(\d+)$/);
  if (m) document.getElementById("p" + m[1])?.scrollIntoView({ block: "center" });
}
