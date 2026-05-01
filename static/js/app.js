// ── Stars ──────────────────────────────────────────────────────────────────
(function initStars() {
  const canvas = document.getElementById('stars-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let stars = [];

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    stars = Array.from({ length: 160 }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 1.3 + 0.2,
      tp: Math.random() * Math.PI * 2,
      tw: Math.random() * 0.018 + 0.004,
      dx: (Math.random() - 0.5) * 0.06,
      dy: (Math.random() - 0.5) * 0.06,
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    stars.forEach(s => {
      s.tp += s.tw; s.x += s.dx; s.y += s.dy;
      if (s.x < 0) s.x = canvas.width;
      if (s.x > canvas.width) s.x = 0;
      if (s.y < 0) s.y = canvas.height;
      if (s.y > canvas.height) s.y = 0;
      const alpha = ((Math.sin(s.tp) + 1) / 2) * 0.65 + 0.1;
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(160,200,255,${alpha})`;
      ctx.fill();
    });
    requestAnimationFrame(draw);
  }

  resize();
  draw();
  window.addEventListener('resize', resize);
})();

// ── 3D Card Tilt ────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Apply tilt to all glass cards
  document.querySelectorAll('.glass-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const r = card.getBoundingClientRect();
      const x = e.clientX - r.left;
      const y = e.clientY - r.top;
      const cx = r.width / 2;
      const cy = r.height / 2;
      const rotX = ((y - cy) / cy) * -6;
      const rotY = ((x - cx) / cx) * 6;
      card.style.transform = `perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-4px)`;
      card.style.boxShadow = `0 24px 60px rgba(0,0,0,.6), 0 0 0 1px rgba(19,120,255,.15)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
      card.style.boxShadow = '';
    });
  });

  // ── Image Upload Zone ──────────────────────────────────────────────────────
  const input   = document.getElementById('imageInput');
  const zone    = document.getElementById('uploadZone');
  const preview = document.getElementById('previewImage');

  if (input && zone && preview) {
    const showPreview = file => {
      if (!file || !file.type.startsWith('image/')) return;
      const reader = new FileReader();
      reader.onload = e => { preview.src = e.target.result; zone.classList.add('has-image'); };
      reader.readAsDataURL(file);
    };

    input.addEventListener('change', () => showPreview(input.files[0]));

    ['dragenter', 'dragover'].forEach(ev =>
      zone.addEventListener(ev, e => { e.preventDefault(); zone.classList.add('dragover'); })
    );
    ['dragleave', 'drop'].forEach(ev =>
      zone.addEventListener(ev, e => { e.preventDefault(); zone.classList.remove('dragover'); })
    );
    zone.addEventListener('drop', e => {
      const file = e.dataTransfer.files[0];
      if (!file) return;
      const dt = new DataTransfer();
      dt.items.add(file);
      input.files = dt.files;
      showPreview(file);
    });
  }

  // ── Confidence Ring ────────────────────────────────────────────────────────
  document.querySelectorAll('.confidence-ring').forEach(ring => {
    const pct = Number(ring.dataset.percent || 0);
    // Animate from 0 to pct
    let start = null;
    const duration = 1400;
    function animate(ts) {
      if (!start) start = ts;
      const progress = Math.min((ts - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      ring.style.setProperty('--percent', ease * pct);
      if (progress < 1) requestAnimationFrame(animate);
    }
    requestAnimationFrame(animate);
  });

  // ── Stat count-up ──────────────────────────────────────────────────────────
  const statObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseInt(el.textContent);
      let start = null;
      const dur = 1600;
      function tick(ts) {
        if (!start) start = ts;
        const p = Math.min((ts - start) / dur, 1);
        const ease = 1 - Math.pow(1 - p, 4);
        el.textContent = Math.round(ease * target);
        if (p < 1) requestAnimationFrame(tick);
        else el.textContent = target;
      }
      requestAnimationFrame(tick);
      statObs.unobserve(el);
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.stat-card h3').forEach(el => statObs.observe(el));

  // ── Reveal on scroll ───────────────────────────────────────────────────────
  const revealObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('reveal'); revealObs.unobserve(e.target); }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.glass-card:not(.reveal), .stats-grid, .dashboard-grid').forEach(el =>
    revealObs.observe(el)
  );
});
