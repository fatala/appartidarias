function CandidateHandler($, host) {
    this.$ = $;
    console.log(this.$);

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

        this.fetchCandidates(host + '/api/candidates', selects);

        console.log('init candidate handler');
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

    this.fetchCandidates = function(host, selects) {
        let query = this.readSelectStates(selects);

        console.log('query');
        console.log(query);
        let url = host + '?' +  this.$.param(query);
        console.log(url);
        this.$.ajax({
            url: url,
            success: function(result) {
                this.displayCandidates(result);
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
    
    this.buildCandidateUI = function(id, name, description, candidateImg, party, status) {
        let media = this.$('<div>', {class: 'media'});

        // image
        media.append(this.$('<img>', {
            class: 'mr-1 col-3 col-md-1',
            src: candidateImg,
            alt: 'nome da candidata'
        }));
        
        let mediaBody = this.$('<div>', {
            class:'media-body col-5 col-md-9',
            text: description
        });
        media.append(mediaBody);
        
        mediaBody.append(this.$('<h5>', {class: 'mt-0', text: name}));
        
        // candidature status
        let statusDiv = this.$('<div>', {class: 'mr-1 col-1'});
        statusDiv.append(this.$('<img>', {
            src: this.getStatusImg(status),
            class: 'icon',
            alt: 'Candidatura Ok'
        }));
        media.append(statusDiv);
        
        // party
        let partyDiv = this.$('<div>', {class: 'col-1'});
        let partyImg = this.$('<img>', {
            src: party,
            class: 'partido',
            alt: 'imagem do partido'
        });
        partyDiv.append(partyImg);
        media.append(partyDiv);

        this.$('#' + id).append(media);   
    };

    this.onSelectRefresh = function(id, host, selects) {
        this.$('#'+id).change(function() {
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
        return candidate.name;
    };

    this.getCandidateImg = function(candidate) {
        return candidate.picture_url;
    };

    this.getPartyImg = function(candidate) {
        return  'img/' + candidate.party + '.jpg';
    };

    this.displayCandidates = function(result) {
        console.log(result);
        this.clearCandidates();

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

    this.init();
    
    console.log('loading candidate.js');
}
