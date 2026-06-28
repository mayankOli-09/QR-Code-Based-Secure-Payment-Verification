/* ── Config ──────────────────────────────────────────────── */
const API_BASE = "http://localhost:8000";

/* ── DOM refs ────────────────────────────────────────────── */
const dropZone    = document.getElementById("dropZone");
const fileInput   = document.getElementById("fileInput");
const previewWrap = document.getElementById("previewWrap");
const previewImg  = document.getElementById("previewImg");
const clearBtn    = document.getElementById("clearBtn");
const verifyBtn   = document.getElementById("verifyBtn");
const uploadSection = document.getElementById("uploadSection");
const loader      = document.getElementById("loader");
const resultSection = document.getElementById("resultSection");

// Result elements
const scoreNum      = document.getElementById("scoreNum");
const ringFill      = document.getElementById("ringFill");
const ratingBadge   = document.getElementById("ratingBadge");
const recommendation= document.getElementById("recommendation");
const detailsGrid   = document.getElementById("detailsGrid");
const checksList    = document.getElementById("checksList");
const rawData       = document.getElementById("rawData");
const scanAgainBtn  = document.getElementById("scanAgainBtn");

/* ── State ───────────────────────────────────────────────── */
let selectedFile = null;

/* ── File selection ──────────────────────────────────────── */
fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) setFile(fileInput.files[0]);
});

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("drag-over");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith("image/")) setFile(file);
});

function setFile(file) {
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    previewWrap.style.display = "block";
    dropZone.style.display = "none";
    verifyBtn.disabled = false;
  };
  reader.readAsDataURL(file);
}

clearBtn.addEventListener("click", resetUpload);

function resetUpload() {
  selectedFile = null;
  fileInput.value = "";
  previewImg.src = "";
  previewWrap.style.display = "none";
  dropZone.style.display = "block";
  verifyBtn.disabled = true;
}

/* ── Verify ──────────────────────────────────────────────── */
verifyBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  // Show loader
  uploadSection.style.display = "none";
  resultSection.style.display = "none";
  loader.style.display = "block";

  try {
    const formData = new FormData();
    formData.append("file", selectedFile);

    const resp = await fetch(`${API_BASE}/verify`, {
      method: "POST",
      body: formData,
    });

    if (!resp.ok) {
      const err = await resp.json();
      throw new Error(err.detail || `Server error: ${resp.status}`);
    }

    const data = await resp.json();
    renderResult(data);
  } catch (err) {
    loader.style.display = "none";
    uploadSection.style.display = "flex";
    alert(`Error: ${err.message}`);
  }
});

/* ── Render result ───────────────────────────────────────── */
function renderResult(data) {
  loader.style.display = "none";

  // Score ring
  const score = data.trust_score ?? 0;
  const circumference = 326.7;
  const offset = circumference - (score / 100) * circumference;

  // Ring colour
  let ringColor = "var(--accent)";
  if (data.rating === "SAFE")      ringColor = "var(--safe)";
  else if (data.rating === "WARNING") ringColor = "var(--warn)";
  else if (data.rating === "DANGEROUS") ringColor = "var(--danger)";

  ringFill.style.stroke = ringColor;

  // Animate score
  animateScore(score);
  setTimeout(() => {
    ringFill.style.strokeDashoffset = offset;
  }, 80);

  // Rating badge
  ratingBadge.textContent = data.rating;
  ratingBadge.className = `rating-badge ${data.rating}`;

  recommendation.textContent = data.recommendation;

  // Details grid
  detailsGrid.innerHTML = "";
  const details = buildDetails(data);
  details.forEach(({ label, value }) => {
    detailsGrid.innerHTML += `
      <div class="detail-card">
        <div class="label">${label}</div>
        <div class="value">${value}</div>
      </div>`;
  });

  // Checks list
  checksList.innerHTML = "";
  (data.checks || []).forEach((check) => {
    const cls = check.passed === true ? "pass" : check.passed === false ? "fail" : "neutral";
    const icon = check.passed === true ? "✓" : check.passed === false ? "✗" : "·";
    checksList.innerHTML += `
      <li class="check-item ${cls}">
        <span class="check-icon">${icon}</span>
        <span>${check.label}</span>
      </li>`;
  });

  // Raw data
  rawData.textContent = data.raw_data || "—";

  resultSection.style.display = "flex";
}

function buildDetails(data) {
  const details = [];
  details.push({ label: "QR Type", value: data.type?.toUpperCase() || "UNKNOWN" });

  if (data.upi_info) {
    const u = data.upi_info;
    details.push({ label: "Payee Name",     value: u.payee_name    || "Not specified" });
    details.push({ label: "UPI ID",         value: u.payment_address || "—" });
    details.push({ label: "Amount",         value: u.amount ? `₹${parseFloat(u.amount).toLocaleString("en-IN")}` : "Not specified" });
    details.push({ label: "Currency",       value: u.currency || "INR" });
    if (u.transaction_note) {
      details.push({ label: "Note",         value: u.transaction_note });
    }
  }

  if (data.url_safety) {
    const s = data.url_safety;
    details.push({ label: "URL Safety",     value: s.is_safe === true ? "✓ Safe" : s.is_safe === false ? "✗ Unsafe" : "Unknown" });
    details.push({ label: "Checked Via",    value: (s.sources_checked || []).join(", ") || "—" });
  }

  return details;
}

function animateScore(target) {
  let current = 0;
  const step = Math.ceil(target / 40);
  const interval = setInterval(() => {
    current = Math.min(current + step, target);
    scoreNum.textContent = current;
    if (current >= target) clearInterval(interval);
  }, 25);
}

/* ── Scan Again ──────────────────────────────────────────── */
scanAgainBtn.addEventListener("click", () => {
  resultSection.style.display = "none";
  uploadSection.style.display = "flex";
  resetUpload();
  // Reset ring
  ringFill.style.strokeDashoffset = 326.7;
  scoreNum.textContent = "0";
});