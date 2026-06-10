/* ═══════════════════════════════════════════════
   Business Portfolio Tracker — main.js
   ═══════════════════════════════════════════════ */

/* ── Tab switching ── */
function switchTab(id, btn) {
  document.querySelectorAll('.tab-section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  const section = document.getElementById('tab-' + id);
  if (section) section.classList.add('active');
  if (btn) btn.classList.add('active');
  // Update URL so back button and refresh preserve the tab
  const url = new URL(window.location);
  url.searchParams.set('tab', id);
  window.history.replaceState({}, '', url);
}

/* ── Plan accordion ── */
function togglePlan(row) {
  const isOpen = row.classList.contains('open');
  document.querySelectorAll('.plan-row.open').forEach(r => r.classList.remove('open'));
  if (!isOpen) {
    row.classList.add('open');
    row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

/* ── Generic show/hide toggle ── */
function toggleSection(id) {
  const el = document.getElementById(id);
  if (!el) return;
  const isHidden = el.style.display === 'none' || el.style.display === '';
  el.style.display = isHidden ? 'block' : 'none';
  if (isHidden) {
    setTimeout(() => el.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 50);
  }
}

/* ── Mobile nav drawer ── */
function toggleMobileNav() {
  const drawer  = document.getElementById('mobileDrawer');
  const overlay = document.getElementById('mobileOverlay');
  if (!drawer) return;
  const isOpen = drawer.classList.contains('open');
  drawer.classList.toggle('open', !isOpen);
  overlay.classList.toggle('open', !isOpen);
  document.body.style.overflow = isOpen ? '' : 'hidden';
}

/* ── Flash message auto-dismiss ── */
function initFlash() {
  document.querySelectorAll('.flash-msg').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .3s, transform .3s';
      el.style.opacity = '0';
      el.style.transform = 'translateY(-6px)';
      setTimeout(() => el.remove(), 320);
    }, 3800);
  });
}

/* ── Progress bar animate on load ── */
function initProgressBars() {
  document.querySelectorAll('.progress-fill').forEach(el => {
    const target = el.style.width;
    el.style.width = '0';
    el.style.transition = 'none';
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        el.style.transition = 'width .6s ease';
        el.style.width = target;
      });
    });
  });
}

/* ── Range slider live label ── */
function initRangeInputs() {
  document.querySelectorAll('.range-input').forEach(input => {
    input.addEventListener('input', () => {
      const label = input.nextElementSibling;
      if (label) label.textContent = input.value + '%';
    });
  });
}

/* ── Confirm delete forms ── */
function initConfirms() {
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', e => {
      if (!confirm(el.dataset.confirm)) e.preventDefault();
    });
  });
}

/* ── Chart.js responsive resize ── */
function initChartResize() {
  window.addEventListener('resize', () => {
    if (window.Chart && Chart.instances) {
      Object.values(Chart.instances).forEach(c => {
        try { c.resize(); } catch(e) {}
      });
    }
  });
}

/* ── Format KES numbers ── */
function fmtKES(val) {
  if (val >= 1000000) return 'KES ' + (val / 1000000).toFixed(1) + 'M';
  if (val >= 1000)    return 'KES ' + (val / 1000).toFixed(0) + 'K';
  return 'KES ' + Math.round(val).toLocaleString();
}

/* ── Active sidebar link scroll ── */
function initSidebarScroll() {
  const active = document.querySelector('.sidebar .nav-item.active');
  if (active) active.scrollIntoView({ block: 'nearest' });
}

/* ── Init all on DOM ready ── */
document.addEventListener('DOMContentLoaded', () => {
  initFlash();
  initProgressBars();
  initRangeInputs();
  initConfirms();
  initChartResize();
  initSidebarScroll();
});
