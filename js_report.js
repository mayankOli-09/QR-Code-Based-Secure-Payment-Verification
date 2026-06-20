async function loadHistory() {
  const res = await fetch("/api/history");
  const data = await res.json();
  const list = document.getElementById("history-list");
  list.innerHTML = "";
  data.forEach(item => {
    const div = document.createElement("div");
    div.className = "history-item";
    div.innerHTML = `
      <div><strong>Time:</strong> ${item.timestamp}</div>
      <div><strong>Score:</strong> ${item.trust_score}</div>
      <div><strong>Risk:</strong> ${item.risk_category}</div>
      <div><strong>Payment QR:</strong> ${item.is_payment_qr}</div>
      <div><strong>Action:</strong> ${item.action_recommendation}</div>
    `;
    list.appendChild(div);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const refreshBtn = document.getElementById("refresh-history-btn");
  const downloadBtn = document.getElementById("download-report-btn");
  if (refreshBtn) refreshBtn.addEventListener("click", loadHistory);
  if (downloadBtn) downloadBtn.addEventListener("click", async () => {
    const res = await fetch("/api/history");
    const data = await res.json();
    const pdfRes = await fetch("/api/report/pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ history: data })
    });
    const blob = await pdfRes.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "qr_report.txt";
    a.click();
    URL.revokeObjectURL(url);
  });
});