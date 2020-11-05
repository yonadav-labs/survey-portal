var tplAttachment = `
    <div class="card attachment-card border-light border mb-2">
        <div class="card-body">
            <button type="button" class="close close-card" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
            <div class="form-group float-left">
                <input type="file" id="example-fileinput" class="form-control-file">
            </div>
            <div class="clearfix"></div>
            <div class="form-group">
                <label for="simpleinput">Description</label>
                <input type="text" id="simpleinput" class="form-control">
            </div>
        </div>
    </div>
`

$("body").on("click", "#add-attachment-card", function(e) {
    $('.attachments-wrapper').append(tplAttachment);
})

$("body").on("click", "button.close-card", function(e) {
    $(this).parents('.attachment-card').remove()
})