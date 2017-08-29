;$(document).ready(function(){
    // Add class "active" to sidebar menu's option, based on current url
    $(function() {
        var loc = location.pathname.split("/");
        if(loc[1] === "dashboard"){
            $('#sidebar-' + loc[1]).addClass('active');
        }
        else if (loc[1] === "proposals"){
            $('#sidebar-' + loc[2]).addClass('active');
        }
        else if (loc[1] === "billboard"){
            $('#sidebar-' + "billboard").addClass('active');
        }
    });

    // Datatable initialize.
    // Primarily for model's listview
    $('#list_table').DataTable({
      "paging": true,
      "lengthChange": false,
      "searching": true,
      "ordering": false,
      "info": true,
      "autoWidth": true,
       serverSide: true,
       ajax: {
           "url": '.',
           "type": "POST",
           "data": function ( d ) {
              return $.extend( {}, d, {
                "csrfmiddlewaretoken": jQuery("[name=csrfmiddlewaretoken]").val()
              } );
            }
       }
    });
    //Bootstrap datepicker
    $('.dateinput').datepicker({
        format: 'yyyy-mm-dd',
    });
    $('.dateinput').attr("placeholder", "yyyy-mm-dd");

    $(".has-danger").addClass("has-error");

    // Listener for models which use ajax to submit deletion
    $("#remove-object").on("click", triggerRemove);
    $(".remove-objects").on("click", triggerRemove);
    function triggerRemove(){
        let form_id = $(this).attr("form_id") || "form#remove-form";
        bootbox.confirm({
            message: 'This item will be permanently deleted and cannot be recovered. Are you sure?',
            callback: function(result){
                if (result === true){
                    $(form_id).submit();
                }
            },
            buttons: {
                cancel: {
                    label: 'Cancel',
                    className: 'btn btn-danger'
                },
                confirm: {
                    label: 'Yes',
                    className: 'btn btn-primary'
                },
            },
        })
    }

    //  Listener for file remove button
    function remove_file(){
        var $this = $(this);
        bootbox.confirm({
            message: "Are you sure?",
            callback: function(result) {
                if (result === true) {
                    $.ajax({
                        url: $this.attr("delete_url"),
                        data: {"pk": $this.attr("pk")},
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
                        },
                        success: function () {
                            $this.closest('li').remove();
                        }
                    })
                }
            },
            size: "small",
            buttons: {
                cancel: {
                    label: 'Cancel',
                    className: 'btn btn-danger'
                },
                confirm: {
                    label: 'Yes',
                    className: 'btn btn-primary'
                },
            },
        })
    }
    $('.file-remove').on('click', remove_file);

    //file uploading
    var progressBar = $('<div/>').addClass('progress progress-xs active')
        .append($('<div/>').addClass('progress-bar progress-bar-primary progress-bar-striped')
            .css({"width": '0%'}));
    var uploadButton = $('<button/>').addClass('btn btn-xs btn-primary')
        .text('Upload')
        .on('click', function () {
            var $this = $(this);
            var data = $(this).data();
            $this.parent().remove();
            $('<td/>').append(progressBar.clone(true)).appendTo(data.context);
            data.submit();
        });
    var deleteButton = $('<button/>').addClass('btn btn-xs btn-warning')
                            .text('Cancel')
                            .on('click', function () {
                                $(this).data().context.remove();
                            });

    var quitButton = $('<button/>').addClass('btn btn-xs btn-warning')
                                .text('OK')
                                .on('click', function () {
                                    $(this).data().context.remove();
                                });

    // Set maximum file size to 10Mb
    var maxFileSize = 10485760;

    function create_error_tag(text){
        var error = $('<td/>').append(
                        $('<div/>').addClass('form-group has-error').append(
                            $("<label/>").addClass('control-label').append(
                                $('<i/>').addClass('fa fa-times-circle-o')
                            ).text(text),
                        )
                    );
        return error
    }

    function get_file_size_string(size){
        return Math.floor((size / (10**6))).toString()
    }
    $('#fileupload').fileupload({
        url: $('#fileupload').attr('upload_url'),
        dataType: 'json',
        method: 'POST',
        autoUpload: false,
        headers: {
            'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
        },
        formData: {
            "object_type": $('#fileupload').attr("object_type"),
            "pk": $('#fileupload').attr("pk")
        },
    }).on('fileuploadadd', function (e, data) {
        data.context = $('<tr/>').appendTo('#files-queue');
        $.each(data.files, function (index, file) {
            if(file.size > maxFileSize){
                let message = "File size: " + get_file_size_string(file.size) +
                              "MB. It should not exceed " + get_file_size_string(maxFileSize) + "MB.";
                var error = create_error_tag(message, data);
                data.context.empty();
                data.context.append(error, $('<td/>').append(quitButton.clone(true).data(data)));
            }
            else{
                $('<td/>').append($('<span/>').text(file.name)).appendTo(data.context);
                if (!index) {
                $('<td/>').append(uploadButton.clone(true).data(data))
                          .append(deleteButton.clone(true).data(data))
                          .appendTo(data.context);
                }
            }
        });
    }).on('fileuploadfail', function (e, data) {
        var error = create_error_tag(data.jqXHR.responseJSON.message);
        data.context.empty();
        data.context.append(error, $('<td/>').append(quitButton.clone(true).data(data)));
    }).on('fileuploadprogress', function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        $(data.context).find('.progress-bar').css('width', progress + '%');
    }).on('fileuploaddone', function (e, data) {
            var result = data.result;
            var newfile = $('<li/>').append(
                $('<a/>').attr('download', '').attr('href', result.file_url).text(data.files[0].name),
                $('<button/>').addClass('btn btn-xs btn-danger pull-right file-remove')
                    .attr('pk', result.file_pk).attr('delete_url', result.delete_url)
                    .append(
                        $('<span/>').addClass('fa fa-trash-o'),
                        "Remove"
                    ).on('click', remove_file)
            );
            newfile.appendTo($('#files-list'));
            data.context.remove();
    });

    $(".ajax-select2").each(function(index) {
        $(this).select2({
            ajax: {
                url: $(this).attr("data-url"),
                dataType: 'json',
                delay: 250,
                contentType: "application/x-www-form-urlencoded; charset=UTF-8",
                data: function (params) {
                    if (params.term===undefined){
                        params.term = ""
                    }
                    d = {
                        q: params.term, // search term
                        page: params.page,
                        able_create_new: $(this).attr("able-create-new")
                    };
                    return d;
                },
                processResults: function (data, params) {
                  params.page = params.page || 1;
                  return {
                    results: data.items,
                    pagination: {
                      more: (params.page * 10) < data.total_count
                    }
                  };
                },
                cache: true
            },
            escapeMarkup: function (markup) { return markup; }, // let our custom formatter work
            minimumInputLength: 0,
            placeholder: "Type to search..."
        });
    });


    $('.ajax-select2').on('select2:select',function(e){
        var $target = $(e.target);
        if (e.params.data.id >= 0 || $target.attr("able-create-new")==="false") return false;
        e.preventDefault();
        $(this).find('option[value="-1"]').remove();
        var feedback_array = [];
        var parent_div = [];
        $.ajax({
            url: $target.attr("create-new-url"),
            success: function (data) {
                var new_modal = $("<div></div>").appendTo("section.content").html(data.html);
                new_modal.dialog({
                    resizable: false,
                    height: "auto",
                    title: 'Create New '+ $target.attr("name"),
                    zIndex: 10000,
                    autoOpen: true,
                    modal: true,
                    width: "50%",
                    position:{ my: "center center", at: "center center", of: $("section.content") },
                    buttons: {
                        "Submit": {
                            click: function() {
                                while(feedback_array.length>0){
                                    let ele = feedback_array.pop();
                                    ele.remove();
                                }
                                while(parent_div.length>0){
                                    let ele = parent_div.pop();
                                    ele.removeClass("has-error");
                                }
                                var error = false;
                                $("#ajax-modal").find("form").ajaxSubmit({
                                    url: $target.attr("create-new-url"),
                                    dataType:"json",
                                    method: "POST",
                                    success: function (data) {
                                        let newOption = new Option(data.text, data.id, false, true);
                                        $target.append(newOption);
                                        new_modal.remove();
                                    },
                                    error: function (data) {
                                        error = true;
                                        for (key in data.responseJSON){
                                            let $feedback = $('<span class="help-block">'+ data.responseJSON[key] +'</span>');
                                            let $parent = $('input[name='+ key +']').parents(".form-group").first() ;
                                            $parent.addClass("has-error").append($feedback);
                                            parent_div.push($parent);
                                            feedback_array.push($feedback);
                                        }
                                    }
                                });
                            },
                            class: "btn btn-primary",
                            text: "Submit"
                        },
                        Cancel: {
                            click: function() {
                                      $(this).remove();
                                    },
                            class: "btn btn-default",
                            text: "Cancel"
                        },
                    }
                });
                $(new_modal).find('input[type ="submit"]').remove();
            },
            error: function(e){
                alert("Something goes wrong.")
            }
        });
    });

    // Use for translating chinese post address to english address
    $("#div_id_post_address").find("label").append('<a class="btn btn-xs btn-primary" id="translate_address">Try to translate</a>')
    $("#translate_address").on("click", function(){
        $.ajax({
            url: "/proposals/chinese_to_english/",
            data: {
                "address": $("#id_post_address").val()
            },
            success: function(data){
                if(data.english_address) $("#id_english_address").val(data.english_address);
                else if (data.error) alert(data.error);
            },
            error: function(e){
                alert("Can't not translate.")
            }
        })
    })
});
