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
                        page: params.page,
                        able_create_new: $(this).attr("able-create-new")
                    };
                    if ($(this).attr("id")=="id_inventor"){
                        d.client_id = $("#id_client").select2('data')[0].id;
                    }
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
                        "Submit": function() {
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
                        Cancel: function() {
                          $(this).remove();
                        }
                    }
                });
                $(new_modal).find('input[type ="submit"]').remove();
            },
            error: function(e){
                alert("Something goes wrong.")
            }
        });
    });
});
