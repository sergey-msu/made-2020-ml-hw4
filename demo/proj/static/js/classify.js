function classify() {
    $('#btn-analysis-id').hide();
    $('#wait-block-id').show();

    var fd = new FormData();
    var files = $('#img-file-id')[0].files[0];
    fd.append('img', files);

    $.ajax({
        url: '/classify_ajax',
        type: 'post',
        data: fd,
        contentType: false,
        processData: false,
        success: function(response){
            result = response['result'];
            createDiseaseResult(result);
        },
        error: function(response){
            createErrorResult(response);
        },
        complete: function(response){
            $('#wait-block-id').hide();
        }
    });
}

function createErrorResult(response){
    var resultsDiv = $('#results-block-id');

    var innerHtml =`
          <div id="diseases-result-id">
            <p class="text-danger"><b>Ошибка на сервере</b></p>
          </div>`;

    resultsDiv.html(innerHtml);
    resultsDiv.show();
}

function createDiseaseResult(result){
    var resultsDiv = $('#results-block-id');
    var diseases = result['diseases'];
    var details = result['details'];

    var innerHtml = '<div id="diseases-result-id">';
    if (diseases.length == 0) {
        innerHtml += '<p class="made-welcome-text"><b>Болезни не выявлены</b></p>';
    }
    else {
        innerHtml += '<p class="made-diseases-detected">Выявлены болезни:';
        for (var i in diseases) {
            var disease = diseases[i];
            innerHtml += '<br><span class="text-danger"><b>' + disease + '</b></span>';
        }
        innerHtml += '</p>';
        innerHtml += '<a href="javascript:displayDetails(true);">подробнее</a>';
    }
    innerHtml += '</div>';

    innerHtml += '<div id="diseases-details-id">';
    innerHtml += '<table class="made-details-table">';
    for (var class_name in details) {
        var pct = Math.round(100*details[class_name]);
        var disease_class = ((pct >= 80) ? 'text-danger' : '');
        innerHtml += '<tr class="' + disease_class + '">';
        innerHtml += '<td class="made-disease-td">' + class_name + '</td>';
        innerHtml += '<td class="made-disease-pct-td">' + pct + '%</td>';
        innerHtml += '</tr>';
    }
    innerHtml += '</table>';

    innerHtml += '<a href="javascript:displayDetails(false);">скрыть</a>';
    innerHtml += '</div>';

    resultsDiv.html(innerHtml);
    resultsDiv.show();
}

function readImageURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('#img-preview-id').attr('src', e.target.result);
            $('#btn-analysis-id').show();
            $('#results-block-id').hide();
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function displayDetails(display) {
    resultDiv = $('#diseases-result-id');
    detailsDiv = $('#diseases-details-id');

    if (display) {
        resultDiv.hide();
        detailsDiv.show();
    }
    else{
        resultDiv.show();
        detailsDiv.hide();
    }
}
