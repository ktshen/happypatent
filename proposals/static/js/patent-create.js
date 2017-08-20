$(document).ready(function() {
    //Priority
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

    function manage_US(e){
        if(e===true){
            $("#div_id_extended_days").show();
            $("#div_id_IDS_infomation").show();
        }
        else{
            $("#div_id_extended_days").hide();
            $("#div_id_IDS_infomation").hide();
            $("#id_extended_days").val("0");
            $("#id_IDS_infomation").val("");
        }
    }
    //IDS, extended days (US only)
    $("#id_country").on("select2:select", function(e){
        if(e.params.data.id==="US") manage_US(true);
        else manage_US(false);
    });
    //fire at start
    if($("#id_country").find('option[selected="selected"]').val()!=="US") manage_US(false);
});
