function BsModal(id) {

    var instance = document.getElementById(id);
    var template = '<div class="modal fade" id="'+id+'" tabindex="-1" role="dialog"> \
  <div class="modal-dialog" role="document"> \
    <div class="modal-content"> \
      <div class="modal-header"> \
        <h5 class="modal-title">Modal title</h5> \
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"> \
          <span aria-hidden="true">&times;</span> \
        </button> \
      </div> \
      <div class="modal-body"> \
      </div> \
      <div class="modal-footer"> \
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button> \
      </div> \
    </div> \
  </div> \
</div>';

    var $element;

    if (!instance) {
        $(document.body).append(template);
        $element = $(template);
    } else {
        $element = $(instance);
    }

    this.show = function(title, body) {
        $element.find('.modal-body').html(body);
        $element.find('.modal-title').html(title);
        $element.modal('show');
    };

    this.hide = function() {
        $element.modal('hide');
    };

}
