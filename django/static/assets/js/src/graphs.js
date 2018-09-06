window.charts = {
    candidates_party: new Chart(document.getElementById("candidates_party"), {
        type: 'pie',
        data: {
            labels: ["Mulheres", "Homens", "Mínimo Exigido"],
            datasets: [{
                label: "Values",
                backgroundColor: ["#bb84e0", "#340056","#fba919"],
                data: [0.27, 0.7, 0.03]
            }]
        },
        options: {
            legend: {
                display: false
            }
        }
    }),
    candidates_coalition: new Chart(document.getElementById("candidates_coalition"), {
        type: 'pie',
        data: {
            labels: ["Mulheres", "Homens", "Mínimo Exigido"],
            datasets: [{
                label: "Values",
                backgroundColor: ["#bb84e0", "#340056","#fba919"],
                data: [0.31, 0, 0.69]
            }]
        },
        options: {
            legend: {
                display: false
            }
        }
    }),
    candidates_state: new Chart(document.getElementById("candidates_state"), {
        type: 'pie',
        data: {
            labels: ["Mulheres", "Homens", "Mínimo Exigido"],
            datasets: [{
                label: "Values",
                backgroundColor: ["#bb84e0", "#340056","#fba919"],
                data: [0.29, 0.7, 0.01]
            }]
        },
        options: {
            legend: {
                display: false
            }
        }
    }),
    candidates_federal: new Chart(document.getElementById("candidates_federal"), {
        type: 'pie',
        data: {
            labels: ["Mulheres", "Homens", "Mínimo Exigido"],
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
    }),
    candidates_pass: new Chart(document.getElementById("candidates_pass"), {
        type: 'pie',
        data: {
            labels: ["Mulheres", "Homens", "Mínimo Exigido"],
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
    })
};
