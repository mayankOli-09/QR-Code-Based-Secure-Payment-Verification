function applyThemeFromSettings(settings) {
  document.body.classList.toggle("dark-mode", !!settings.dark_mode);
  document.body.classList.remove("theme-professional", "theme-clean", "theme-student");
  document.body.classList.add(`theme-${settings.theme || "professional"}`);
}

async function fetchSettings() {
  const res = await fetch("/api/settings");
  return await res.json();
}

document.addEventListener("DOMContentLoaded", async () => {
  const settings = await fetchSettings();
  applyThemeFromSettings(settings);
  const currentMode = document.getElementById("current-mode");
  if (currentMode) currentMode.textContent = (settings.verification_mode || "local").toUpperCase();
});