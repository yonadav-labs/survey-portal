var tplAttachment = `
    <div class="card attachment-card border-light border mb-2">
        <div class="card-body">
            <button type="button" class="close close-card new" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
            <div class="form-group float-left">
                <input type="file" name="attachment-file" class="form-control-file" required>
            </div>
            <div class="clearfix"></div>
            <div class="form-group">
                <label for="simpleinput">Description</label>
                <input type="text" name="attachment-desc" class="form-control attachment-desc new">
            </div>
        </div>
    </div>
`

$("body").on("click", "#add-attachment-card", function(e) {
    $('.attachments-wrapper').append(tplAttachment);
})

$("body").on("click", "button.close-card", function(e) {
    if ($(this).hasClass('old')) {
        var idx = $('button.close-card.old').index(this);

        var fileNames = $('#meta_old_files').val().split('@$@');
        fileNames.splice(idx, 1);
        $('#meta_old_files').val(fileNames.join('@$@'));

        var fileDesc = $('#meta_old_desc').val().split('@$@');
        fileDesc.splice(idx, 1);
        $('#meta_old_desc').val(fileDesc.join('@$@'));
    } else {
        var idx = $('button.close-card.new').index(this);

        var fileDesc = $('#meta_new_desc').val().split('@$@');
        fileDesc.splice(idx, 1);
        $('#meta_new_desc').val(fileDesc.join('@$@'));
    }

    $(this).parents('.attachment-card').remove()
})

$("body").on("keyup", ".attachment-desc", function(e) {
    if ($(this).hasClass('old')) {
        var idx = $('.attachment-desc.old').index(this);

        var fileDesc = $('#meta_old_desc').val().split('@$@');
        fileDesc[idx] = $(this).val();
        $('#meta_old_desc').val(fileDesc.join('@$@'));
    } else {
        var idx = $('.attachment-desc.new').index(this);

        var fileDesc = $('#meta_new_desc').val().split('@$@');
        fileDesc[idx] = $(this).val();
        $('#meta_new_desc').val(fileDesc.join('@$@'));
    }
})