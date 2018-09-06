function CandidateHandler($, host) {

    this.init = function() {

        var selects = [
            {
                name: 'estado',
                path: '/api/states/'
            },
            {
                name: 'partido',
                path: '/api/parties/'
            },
            {
                name: 'cargo',
                path: '/api/job_roles'
            }
        ];

        selects.map(function(select) {
            this.fetchSelectData(host + select.path, select.name);
        });

        selects.map(function(select) {
            this.onSelectRefresh(select.name, '/api/candidates', selects);
        });

        this.registerLoadMoreCandidates(host + '/api/candidates', selects);
    };

    this.registerLoadMoreCandidates = function(host, selects) {
        this.$("#loadMoreCandidates").on('click', function (e) {
            e.preventDefault();
            this.fetchCandidates(host, selects);
        }.bind(this));
    };

    this.logError = function(xhr, err) {
        console.error(err);
    };

    this.fetchSelectData = function(url, id) {
        this.$.ajax({
            mode: 'cors',
            url: url,
            success: function(result) {
                console.log(result);
                this.fullfill(id, result);
            }.bind(this),
            error: function(xhr, opt, err) {
                this.logError(xhr, err);
            }.bind(this)
        });
    };

    this.setInfinityScroll = function(id, host, selects) {
        $(window).scroll(function() {
            if ($(window).scrollTop() >= $(document).height() - $(window).height() - 1000) {
                if (!this.waitingFetchCandidates) {
                    this.waitingFetchCandidates = true;
                    this.fetchCandidates(host, selects, this.page);
                }
            }
        });
    };

    this.fullfill = function(id, data) {
        var length = data.length;
        var picker = this.$('#'+id);
        for (var i = 0; i < length; i++) {
            var d = data[i];
            var option = this.$('<option>', {
                value: d.value,
                text: d.name
            });
            picker.append(option);
        }
    };

    this.readSelectStates = function(selects){
        var query = {};
        selects.map(function(select) {
            var value = this.$('#' + select.name).val();
            if (value != undefined && value.length > 0) {
                query[select.name] = value;
            }
        });
        return query;
    };

    this.fetchCandidates = function(host, selects) {
        var query = this.readSelectStates(selects);
        query['page'] = this.page + 1;

        console.log(query);

        var url = host + '?' +  this.$.param(query);
        console.log(url);
        this.$.ajax({
            url: url,
            success: function(result) {
                this.displayCandidates(result);
                this.page += 1;
                this.waitingFetchCandidates = false;
            }.bind(this),
            error: function(xhr, opt, err) {
                this.logError(xhr, err);
            }.bind(this)
        });
    };

    this.getStatusImg = function(status) {
        var img = '';

        console.log(`status: ${status}`);
        if (status === 'P') {
            img = '/static/img/pending.png';
        } else if (status == 'A') {
            img = '/static/img/approved.svg';
        } else if (status == 'D') {
            img = '/static/img/alert.svg';
        } else {
            img = '/static/img/empty.svg';
        }

        return img;
    };


    this.buildCandidateUI = function(id, name, description, candidateImg, partyImg, status) {
        var media = this.$('<div>', {class: 'media border'});

        // image
        media.append(this.$('<img>', {
            class: 'border picture',
            src: candidateImg,
            alt: name
        }));

        var mediaBody = this.$('<div>', {
            class:'col-5 col-md-8 align-center',
            text: description
        });
        media.append(mediaBody);

        mediaBody.append(this.$('<h5>', {class: 'align-text-bottom', text: name}));

        // party
        var partyDiv = this.$('<div>', {class: 'col-3 col-md-2 align-center'});
        partyDiv.append(this.$('<img>', {
            src: partyImg,
            class: 'brand img-fluid',
            alt: 'imagem do partido'
        }));
        media.append(partyDiv);

        this.$('#' + id).append(media);

        // candidature status
        var statusDiv = this.$('<div>', {class: 'col-1 align-center'});
        statusDiv.append(this.$('<img>', {
            src: this.getStatusImg(status),
            class: 'icon',
            alt: status
        }));
        media.append(statusDiv);
    };

    this.onSelectRefresh = function(id, host, selects) {
        this.$('#'+id).change(function() {
            this.page = 1;
            this.clearCandidates();
            this.fetchCandidates(host, selects);
        }.bind(this));
    };

    this.clearCandidates = function() {
        this.$('#candidates-list').empty();
    };

    this.getCandidateStatus = function(candidate) {
        return candidate.status;
    };

    this.getCandidateName = function(candidate) {
        return candidate.name;
    };

    this.getCandidateDescription = function(candidate) {
        return candidate.description;
    };

    this.getCandidateImg = function(candidate) {
        return candidate.picture_url;
    };

    this.getPartyImg = function(candidate) {
        var p = candidate.political_party_initials.toLowerCase().replace(/ /g, '');
        var path = `/static/img/partidos/${p}.png`;
        console.log(p);
        return path;
    };

    this.displayCandidates = function(result) {
        console.log(result);

        result.map(function(candidate) {

            var name = this.getCandidateName(candidate);
            var description = this.getCandidateDescription(candidate);
            var partyImg = this.getPartyImg(candidate);
            var img = this.getCandidateImg(candidate);
            var status = this.getCandidateStatus(candidate);

            this.buildCandidateUI(
                'candidates-list',
                name,
                description,
                img,
                partyImg,
                status
            );

        }.bind(this));

        this.$(".load_more_candidates").show();
    };

    this.$ = $;
    this.page = 0;
    this.waitingFetchCandidates = false;
    this.init();
}


