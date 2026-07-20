/* ── Config ──────────────────────────────────────────────── */
const API_BASE = "http://127.0.0.1:8000";

/* ── Tab switching ───────────────────────────────────────── */
document.querySelectorAll(".tab-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(`tab-${btn.dataset.tab}`).classList.add("active");
  });
});

/* ── QR TAB ──────────────────────────────────────────────── */
const dropZone      = document.getElementById("dropZone");
const fileInput     = document.getElementById("fileInput");
const previewWrap   = document.getElementById("previewWrap");
const previewImg    = document.getElementById("previewImg");
const clearBtn      = document.getElementById("clearBtn");
const verifyBtn     = document.getElementById("verifyBtn");
const uploadSection = document.getElementById("uploadSection");
const loader        = document.getElementById("loader");
const resultSection = document.getElementById("resultSection");
const scoreNum      = document.getElementById("scoreNum");
const ringFill      = document.getElementById("ringFill");
const ratingBadge   = document.getElementById("ratingBadge");
const recommendation= document.getElementById("recommendation");
const detailsGrid   = document.getElementById("detailsGrid");
const checksList    = document.getElementById("checksList");
const rawData       = document.getElementById("rawData");
const scanAgainBtn  = document.getElementById("scanAgainBtn");

let selectedFile = null;

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) setFile(fileInput.files[0]);
});

dropZone.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("dragover", (e) => { e.preventDefault(); dropZone.classList.add("drag-over"); });
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));
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

