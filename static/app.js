async function fetchJSON(url, options = {}) {
  const res = await fetch(url, options);
  return await res.json();
}

function renderObservation(obs) {
  if (!obs) {
    document.getElementById("post").innerText = "No more cases in this session.";
    document.getElementById("context").innerText = "-";
    document.getElementById("user_history").innerText = "-";
    return;
  }

  document.getElementById("post").innerText = obs.post;
  document.getElementById("context").innerText = obs.context;
  document.getElementById("user_history").innerText = obs.user_history;
}

function renderState(state) {
  const stats = state.stats;
  document.getElementById("avg_score").innerText = stats.average_score.toFixed(3);
  document.getElementById("total_cases").innerText = stats.total_cases;
  document.getElementById("completed_cases").innerText = stats.completed_cases;
  document.getElementById("count_allow").innerText = stats.decisions.allow;
  document.getElementById("count_flag").innerText = stats.decisions.flag;
  document.getElementById("count_remove").innerText = stats.decisions.remove;
  document.getElementById("count_escalate").innerText = stats.decisions.escalate;

  const historyBox = document.getElementById("history");
  historyBox.innerHTML = "";

  const items = state.history.slice().reverse();
  if (items.length === 0) {
    historyBox.innerHTML = '<div class="muted">No actions yet.</div>';
    return;
  }

  items.forEach(item => {
    const div = document.createElement("div");
    div.className = "history-item";
    div.innerHTML = `
      <span class="pill">Case ${item.item_id}</span>
      <span class="pill">${item.decision}</span>
      score: <strong>${item.score}</strong>
    `;
    historyBox.appendChild(div);
  });
}

function renderReward(reward) {
  document.getElementById("last_score").innerText = reward.score.toFixed(3);
  document.getElementById("feedback").innerText = reward.feedback;

  const breakdown = reward.breakdown || {};
  document.getElementById("breakdown").innerHTML = `
    <div class="muted">Decision: ${breakdown.decision_score ?? 0}</div>
    <div class="muted">Reasoning: ${breakdown.reasoning_score ?? 0}</div>
    <div class="muted">Policy: ${breakdown.policy_score ?? 0}</div>
    <div class="muted">Rewrite: ${breakdown.rewrite_score ?? 0}</div>
    <div class="muted">Supervisor penalty: ${breakdown.supervisor_penalty ?? 0}</div>
  `;
}

async function refreshState() {
  const state = await fetchJSON("/state");
  renderState(state);
}

async function resetEnv() {
  const obs = await fetchJSON("/reset");
  renderObservation(obs);
  document.getElementById("last_score").innerText = "-";
  document.getElementById("feedback").innerText = "Session reset.";
  document.getElementById("breakdown").innerHTML = "";
  document.getElementById("reasoning").value = "";
  document.getElementById("rewrite").value = "";
  await refreshState();
}

async function changeLevel() {
  const level = document.getElementById("level").value;
  const obs = await fetchJSON("/set_level", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ level })
  });
  renderObservation(obs);
  document.getElementById("last_score").innerText = "-";
  document.getElementById("feedback").innerText = `Difficulty changed to ${level}.`;
  document.getElementById("breakdown").innerHTML = "";
  document.getElementById("reasoning").value = "";
  document.getElementById("rewrite").value = "";
  await refreshState();
}

async function sendAction(decision) {
  const reasoning = document.getElementById("reasoning").value.trim();
  const rewrite = document.getElementById("rewrite").value.trim();

  const payload = {
    decision,
    reasoning,
    rewrite: rewrite || null
  };

  const result = await fetchJSON("/step", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });

  renderReward(result.reward);
  renderObservation(result.observation);
  await refreshState();

  if (result.done) {
    document.getElementById("feedback").innerText += " Session complete.";
  }

  document.getElementById("reasoning").value = "";
  document.getElementById("rewrite").value = "";
}

window.onload = async function () {
  await resetEnv();
};