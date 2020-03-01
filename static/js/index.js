CAPTURE_IMG_WIDTH = 640
CAPTURE_IMG_HEIGHT = 480

jQuery.ajaxSetup({
  beforeSend: function() {
     $('#loading').removeClass('hidden');
  },
  complete: function(){
     $('#loading').addClass('hidden');
  },
  success: function() {
    $('#loading').addClass('hidden');
  }
});

// HTML5 WEBCAM
Webcam.set({
  width: CAPTURE_IMG_WIDTH,
  height: CAPTURE_IMG_HEIGHT,
  image_format: 'jpeg',
  jpeg_quality: 90
});
Webcam.attach( '#my-camera' );

let form_capture = document.getElementById('form-capture-image')
$('.btn-capture-image').on('click', function(e) {
  e.preventDefault();

  Webcam.snap(function(data_uri) {
    // display results in page
    // readURL(data_uri, '#input-data-uri')
    let json_data = {'data-uri': data_uri }

    $.ajax({
      type: 'POST',
      url: '/predict/',
      processData: false,
      contentType: 'application/json; charset=utf-8',
      dataType: 'json',
      data: JSON.stringify(json_data),
      success: function(data) {
        console.log(data)
        $(".class-result-1").text('Grapheme root : ' + data.root);
        $(".class-result-2").text('Vowel diacritic : ' + data.vowel);
        $(".class-result-3").text('Consonant diacritic : ' + data.consonant);

        // $('.box-main').css('height', $('.box-results').height());
      }
    });
  });
});