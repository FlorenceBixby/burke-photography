// Motion (motion.dev, vendored at /vendor/motion-14.1.0.js) drives every
// reveal; CSS view transitions handle the cross-page fade. With reduced
// motion, or if Motion fails to load, everything just shows.
const M = window.Motion;
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const live = !!M && !reduced;
if (live) window.__motion = true;
else document.documentElement.classList.remove("m");

const EASE = [0.22, 1, 0.36, 1];
const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];
const rise = (els, opts = {}) =>
  M.animate(els, { opacity: [0, 1], y: [opts.y ?? 28, 0], filter: ["blur(6px)", "blur(0px)"] },
    { duration: opts.duration ?? 1.1, ease: EASE, delay: opts.delay ?? 0 });

// ---------- nav ----------
const nav = $(".nav");
const home = document.body.classList.contains("home");
if (nav) {
  const hero = $(".hero");
  let lastY = scrollY, hidden = false;
  const onScroll = () => {
    const y = scrollY;
    if (home && hero) nav.classList.toggle("solid", y > hero.offsetHeight - 80);
    // Inside a gallery the nav tucks away while you scroll down to look,
    // and comes back the moment you scroll up.
    if (live && document.body.classList.contains("exhibit")) {
      const hide = y > 240 && y > lastY + 4;
      const show = y < lastY - 4 || y < 240;
      if (hide && !hidden) { hidden = true; M.animate(nav, { y: "-110%" }, { duration: 0.45, ease: EASE }); }
      if (show && hidden) { hidden = false; M.animate(nav, { y: "0%" }, { duration: 0.45, ease: EASE }); }
    }
    lastY = y;
  };
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

if (live) {
  // ---------- landing ----------
  const h1 = $(".herotext h1");
  if (h1) {
    // Name assembles letter by letter.
    h1.innerHTML = [...h1.textContent].map((c) => (c === " " ? '<span class="sp"> </span>' : `<span class="ch">${c}</span>`)).join("");
    h1.style.opacity = 1;
    M.animate($$(".ch", h1), { opacity: [0, 1], y: ["0.45em", "0em"], filter: ["blur(10px)", "blur(0px)"] },
      { duration: 1.2, ease: EASE, delay: M.stagger(0.045, { startDelay: 0.25 }) });
    rise($(".herotext .label"), { delay: 0.95, y: 14 });
    M.animate($(".scrollcue"), { opacity: [0, 1] }, { duration: 1, delay: 1.5 });
    M.animate($(".heroframe"), { scale: [1.12, 1], opacity: [0, 1] }, { duration: 2.4, ease: EASE });

    // The hero drifts up slower than the page and the title lifts away.
    const hero = $(".hero");
    M.scroll(M.animate($(".heroframe"), { y: ["0%", "22%"] }, { ease: "linear" }), { target: hero, offset: ["start start", "end start"] });
    M.scroll(M.animate($(".herotext"), { y: [0, -90], opacity: [1, 0] }, { ease: "linear" }), { target: hero, offset: ["start start", "0.7 start"] });
  }

  M.inView(".statement", (el) => {
    rise($$("p", el), { delay: M.stagger(0.18), y: 34, duration: 1.3 });
    rise($(".sig"), { delay: 0.6, y: 10 });
  }, { amount: 0.35 });

  M.inView(".roomshead", (el) => { rise(el, { y: 16 }); }, { amount: 0.6 });

  // Gallery cards: the photo wipes up into its frame, the text follows.
  $$(".room").forEach((room) => {
    M.inView(room, () => {
      const frame = $(".roomimg", room);
      M.animate(frame, { clipPath: ["inset(100% 0 0 0)", "inset(0% 0 0 0)"] }, { duration: 1.3, ease: EASE });
      M.animate($("img", frame), { scale: [1.22, 1] }, { duration: 1.8, ease: EASE });
      rise($$(".roomtext > *", room), { delay: M.stagger(0.08, { startDelay: 0.25 }), y: 22 });
    }, { amount: 0.3 });
  });

  // ---------- page heads ----------
  const ph = $$(".pagehead > *");
  if (ph.length) rise(ph, { delay: M.stagger(0.1, { startDelay: 0.1 }) });

  $$(".exitem").forEach((item, i) => {
    M.inView(item, () => {
      rise(item, { y: 40, delay: (i % 2) * 0.12 });
      M.animate($("img", item), { scale: [1.15, 1] }, { duration: 1.6, ease: EASE, delay: (i % 2) * 0.12 });
    }, { amount: 0.25 });
  });

  $$(".iw").forEach((sec) => {
    M.inView(sec, () => {
      M.animate(sec, { opacity: [0, 1] }, { duration: 0.6 });
      M.animate($$(".thumb", sec), { opacity: [0, 1], y: [18, 0], scale: [0.96, 1] },
        { duration: 0.8, ease: EASE, delay: M.stagger(0.03) });
    }, { amount: 0.15 });
  });

  const ag = $$(".aboutgrid > *");
  if (ag.length) {
    rise(ag, { delay: M.stagger(0.15, { startDelay: 0.3 }), y: 30 });
    M.animate($(".aboutgrid img"), { scale: [1.12, 1] }, { duration: 1.8, ease: EASE, delay: 0.3 });
  }

  // ---------- a gallery ----------
  const wall = $$(".wall > :not(.walltext)");
  if (wall.length) {
    rise(wall, { delay: M.stagger(0.1, { startDelay: 0.15 }) });
    M.animate($(".walltext"), { opacity: [0, 1] }, { duration: 0.01, delay: 0.3 });
    rise($$(".walltext p"), { delay: M.stagger(0.14, { startDelay: 0.45 }), y: 20 });
  }

  // Each plate: frame rises, photo settles inside it, placard arrives last.
  $$(".plate").forEach((plate) => {
    M.inView(plate, () => {
      M.animate(plate, { opacity: [0, 1], y: [70, 0] }, { duration: 1.3, ease: EASE });
      M.animate($("img", plate), { scale: [1.1, 1] }, { duration: 1.9, ease: EASE });
      M.animate($("figcaption", plate), { opacity: [0, 1], y: [8, 0] }, { duration: 0.9, ease: EASE, delay: 0.45 });
    }, { amount: 0.18 });
  });

  M.inView(".nextroom", (el) => { rise(el, { y: 30 }); }, { amount: 0.4 });

  // Hover: photos on the wall lean in slightly.
  $$(".plate .open").forEach((btn) => {
    const img = $("img", btn);
    M.hover(btn, () => {
      M.animate(img, { scale: 1.015 }, { type: "spring", bounce: 0.2, visualDuration: 0.5 });
      return () => M.animate(img, { scale: 1 }, { type: "spring", bounce: 0.2, visualDuration: 0.5 });
    });
  });
}

// ---------- lightbox ----------
const lb = $(".lightbox");
const data = document.getElementById("plates");
if (lb && data) {
  const items = JSON.parse(data.textContent);
  const img = $("img", lb);
  const cap = $("figcaption", lb);
  const plates = $$(".plate");
  let cur = 0, busy = false, closing = false, pending = 0;

  const fill = (i) => {
    cur = (i + items.length) % items.length;
    const it = items[cur];
    img.sizes = "100vw";
    img.srcset = it.srcset;
    img.src = it.src;
    img.alt = `Plate ${it.no}`;
    cap.innerHTML = `<span class="no">${it.no}</span><span>${it.cap}</span><span>${it.set}</span>`;
    [cur + 1, cur - 1].forEach((j) => {
      const n = items[(j + items.length) % items.length], pre = new Image();
      pre.sizes = "100vw"; pre.srcset = n.srcset; pre.src = n.src;
    });
  };
  const loaded = () => (img.complete && img.naturalWidth ? Promise.resolve() : img.decode().catch(() => {}));
  const plateImg = (i) => plates[i] && $("img", plates[i]);

  // Grow the photo out of its spot on the wall (FLIP).
  const flipFrom = (fromEl, reverse = false) => {
    const a = fromEl.getBoundingClientRect(), b = img.getBoundingClientRect();
    if (!a.width || !b.width) return Promise.resolve();
    const from = { x: a.left + a.width / 2 - (b.left + b.width / 2), y: a.top + a.height / 2 - (b.top + b.height / 2), scale: a.width / b.width };
    const kf = reverse
      ? { x: [0, from.x], y: [0, from.y], scale: [1, from.scale] }
      : { x: [from.x, 0], y: [from.y, 0], scale: [from.scale, 1] };
    return M.animate(img, kf, { type: "spring", bounce: 0.12, visualDuration: reverse ? 0.45 : 0.6 }).finished;
  };

  const open = async (i) => {
    fill(i);
    lb.showModal();
    document.body.style.overflow = "hidden";
    if (!live) return;
    busy = true;
    const src = plateImg(cur);
    M.animate(lb, { backgroundColor: ["rgba(14,13,11,0)", "rgba(14,13,11,.97)"] }, { duration: 0.45 });
    M.animate([cap, $(".lbclose", lb), $(".lbprev", lb), $(".lbnext", lb)], { opacity: [0, 1] }, { duration: 0.5, delay: 0.3 });
    await loaded();
    if (src) { src.style.visibility = "hidden"; await flipFrom(src); src.style.visibility = ""; }
    busy = false;
    if (pending && !closing) { const n = pending; pending = 0; step(n); }
  };

  // Closing is always allowed, even mid-animation.
  const close = async () => {
    if (!live) { lb.close(); return; }
    if (closing) return;
    closing = true; busy = true; pending = 0;
    M.animate(img, { opacity: 1 }, { duration: 0.01 });
    const dst = plateImg(cur);
    // Bring the plate into view first so the photo can fly home to it.
    dst?.closest(".plate").scrollIntoView({ block: "center", behavior: "instant" });
    M.animate(lb, { backgroundColor: "rgba(14,13,11,0)" }, { duration: 0.4 });
    M.animate([cap, $(".lbclose", lb), $(".lbprev", lb), $(".lbnext", lb)], { opacity: 0 }, { duration: 0.2 });
    if (dst) { dst.style.visibility = "hidden"; await flipFrom(dst, true); dst.style.visibility = ""; }
    lb.close();
    img.style.transform = ""; lb.style.backgroundColor = "";
    [cap, $(".lbclose", lb), $(".lbprev", lb), $(".lbnext", lb)].forEach((e) => (e.style.opacity = ""));
    busy = false; closing = false;
  };

  // Slide between photos in the direction you're moving. Presses that land
  // mid-slide are queued (latest wins) instead of dropped.
  const step = async (d) => {
    if (!live) { fill(cur + d); return; }
    if (busy) { if (!closing) pending = d; return; }
    busy = true;
    await M.animate(img, { opacity: 0, x: -60 * d }, { duration: 0.2, ease: [0.4, 0, 1, 1] }).finished;
    if (closing) return;
    fill(cur + d);
    await loaded();
    if (closing) return;
    await M.animate(img, { opacity: [0, 1], x: [60 * d, 0] }, { duration: 0.4, ease: EASE }).finished;
    busy = false;
    if (pending) { const n = pending; pending = 0; step(n); }
  };

  lb.addEventListener("close", () => { document.body.style.overflow = ""; });
  lb.addEventListener("cancel", (e) => { e.preventDefault(); close(); });
  plates.forEach((p) => $(".open", p).addEventListener("click", () => open(Number(p.dataset.n) - 1)));
  $(".lbprev", lb).addEventListener("click", () => step(-1));
  $(".lbnext", lb).addEventListener("click", () => step(1));
  $(".lbclose", lb).addEventListener("click", close);
  lb.addEventListener("click", (e) => { if (e.target === lb || e.target.tagName === "FIGURE") close(); });
  addEventListener("keydown", (e) => {
    if (!lb.open) return;
    if (e.key === "ArrowRight") step(1);
    if (e.key === "ArrowLeft") step(-1);
  });
  let x0 = null;
  lb.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener("touchend", (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1);
    x0 = null;
  });
  // Arriving from the Index of Works with #p7 scrolls to that plate.
  const m = location.hash.match(/^#p(\d+)$/);
  if (m) document.getElementById("p" + m[1])?.scrollIntoView({ block: "center" });
}