// load partidos
$.getJSON("/api/parties/", function (response) {
    response.map(getPartyDetails).forEach(showStore);
});

// load view
function getPartyDetails(partyInfo) {
    return '<div class="item-party">' +
            '<div class="row mb-4 justify-content-center">' +
        '<div class="col-4 text-center">' +
        '<a href="/parties/' + partyInfo.initials.toUpperCase() + '">' +
          '<img src="/static/img/partidos/'+partyInfo.initials.toLowerCase()+'.png" class="img-fluid gray" alt="'+partyInfo.name+'" />' +
           '</a>' +
              '</div>' +
            '</div>'+

            '<div class="row">' +
              '<div class="col-1 mt-1 p-1">' +
                '<img src="/static/img/icon_person.png" class="img-fluid" alt="Person" />' +
              '</div>'+
              '<div class="col-11">'+
                '<div class="arrow-progress">'+
                  '<div class="arrow-bar" role="progressbar" style="width: 30%" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100"></div>' +
                '</div>' +
                '<div class="progress">' +
                  '<div class="progress-bar" role="progressbar" style="width: '+100*partyInfo.women_pct+'%" aria-valuenow="'+partyInfo.women_pct+'" aria-valuemin="0" aria-valuemax="100"></div>' +
                '</div>' +
              '</div>' +
            '</div>' +

            '<hr>' +

            '<div class="row">' +
              '<div class="col-1 mt-1 p-1">' +
                '<img src="/static/img/icon_money.png" class="img-fluid" alt="Money" />' +
              '</div>' +
              '<div class="col-11">' +
                '<div class="arrow-progress">' +
                  '<div class="arrow-bar" role="progressbar" style="width: 30%" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100"></div>' +
                '</div>' +
                '<div class="progress">' +
                  '<div class="progress-bar" role="progressbar" style="width: '+ 100 * partyInfo.money_women_pct + '%" aria-valuenow="' + partyInfo.money_women_pct + '" aria-valuemin="0" aria-valuemax="100"></div>' +
                '</div>' +
              '</div>' +
            '</div>' +

            '<hr>'+
            '</div>';
}
function showStore(partyDetails) {
    document.querySelector(".stores").innerHTML += partyDetails;
}
// partyInfo.map(getPartyDetails).forEach(showStore);

// carrega mais partidos
$(function () {
    $(".item-party").slice(0, 4).show();
    $("#loadMore").on('click', function (e) {
        e.preventDefault();
        $(".item-party:hidden").slice(0, 4).slideDown();
        if ($(".item-party:hidden").length == 0) {
            $("#loadMore").fadeOut('slow');
        };
    });
});
