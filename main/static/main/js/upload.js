function fileName(str)
{
   var base = str.split('/');
   base = base[base.length - 1];
   base = base.split('\\');
   base = base[base.length - 1];
   return base;
}


$('#ufr-file').on('change',function(){
    var fileName = $(this).val();
    $('#ufr-file-label').text(fileName(fileName))
})