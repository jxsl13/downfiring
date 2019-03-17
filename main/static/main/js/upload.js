$('#ufr-file').on('change',function(){
	// splits the fake file path and returns the file name
    var fileName = $(this).val().split(/[\\/]/).pop();

    $('#ufr-file-label').text(fileName);
})