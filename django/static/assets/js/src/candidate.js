function CandidateHandler($, host) {

    this.init = function() {

        let selects = [
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

        this.setInfinityScroll('#candidates-list', '/api/candidates', selects);
        // this.fetchCandidates(host + '/api/candidates', selects);
    };

    this.logError = function(xhr, err) {
        // console.log(xhr.responseText);
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
        let length = data.length;
        let picker = this.$('#'+id);
        for (let i = 0; i < length; i++) {
            let d = data[i];
            let option = this.$('<option>', {
                value: d.value,
                text: d.name
            });
            picker.append(option);
        }
    };

    this.readSelectStates = function(selects){
        let query = {};
        selects.map(function(select) {
            let value = this.$('#' + select.name).val();
            if (value != undefined && value.length > 0) {
                query[select.name] = value;
            }
        });
        return query;
    };

    this.fetchCandidates = function(host, selects, page) {
        let query = this.readSelectStates(selects);
        query['page'] = page;

        console.log(query);

        let url = host + '?' +  this.$.param(query);
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
        let img = '';

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
        let media = this.$('<div>', {class: 'media border'});

        // image
        media.append(this.$('<img>', {
            class: 'border picture',
            src: candidateImg,
            alt: name
        }));
        
        let mediaBody = this.$('<div>', {
            class:'col-5 col-md-8 align-center',
            text: description
        });
        media.append(mediaBody);
        
        mediaBody.append(this.$('<h5>', {class: 'align-text-bottom', text: name}));

        // party
        let partyDiv = this.$('<div>', {class: 'col-3 col-md-2 align-center'});
        partyDiv.append(this.$('<img>', {
            src: partyImg,
            class: 'brand',
            alt: 'imagem do partido'
        }));
        media.append(partyDiv);

        this.$('#' + id).append(media);

        // candidature status
        let statusDiv = this.$('<div>', {class: 'col-1 align-center'});
        statusDiv.append(this.$('<img>', {
            src: this.getStatusImg(status),
            class: 'icon',
            alt: 'Candidatura Ok'
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
        let p = candidate.political_party_initials.toLowerCase().replace(/ /g, '');
        let path = `/static/img/partidos/${p}.png`;
        console.log(path);
        return path;
    };

    this.displayCandidates = function(result) {
        console.log(result);

        result.map(function(candidate) {

            let name = this.getCandidateName(candidate);
            let description = this.getCandidateDescription(candidate);
            let partyImg = this.getPartyImg(candidate);
            let img = this.getCandidateImg(candidate);
            let status = this.getCandidateStatus(candidate);

            this.buildCandidateUI(
                'candidates-list',
                name,
                description,
                img,
                partyImg,
                status
            );

        }.bind(this));
    };

    this.$ = $;
    this.page = 1;
    this.waitingFetchCandidates = false;
    this.init();
}
