let trendChart = null;
let linesChart = null;

// Función para dar formato de miles a los números (ej. 1000000 -> 1,000,000)
const formatNumber = (num) => new Intl.NumberFormat("en-US").format(num);

async function loadDashboard(from = "", to = "") {
  try {
    // Construir los parámetros de fecha para la URL
    const params = new URLSearchParams();
    if (from) params.append("desde", from);
    if (to) params.append("hasta", to);
    const queryString = params.toString() ? `?${params.toString()}` : "";

    // BUENA PRÁCTICA: Hacer las 3 peticiones al mismo tiempo
    const [kpisRes, trendRes, linesRes] = await Promise.all([
      fetch(`/api/kpis${queryString}`),
      fetch(`/api/trend${queryString}`),
      fetch(`/api/lines${queryString}`),
    ]);

    const kpis = await kpisRes.json();
    const trendData = await trendRes.json();
    const linesData = await linesRes.json();

    updateKPIs(kpis);
    renderTrendChart(trendData);
    renderLinesChart(linesData);
  } catch (error) {
    console.error("Error cargando los datos del dashboard:", error);
  }
}

function updateKPIs(data) {
  if (!data || Object.keys(data).length === 0) return;

  document.getElementById("kpi-total").textContent = formatNumber(
    data.total_afluencia,
  );
  document.getElementById("kpi-avg").textContent = formatNumber(
    data.promedio_diario,
  );
  document.getElementById("kpi-station").textContent = data.estacion_top;
  document.getElementById("kpi-line").textContent = data.linea_top;
}

function renderTrendChart(data) {
  const labels = data.map((d) => d.fecha);
  const values = data.map((d) => d.afluencia);

  if (trendChart) trendChart.destroy();
  const ctx = document.getElementById("chart-trend").getContext("2d");

  const gradient = ctx.createLinearGradient(0, 0, 0, 300);
  gradient.addColorStop(0, "rgba(255, 154, 68, 0.4)");
  gradient.addColorStop(1, "rgba(252, 96, 118, 0.0)");

  trendChart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Usuarios Totales",
          data: values,
          borderColor: "#ff9a44",
          backgroundColor: gradient,
          borderWidth: 2.5,
          pointRadius: 2,
          pointBackgroundColor: "#fc6076",
          fill: true,
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { intersect: false, mode: "index" },
      plugins: { legend: { display: false } },
      scales: {
        x: {
          ticks: { color: "#8e8ea0" },
          grid: { color: "rgba(255,255,255,0.04)" },
        },
        y: {
          ticks: { color: "#8e8ea0", callback: (v) => formatNumber(v) },
          grid: { color: "rgba(255,255,255,0.06)" },
        },
      },
    },
  });
}

function renderLinesChart(data) {
  // Tomamos solo las 10 líneas con más gente para no saturar la gráfica
  const topLines = data.slice(0, 10);
  const labels = topLines.map((d) => d.linea);
  const values = topLines.map((d) => d.afluencia);

  if (linesChart) linesChart.destroy();
  const ctx = document.getElementById("chart-lines").getContext("2d");

  linesChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Afluencia",
          data: values,
          backgroundColor: "rgba(252, 96, 118, 0.8)",
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: {
          ticks: { color: "#8e8ea0", font: { size: 10 } },
          grid: { display: false },
        },
        y: {
          ticks: { color: "#8e8ea0", callback: (v) => formatNumber(v) },
          grid: { color: "rgba(255,255,255,0.06)" },
        },
      },
    },
  });
}

function applyFilters() {
  const from = document.getElementById("date-from").value;
  const to = document.getElementById("date-to").value;
  loadDashboard(from, to);
}

function resetFilters() {
  document.getElementById("date-from").value = "";
  document.getElementById("date-to").value = "";
  loadDashboard();
}

// Carga inicial
loadDashboard();