verifyBtn.addEventListener("click", async () => {
  if (!selectedFile) return;
  uploadSection.style.display = "none";
  resultSection.style.display = "none";
  loader.style.display = "block";

  try {
    const formData = new FormData();
    formData.append("file", selectedFile);
    const resp = await fetch(`${API_BASE}/verify`, { method: "POST", body: formData });
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

function renderResult(data) {
  loader.style.display = "none";
  const score = data.trust_score ?? 0;
  const circumference = 326.7;
  const offset = circumference - (score / 100) * circumference;

  let ringColor = "var(--accent)";
  if (data.rating === "SAFE")      ringColor = "var(--safe)";
  else if (data.rating === "WARNING")   ringColor = "var(--warn)";
  else if (data.rating === "DANGEROUS") ringColor = "var(--danger)";

  ringFill.style.stroke = ringColor;
  animateScore(score);
  setTimeout(() => { ringFill.style.strokeDashoffset = offset; }, 80);

  ratingBadge.textContent = data.rating;
  ratingBadge.className = `rating-badge ${data.rating}`;
  recommendation.textContent = data.recommendation;

  detailsGrid.innerHTML = "";
  buildDetails(data).forEach(({ label, value }) => {
    detailsGrid.innerHTML += `
      <div class="detail-card">
        <div class="label">${label}</div>
        <div class="value">${value}</div>
      </div>`;
  });

  checksList.innerHTML = "";
  (data.checks || []).forEach((check) => {
    const cls  = check.passed === true ? "pass" : check.passed === false ? "fail" : "neutral";
    const icon = check.passed === true ? "✓"    : check.passed === false ? "✗"    : "·";
    checksList.innerHTML += `
      <li class="check-item ${cls}">
        <span class="check-icon">${icon}</span>
        <span>${check.label}</span>
      </li>`;
  });

  rawData.textContent = data.raw_data || "—";
  resultSection.style.display = "flex";
}

function buildDetails(data) {
  const details = [];
  details.push({ label: "QR Type", value: data.type?.toUpperCase() || "UNKNOWN" });
  if (data.upi_info) {
    const u = data.upi_info;
    details.push({ label: "Payee Name",  value: u.payee_name       || "Not specified" });
    details.push({ label: "UPI ID",      value: u.payment_address  || "—" });
    details.push({ label: "Amount",      value: u.amount ? `₹${parseFloat(u.amount).toLocaleString("en-IN")}` : "Not specified" });
    details.push({ label: "Currency",    value: u.currency         || "INR" });
    if (u.transaction_note) details.push({ label: "Note", value: u.transaction_note });
  }
  if (data.url_safety) {
    const s = data.url_safety;
    details.push({ label: "URL Safety",  value: s.is_safe === true ? "✓ Safe" : s.is_safe === false ? "✗ Unsafe" : "Unknown" });
    details.push({ label: "Checked Via", value: (s.sources_checked || []).join(", ") || "—" });
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

scanAgainBtn.addEventListener("click", () => {
  resultSection.style.display = "none";
  uploadSection.style.display = "flex";
  resetUpload();
  ringFill.style.strokeDashoffset = 326.7;
  scoreNum.textContent = "0";
});

/* ── SCREENSHOT TAB ──────────────────────────────────────── */
const ssDropZone      = document.getElementById("ssDropZone");
const ssFileInput     = document.getElementById("ssFileInput");
const ssPreviewWrap   = document.getElementById("ssPreviewWrap");
const ssPreviewImg    = document.getElementById("ssPreviewImg");
const ssClearBtn      = document.getElementById("ssClearBtn");
const ssVerifyBtn     = document.getElementById("ssVerifyBtn");
const ssUploadSection = document.getElementById("ssUploadSection");
const ssLoader        = document.getElementById("ssLoader");
const ssResultSection = document.getElementById("ssResultSection");
const ssBanner        = document.getElementById("ssBanner");
const ssVerdictIcon   = document.getElementById("ssVerdictIcon");
const ssVerdict       = document.getElementById("ssVerdict");
const ssRecommendation= document.getElementById("ssRecommendation");
const ssDetailsGrid   = document.getElementById("ssDetailsGrid");
const ssChecksList    = document.getElementById("ssChecksList");
const ssRawText       = document.getElementById("ssRawText");
const ssScanAgainBtn  = document.getElementById("ssScanAgainBtn");

let ssSelectedFile = null;

ssFileInput.addEventListener("change", () => {
  if (ssFileInput.files[0]) ssSetFile(ssFileInput.files[0]);
});

ssDropZone.addEventListener("click", () => ssFileInput.click());
ssDropZone.addEventListener("dragover", (e) => { e.preventDefault(); ssDropZone.classList.add("drag-over"); });
ssDropZone.addEventListener("dragleave", () => ssDropZone.classList.remove("drag-over"));
ssDropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  ssDropZone.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith("image/")) ssSetFile(file);
});

function ssSetFile(file) {
  ssSelectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    ssPreviewImg.src = e.target.result;
    ssPreviewWrap.style.display = "block";
    ssDropZone.style.display = "none";
    ssVerifyBtn.disabled = false;
  };
  reader.readAsDataURL(file);
}

ssClearBtn.addEventListener("click", ssResetUpload);

function ssResetUpload() {
  ssSelectedFile = null;
  ssFileInput.value = "";
  ssPreviewImg.src = "";
  ssPreviewWrap.style.display = "none";
  ssDropZone.style.display = "block";
  ssVerifyBtn.disabled = true;
}

ssVerifyBtn.addEventListener("click", async () => {
  if (!ssSelectedFile) return;
  ssUploadSection.style.display = "none";
  ssResultSection.style.display = "none";
  ssLoader.style.display = "block";

  try {
    const formData = new FormData();
    formData.append("file", ssSelectedFile);
    const resp = await fetch(`${API_BASE}/verify-screenshot`, { method: "POST", body: formData });
    if (!resp.ok) {
      const err = await resp.json();
      throw new Error(err.detail || `Server error: ${resp.status}`);
    }
    const data = await resp.json();
    renderScreenshotResult(data);
  } catch (err) {
    ssLoader.style.display = "none";
    ssUploadSection.style.display = "flex";
    alert(`Error: ${err.message}`);
  }
});

function renderScreenshotResult(data) {
  ssLoader.style.display = "none";

  // Verdict banner
  const verdictMap = {
    "LIKELY REAL":  { icon: "✅", cls: "REAL",       color: "var(--safe)" },
    "SUSPICIOUS":   { icon: "⚠️", cls: "SUSPICIOUS",  color: "var(--warn)" },
    "LIKELY FAKE":  { icon: "❌", cls: "FAKE",        color: "var(--danger)" },
    "UNKNOWN":      { icon: "❓", cls: "",             color: "var(--muted)" },
    "ERROR":        { icon: "⚠️", cls: "",             color: "var(--muted)" },
  };

  const v = verdictMap[data.verdict] || verdictMap["UNKNOWN"];
  ssVerdictIcon.textContent   = v.icon;
  ssVerdict.textContent       = data.verdict;
  ssVerdict.style.color       = v.color;
  ssRecommendation.textContent= data.recommendation;
  ssBanner.className          = `verdict-banner ${v.cls}`;

  // Details
  ssDetailsGrid.innerHTML = "";
  const details = [];
  if (data.transaction_id) details.push({ label: "Transaction ID", value: data.transaction_id });
  if (data.amount)         details.push({ label: "Amount Detected", value: `₹${data.amount}` });
  if (data.app_detected)   details.push({ label: "App Detected", value: data.app_detected });
  details.push({ label: "Confidence", value: `${data.confidence} / 100` });

  details.forEach(({ label, value }) => {
    ssDetailsGrid.innerHTML += `
      <div class="detail-card">
        <div class="label">${label}</div>
        <div class="value">${value}</div>
      </div>`;
  });

  // Checks
  ssChecksList.innerHTML = "";
  (data.checks || []).forEach((check) => {
    const cls  = check.passed === true ? "pass" : check.passed === false ? "fail" : "neutral";
    const icon = check.passed === true ? "✓"    : check.passed === false ? "✗"    : "·";
    ssChecksList.innerHTML += `
      <li class="check-item ${cls}">
        <span class="check-icon">${icon}</span>
        <span>${check.label}</span>
      </li>`;
  });

  // Raw OCR text
  ssRawText.textContent = data.extracted_text || "No text extracted.";
  ssResultSection.style.display = "flex";
}

ssScanAgainBtn.addEventListener("click", () => {
  ssResultSection.style.display = "none";
  ssUploadSection.style.display = "flex";
  ssResetUpload();
});