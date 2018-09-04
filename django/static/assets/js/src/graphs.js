

// candidatas por partido
new Chart(document.getElementById("candidates_party"), {
    type: 'pie',
    data: {
      labels: ["Candidatas", "Partido", "Sei lá"],
      datasets: [{
        label: "Values",
        backgroundColor: ["#bb84e0", "#340056","#fba919"],
        data: [2478,5267,734]
      }]
    },
    options: {
        legend: {
            display: false
        }
    }
});

// candidatas por partido
new Chart(document.getElementById("candidates_coalition"), {
    type: 'pie',
    data: {
      labels: ["Candidatas", "Partido", "Sei lá"],
      datasets: [{
        label: "Values",
        backgroundColor: ["#bb84e0", "#340056","#fba919"],
        data: [2478,5267,734]
      }]
    },
    options: {
        legend: {
            display: false
        }
    }
});

// candidatas por estado
new Chart(document.getElementById("candidates_state"), {
    type: 'pie',
    data: {
      labels: ["Candidatas", "Partido", "Sei lá"],
      datasets: [{
        label: "Values",
        backgroundColor: ["#bb84e0", "#340056","#fba919"],
        data: [2478,5267,734]
      }]
    },
    options: {
        legend: {
            display: false
        }
    }
});

// candidatas federal
new Chart(document.getElementById("candidates_federal"), {
    type: 'pie',
    data: {
      labels: ["Candidatas", "Partido", "Sei lá"],
      datasets: [{
        label: "Values",
        backgroundColor: ["#bb84e0", "#340056","#fba919"],
        data: [2478,5267,734]
      }]
    },
    options: {
        legend: {
            display: false
        }
    }
});

// Repasse de fundo partidário
new Chart(document.getElementById("candidates_pass"), {
    type: 'pie',
    data: {
      labels: ["Candidatas", "Partido", "Sei lá"],
      datasets: [{
        label: "Values",
        backgroundColor: ["#bb84e0", "#340056","#fba919"],
        data: [2478,5267,734]
      }]
    },
    options: {
        legend: {
            display: false
        }
    }
});
