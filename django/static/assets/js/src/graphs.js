function PartyCharts(rawJson) {
    this.data = JSON.parse(rawJson);
    this.render = function(id, data) {
        return new Chart(document.getElementById(id), {
            type: 'pie',
            data: {
                labels: ["Mulheres", "Homens"],
                datasets: [{
                    label: "Values",
                    backgroundColor: ["#bb84e0","#340056"],
                    data: data
                }]
            },
            options: {
                legend: {
                    display: false
                }
            }
        });
    };

    this.calc = function(pct, size) {
        if (pct == null) pct = 0;
        return [pct * 100, (1 - pct) * 100].map(Math.round);
    };

    this.findBy = function(property, equality) {
        return this.data.find(function(item){
            if (item[property] != undefined) {
                if (equality == undefined) {
                    return item;
                } else if (equality != undefined && item[property] == equality) {
                    return item;
                }
            }
        });
    };

    this.calculate = function(type) {
        switch(type) {
            case 'party':
                return this.calc(this.findBy('initials').women_pct);
                break;
            case 'state':
                return this.calc(this.findBy('job_role_name', 'Deputado Estadual').women_pct);
                break;
            case 'federal':
                return this.calc(this.findBy('job_role_name', 'Deputado Federal').women_pct);
                break;
            case 'pass':
                return this.calc(this.findBy('money_women_pct').women_pct);
                break;
        }
    };

    this.render("candidates_party", this.calculate('party'));
    // this.render("candidates_coalition", [0.31, 0, 0.69]);
    this.render("candidates_state", this.calculate('state'));
    this.render("candidates_federal", this.calculate('federal'));
    this.render("candidates_pass", this.calculate('pass'));
}
