
$(document).ready(function() {
    $(".select2-js").select2({
        placeholder: "Please select",
        minimumResultsForSearch: Infinity
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

});
