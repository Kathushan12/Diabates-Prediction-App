const form = document.getElementById("predictForm");
const result = document.getElementById("result");
const btn = document.getElementById("btn");
const resetBtn = document.getElementById("resetBtn");

const apiStatus = document.getElementById("apiStatus");
const modelLoaded = document.getElementById("modelLoaded");

// ✅ Theme + History elements (exist in your index.html)
const themeBtn = document.getElementById("themeBtn");
const historyList = document.getElementById("historyList");
const clearHistoryBtn = document.getElementById("clearHistory");

// ✅ LocalStorage keys
const HISTORY_KEY = "diabetes_pred_history_v1";
const THEME_KEY = "diabetes_ui_theme_v1";

function setLoading(isLoading) {
  btn.disabled = isLoading;
  const spinner = btn.querySelector(".spinner");
  const text = btn.querySelector(".btn-text");

  if (isLoading) {
    spinner.style.display = "inline-block";
    text.textContent = "Predicting…";
  } else {
    spinner.style.display = "none";
    text.textContent = "Predict";
  }
}

function renderEmpty() {
  result.className = "result empty";
  result.innerHTML = `
    <div class="pulse-dot" aria-hidden="true"></div>
    <p class="muted">Submit the form to get a prediction.</p>
  `;
}

function renderError(message) {
  result.className = "result";
  result.innerHTML = `
    <div class="badge high">⚠️ Error</div>
    <p class="muted" style="margin-top:10px; white-space:pre-wrap;">${message}</p>
  `;
}

function renderResult(prediction, probability, label) {
  const pct = Math.max(0, Math.min(100, probability * 100));
  const risk = prediction === 1 ? "high" : "low";
  const icon = prediction === 1 ? "🧨" : "✅";

  result.className = "result";
  result.innerHTML = `
    <div class="badge ${risk}">
      ${icon} ${label}
    </div>

    <div class="prog">
      <div class="prog-top">
        <span>Diabetes probability</span>
        <span><b>${pct.toFixed(2)}%</b></span>
      </div>
      <div class="bar"><div class="fill" style="width:${pct}%;"></div></div>
      <p class="muted" style="margin:10px 0 0; font-size:12px;">
        Prediction (0/1): <b>${prediction}</b>
      </p>
    </div>
  `;
}

async function checkHealth() {
  try {
    const res = await fetch("/health");
    if (!res.ok) throw new Error(`Health check failed (${res.status})`);
    const data = await res.json();

    apiStatus.textContent = "Online";
    modelLoaded.textContent = data.model_loaded ? "Loaded" : "Not loaded";
  } catch (e) {
    apiStatus.textContent = "Offline";
    modelLoaded.textContent = "—";
  }
}

/* -----------------------------
   ✅ Theme (dark/light)
-------------------------------- */
function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem(THEME_KEY, theme);

  if (themeBtn) {
    themeBtn.textContent = theme === "light" ? "☀️ Theme" : "🌙 Theme";
  }
}

function initTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  if (saved === "light" || saved === "dark") {
    applyTheme(saved);
  } else {
    applyTheme("dark");
  }
}

/* -----------------------------
   ✅ History (last 10 results)
-------------------------------- */
function getHistory() {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
  } catch {
    return [];
  }
}

function setHistory(items) {
  localStorage.setItem(HISTORY_KEY, JSON.stringify(items.slice(0, 10)));
}

function addHistoryItem(item) {
  const prev = getHistory();
  const next = [item, ...prev].slice(0, 10);
  setHistory(next);
  renderHistory();
}

function renderHistory() {
  if (!historyList) return;

  const items = getHistory();
  if (!items.length) {
    historyList.textContent = "No history yet.";
    return;
  }

  historyList.innerHTML = items
    .map((x) => {
      const pct = (x.probability * 100).toFixed(2);
      const when = new Date(x.ts).toLocaleString();
      return `
        <div class="h-item">
          <div class="h-left">
            <div><b>${x.label}</b></div>
            <div class="kbd">${when}</div>
          </div>
          <div class="h-right">${pct}%</div>
        </div>
      `;
    })
    .join("");
}

/* -----------------------------
   Form submit -> Predict
-------------------------------- */
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = Object.fromEntries(new FormData(form).entries());
  for (const k of Object.keys(data)) data[k] = Number(data[k]);

  setLoading(true);

  try {
    const res = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`API error ${res.status}\n${txt}`);
    }

    const out = await res.json();
    renderResult(out.prediction, out.probability, out.label);

    // ✅ Save into history
    addHistoryItem({
      ts: Date.now(),
      prediction: out.prediction,
      probability: out.probability,
      label: out.label,
      inputs: data,
    });
  } catch (err) {
    renderError(err.message || "Unknown error");
  } finally {
    setLoading(false);
  }
});

resetBtn.addEventListener("click", () => {
  form.reset();
  renderEmpty();
});

/* -----------------------------
   Button handlers
-------------------------------- */
if (themeBtn) {
  themeBtn.addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") || "dark";
    applyTheme(cur === "dark" ? "light" : "dark");
  });
}

if (clearHistoryBtn) {
  clearHistoryBtn.addEventListener("click", () => {
    localStorage.removeItem(HISTORY_KEY);
    renderHistory();
  });
}

/* -----------------------------
   Init
-------------------------------- */
renderEmpty();
renderHistory();
initTheme();
checkHealth();
setInterval(checkHealth, 10000);
