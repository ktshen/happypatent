/* Project specific Javascript goes here. */

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


    $('.django-select2').on('select2:select',function(e){
        if (e.params.data.id >= 0) return false;
        var $target = $(e.target);
        var $modal = $("#"+$target.attr("modelform_id"));
        $target.children("option").last().remove();
        $modal.modal();
        $modal.find(".django-select2").djangoSelect2().on('select2:select', function(e){
            var newOption = new Option(e.params.data.text, e.params.data.id, false, true);
            $(e.target).append(newOption);
        });
        $modal.find("form").on("submit", function (e) {
            e.preventDefault();
            $(e.target).ajaxSubmit({
                url: $(this).attr("action"),
                method: "POST",
                dataType: 'json',
                success: function (data) {
                    $('.close').click();
                    var newOption = new Option(data.text, data.id, false, true);
                    $target.append(newOption);
                },
                error: function (data) {
                    alert("Something goes wrong. Check the form again");
                    console.log(data);
                }
            });
        });
    });

    //Bootstrap datepicker
    $('.dateinput').datepicker({
        format: 'yyyy-mm-dd',
    });
});
