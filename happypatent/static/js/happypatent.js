$(document).ready(function(){
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

    // Datatable initialize
    $('#list_table').DataTable({
      "paging": true,
      "lengthChange": true,
      "searching": true,
      "ordering": false,
      "info": true,
      "autoWidth": true
    });

    //Bootstrap datepicker
    $('.dateinput').datepicker({
        format: 'yyyy-mm-dd',
    });
    $('.dateinput').attr("placeholder", "yyyy-mm-dd");

    $(".has-danger").addClass("has-error");

    $("#remove-object").on("click", function() {
        $('<div></div>').appendTo('section.content')
            .html('<div><p><span class="ui-icon ui-icon-alert" style="float:left; margin:12px 12px 20px 0;"></span>This item will be permanently deleted and cannot be recovered. Are you sure?</p></div>')
            .dialog({
                resizable: false,
                height: "auto",
                title: 'Warning',
                width: 400,
                zIndex: 10000,
                autoOpen: true,
                modal: true,
                buttons: {
                    "Delete": function() {
                       $("form#remove-form").submit();
                    },
                    Cancel: function() {
                      $(this).remove();
                    }
                }
            });
    });

    $(".ajax-select2").each(function(index) {
        $(this).select2({
            ajax: {
                url: $(this).attr("data-url"),
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    d = {
                        q: params.term, // search term
                        page: params.page
                    };
                    if ($(this).attr("id")=="id_inventor"){
                        d.client_id = $("#id_client").select2('data')[0].id;
                    }
                    console.log(d);
                    return d;
                },
                processResults: function (data, params) {
                  // parse the results into the format expected by Select2
                  // since we are using custom formatting functions we do not need to
                  // alter the remote JSON data, except to indicate that infinite
                  // scrolling can be used
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
            minimumInputLength: 1,
            placeholder: "Type to search..."
        });
    });


    // $('.ajax-select2').on('select2:select',function(e){
    //     if (e.params.data.id >= 0) return false;
    //     var $target = $(e.target);
    //     var $modal = $("#"+$target.attr("modelform_id"));
    //     $target.children("option").last().remove();
    //     $modal.modal();
    //     $modal.find(".django-select2").djangoSelect2().on('select2:select', function(e){
    //         var newOption = new Option(e.params.data.text, e.params.data.id, false, true);
    //         $(e.target).append(newOption);
    //     });
    //     $modal.find("form").on("submit", function (e) {
    //         e.preventDefault();
    //         $(e.target).ajaxSubmit({
    //             url: $(this).attr("action"),
    //             method: "POST",
    //             dataType: 'json',
    //             success: function (data) {
    //                 $('.close').click();
    //                 var newOption = new Option(data.text, data.id, false, true);
    //                 $target.append(newOption);
    //             },
    //             error: function (data) {
    //                 alert("Something goes wrong. Check the form again");
    //                 console.log(data);
    //             }
    //         });
    //     });
    // });

    $("#id_inventor").prop("disabled", true);

    $("#id_client").on("select2:select", function(e){
        $("#id_inventor").prop("disabled", false);
    });
});
