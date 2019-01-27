/////////////////////// patientDetail.html///////////////////////////


$( document ).ready(function() {
    $('input[name="eventrange_create"]').daterangepicker({
        timePicker: true,
        timePickerIncrement: 30,
        startDate: new Date().setHours(0,0,0,0),
        endDate: moment(new Date().setHours(0,0,0,0)).add(1, 'days'),
        // dateLimit: { "hours" : 8 },
        locale: {
            format: 'MM/DD/YYYY h:mm A'
        },
    });
});

// when change happens in createRange, update the hidden inputs
$( "#createRange" ).change(function() {
    var range = $('input[name="eventrange_create"]').val().split('-');
    updateInputRange(range, true);
});

// when change happens in range, update the hidden inputs
function updateRange(){
    var range = $('input[name="eventrange_update"]').val().split('-');
    updateInputRange(range, false);
};

// update the specified [create/update] hidden inputs based on range
function updateInputRange(range, isCreate){
    var start = moment(range[0].trim(), 'MM/DD/YYYY hh:mm a').format("YYYY-MM-DD HH:mm");
    var end = moment(range[1].trim(), 'MM/DD/YYYY hh:mm a').format("YYYY-MM-DD HH:mm");
    if(isCreate){
        var start_element=document.getElementById("startTimeCreate");
        start_element.setAttribute("value", start);
        var end_element=document.getElementById("endTimeCreate");
        end_element.setAttribute("value", end);
    }else{
        var start_element=document.getElementById("startTimeChange");
        start_element.setAttribute("value", start);
        var end_element=document.getElementById("endTimeChange");
        end_element.setAttribute("value", end);
    };

};

// For dataTable of documents 
$(document).ready(function(){
    $('#myTable').DataTable();});

// For loading the document by passing appr link
function passLink(url) {
	var element=document.getElementById("objectlink");
	element.setAttribute("data",url);
};

// For passing docID to appr update/delete form
function passDocID(docId, visitDate){
    document.getElementById("delConfirm").innerHTML = "Are you sure that you want to delete the event on " + visitDate + '?';

    var form_upload=document.getElementById("uploadform");
    var form_delete=document.getElementById("deleteform");
    form_upload.action="update_doc/"+docId;
    form_delete.action="delete_doc/"+docId;
};

// For appropriately updating the eventRange
function passDateTime(start, end, docId) {
    var start_date=moment(start.trim());
    var end_date=moment(end.trim());
    $('input[name="eventrange_update"]').daterangepicker({
        startDate: start_date,
        endDate: end_date,
        timePicker: true,
        timePickerIncrement: 30,
        // dateLimit: { "hours" : 8 },
        locale: {
            format: 'MM/DD/YYYY h:mm A'
        }
    }); 
    var form=document.getElementById("datechangeform");
    form.action="update_doc/"+docId;
};
