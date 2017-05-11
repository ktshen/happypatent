$(document).ready(function() {

    function showPriority(){
        $("#div_id_prio_country").show();
        $("#div_id_prio_application_no").show();
        $('#div_id_prio_filing_date').show();
    }

    function hidePriority(){
        $("#div_id_prio_country").hide();
        $("#div_id_prio_application_no").hide();
        $('#div_id_prio_filing_date').hide();
    }

    function PriorityDecision(){
        if($("#id_priority").find(":selected").val() === "yes"){
            showPriority();
        }
        else{
            hidePriority();
        }
    }

    PriorityDecision();

    $("#id_priority").on("change", function(e){
        PriorityDecision();
    });

});
