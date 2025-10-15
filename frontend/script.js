// --- Step 1: Handle Get Started Screen ---
document.getElementById("startBtn").addEventListener("click", () => {
  const selected = document.querySelector('input[name="checkFor"]:checked');
  if (!selected) {
    alert("Please select who this symptom check is for.");
    return;
  }

  // Transition to symptom checker screen
  document.getElementById("startScreen").classList.add("hidden");
  document.getElementById("symptomScreen").classList.remove("hidden");
});

// --- Step 2: Handle Symptom Analysis ---
document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const symptoms = document.getElementById("symptoms").value.trim();
  const resultDiv = document.getElementById("result");
  const conditionsBox = document.getElementById("conditionsBox");
  const stepsBox = document.getElementById("stepsBox");
  const disclaimerBox = document.getElementById("disclaimerBox");

  resultDiv.classList.add("hidden");
  conditionsBox.classList.add("hidden");
  stepsBox.classList.add("hidden");
  disclaimerBox.classList.add("hidden");

  if (!symptoms) {
    alert("Please enter your symptoms.");
    return;
  }

  resultDiv.innerHTML = `
    <div class="loader"></div>
    <p><em>Analyzing your symptoms...</em></p>
  `;
  resultDiv.classList.remove("hidden");

  const response = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ symptoms }),
  });

  const data = await response.json();

  if (!data.analysis) {
    resultDiv.innerText = "Error: " + (data.error || "Unknown error");
    return;
  }

  let analysis = data.analysis.replace(/\*\*/g, "").replace(/\*/g, "");

  const conditionsMatch = analysis.match(/Possible Conditions[\s\S]*?(?=Next Steps|Disclaimer|$)/i);
  const stepsMatch = analysis.match(/Next Steps[\s\S]*?(?=Disclaimer|$)/i);
  const disclaimerMatch = analysis.match(/Disclaimer[\s\S]*/i);

  if (conditionsMatch) {
    conditionsBox.innerHTML = `<strong>Possible Conditions</strong><br>${conditionsMatch[0]
      .replace(/Possible Conditions[:]?/i, "")
      .trim()}`;
    conditionsBox.classList.remove("hidden");
  }

  if (stepsMatch) {
    stepsBox.innerHTML = `<strong>Next Steps</strong><br>${stepsMatch[0]
      .replace(/Next Steps[:]?/i, "")
      .trim()}`;
    stepsBox.classList.remove("hidden");
  }

  if (disclaimerMatch) {
    disclaimerBox.innerHTML = `<strong>Disclaimer</strong><br>${disclaimerMatch[0]
      .replace(/Disclaimer[:]?/i, "")
      .trim()}`;
    disclaimerBox.classList.remove("hidden");
  }

  const subheadingRegex =
    /(Self[- ]?Care Measures:|When to See a Doctor.*?:|When to Seek Immediate Medical Attention.*?:|When to Seek Medical Help.*?:|When to Seek.*?:|Emergency.*?:|Doctor Visit Recommendations.*?:)/gi;

  document.querySelectorAll(".output-box").forEach((box) => {
    box.innerHTML = box.innerHTML.replace(subheadingRegex, "<strong>$1</strong>");
  });

  resultDiv.classList.add("hidden");
});
