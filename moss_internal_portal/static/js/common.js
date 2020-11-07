$('#id-check-all').on('change', function (e) {
    var checked = $(this).is(':checked');
    $('.row-checkbox').prop('checked', checked);
})