const API_URL = "http://localhost:8000/predict";

const sampleSelect = document.getElementById("sample");
const input = document.getElementById("input");
const runBtn = document.getElementById("run");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");

sampleSelect.addEventListener("change", () => {
  if (sampleSelect.value) input.value = sampleSelect.value;
});

const accentFor = (label) => {
  if (label.includes("PER")) return "var(--per)";
  if (label.includes("LOC")) return "var(--loc)";
  if (label.includes("ORG")) return "var(--org)";
  return "var(--muted)";
};

function renderEntities(text, entities) {
  if (!entities.length) {
    resultEl.innerHTML = `<div class="sentence">${escapeHtml(text)}</div><p class="placeholder text-muted" style="margin-top:10px;">No entities found in this sentence.</p>`;
    return;
  }
  entities.sort((a, b) => a.start - b.start);
  let html = "";
  let cursor = 0;
  for (const e of entities) {
    html += escapeHtml(text.slice(cursor, e.start));
    const accent = accentFor(e.label);
    html += `<span class="gloss" style="--accent:${accent}">
                <span class="gloss-text">${escapeHtml(text.slice(e.start, e.end))}</span>
                <span class="gloss-tag">${escapeHtml(e.label)}</span>
            </span>`;
    cursor = e.end;
  }
  html += escapeHtml(text.slice(cursor));
  resultEl.innerHTML = `<div class="sentence">${html}</div>`;
}

function escapeHtml(str) {
  return str.replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}

async function runPrediction() {
  const text = input.value.trim();
  if (!text) {
    statusEl.textContent = "Please enter a sentence first";
    return;
  }
  runBtn.disabled = true;
  statusEl.textContent = "Analyzing...";
  resultEl.innerHTML = "";

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!res.ok) throw new Error(`Server returned error ${res.status}`);
    const data = await res.json();
    renderEntities(data.text, data.entities);
    statusEl.textContent = `Done · ${data.entities.length} entities`;
  } catch (err) {
    resultEl.innerHTML = `<div class="error-box">Could not reach the backend at ${API_URL}.<br>Make sure you've run <code>uvicorn backend:app --port 8000</code>.<br><span style="opacity:0.7">${escapeHtml(err.message)}</span></div>`;
    statusEl.textContent = "Error";
  } finally {
    runBtn.disabled = false;
  }
}

runBtn.addEventListener("click", runPrediction);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) runPrediction();
});