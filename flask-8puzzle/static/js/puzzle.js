let state = [];
let solution = [];
let step = 0;
let startTime = null;

function drawPuzzle() {
  const container = document.getElementById("puzzle-container");
  container.innerHTML = "";
  state.forEach(num => {
    const tile = document.createElement("div");
    tile.className = "tile" + (num === 0 ? " zero" : "");
    tile.textContent = num !== 0 ? num : "";
    container.appendChild(tile);
  });
}

function generatePuzzle() {
  fetch("/generate")
    .then(res => res.json())
    .then(data => {
      state = data.state;
      solution = [];
      step = 0;
      startTime = null;
      drawPuzzle();
      updateInfo();
    });
}

function solvePuzzle() {
  fetch("/solve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ state: state })
  })
    .then(res => res.json())
    .then(data => {
      solution = data.solution;
      step = 0;
      startTime = performance.now();
      alert("Solution found! Press ➡️ Next to step through.");
    });
}

function updateInfo() {
  const timeElapsed = startTime ? ((performance.now() - startTime) / 1000).toFixed(1) : "0.0";
  document.getElementById("info").textContent = `Step: ${step} | Time: ${timeElapsed}s`;
}

function nextStep() {
  if (step < solution.length) {
    state = applyMove(state, solution[step]);
    step++;
    drawPuzzle();
    updateInfo();
  } else if (step === solution.length && solution.length > 0) {
    alert("✅ Puzzle Solved!");
    step++;
  }
}

function applyMove(state, move) {
  const moves = { left: -1, right: 1, up: -3, down: 3 };
  const zeroIndex = state.indexOf(0);
  const newIndex = zeroIndex + moves[move];
  const newState = [...state];
  [newState[zeroIndex], newState[newIndex]] = [newState[newIndex], newState[zeroIndex]];
  return newState;
}

// Auto-generate on load
window.onload = generatePuzzle;