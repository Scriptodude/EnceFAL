$(document).ready(function() {
    actualiserTotal = function () {

        total = 0;
        $('#total').text('0');
        var prix_regex = /id_exemplaires-(?:\d+)-prix/;

        prix = $('input').filter(function(){
            return prix_regex.test(this.id);
        });

        prix.each(function () {

            if ($(this).val()){
                total = $('#total');
                nouveau = (parseFloat(total.text()) + parseFloat($(this).val())).toFixed(2);
                total.text(nouveau);
            }

        });

    };

    actualiserTotal();
    
    prix = $('input').filter(function(){
        return /id_exemplaires-(?:\d+)-prix/.test(this.id);
    }).change(actualiserTotal);

    $('#id_code_permanent').change(function () {

        code = $('#id_code_permanent').val();
        if (code.length == 0){
            return;
        } 

        url = "/vendeur/?code=" + code;
        $.get(url, function(response, status){
            if (status == "success"){

                $('#id_prenom').val(response.prenom);
                $('#id_email').val(response.email);
                $('#id_nom').val(response.nom);
                $('#id_telephone').val(response.telephone);

            }
        });


    });
    
    get_exemplaire = function (event) {

        var identifiant_regex = /id_exemplaires-(\d+)-identifiant/;
        nb = identifiant_regex.exec(event.target.id);
        nb = nb[1];

        identifiant = $('#' + event.target.id).val();
        if (identifiant.length == 0){
            $('#id_exemplaires-' + nb + '-titre').val('');
            $('#id_exemplaires-' + nb + '-auteur').val('');
            $('#id_exemplaires-' + nb + '-isbn').val('');
            $('#id_exemplaires-' + nb + '-prix').val('');
            $('#id_exemplaires-' + nb + '-prix').attr('readonly',false);
            actualiserTotal();
            return;
        } 

        url = "/exemplaire/?identifiant=" + identifiant + '&nb=' + this.nb;
        $.get(url, function(response, status){
            if (status == "success"){
                if (response.status === "ok"){

                    $('#id_exemplaires-' + response.nb + '-titre').val(response.titre);
                    $('#id_exemplaires-' + response.nb + '-auteur').val(response.auteur);
                    $('#id_exemplaires-' + response.nb + '-isbn').val(response.isbn);
                    $('#id_exemplaires-' + response.nb + '-prix').val(response.prix);
                    $('#id_exemplaires-' + response.nb + '-prix').attr('readonly',true);
                    actualiserTotal();

                } else {

                    alert("Impossible de trouver l'exemplaire, se référer aux 'exemplaires disponibles'");
                }

            }

        });

    }

    get_isbn = function (event) {

        var isbn_regex = /id_exemplaires-(\d+)-isbn/;
        nb = isbn_regex.exec(event.target.id);
        nb = nb[1];

        code = $('#' + event.target.id).val();
        if (code.length == 0){
            $('#id_exemplaires-' + nb + '-titre').val('');
            $('#id_exemplaires-' + nb + '-auteur').val('');
            $('#id_exemplaires-' + nb + '-prix').val('');
        } 

        if (code.length !== 10 && code.length !== 13){
            return;
        }

        url = "/livre/?isbn=" + code + '&nb=' + this.nb;
        $.get(url, function(response, status){
            if (status == "success"){

                $('#id_exemplaires-' + response.nb + '-titre').val(response.titre);
                $('#id_exemplaires-' + response.nb + '-auteur').val(response.auteur);
                $('#id_exemplaires-' + response.nb + '-prix').focus();

            }

        });

    }



})
