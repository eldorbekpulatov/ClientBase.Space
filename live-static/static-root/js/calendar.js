/////////////////////////////////////////////////////
////////////////calendar.html///////////////////////
///////////////////////////////////////////////////

$(document).ready(function() {
    // page is now ready, initialize the calendar...
    $('#calendar').fullCalendar({
        // put your options and callbacks here
        locale: 'en',
        header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek,agendaDay'
		},
		views: {
    		month: { // name of view
        		titleFormat: 'MMMM Y' },
    		basic: {
    			titleFormat: 'MMM Y' }
    	},
    	selectable:true,
    	selectHelper:true,
    	editable: true,
    	eventLimit:true,
    	droppable:true,
    	firstDay: 1,
    	allDay: true,
    	allDaySlot: true,
    	minTime: "06:00:00",
		maxTime: "21:00:00",
		defaultView: 'month',
        theme: true,
        themeSystem: 'bootstrap3',
        fixedWeekCount: false,
        navLinks: true, 
		events: [], 
		select: function(start, end) {
			eventCreate(start, end);
  		},
  		eventDrop: function(event, delta, revertFunc, jsEvent, ui, view){
	  		if (!confirm("Are you sure about this change?")) {
	        	revertFunc();
	        }else{
        		updateEvent(event, true); 
        	}
        },
  		eventResize: function(event, delta, revertFunc, jsEvent, ui, view){ 
	  		if (!confirm("Are you sure about this change?")) {
	        	revertFunc();
	        }else{
  				updateEvent(event, false);
  			}
  		},
  		viewRender: function(view) { getEvents(); },
  		eventClick: function(event) { pullEvent(event.id); },
  		
  		drop: function(date, jsEvent, ui, resourceId){
  			// make the event end-time based on drop location
  			var end = date._ambigTime ? moment(date).add(1, 'days') : moment(date).add(2, 'hours'); 
  			document.getElementById("patName").value = $(this).attr("name"); // use the element's name as patName
			eventCreate(date, end); // toggle the eventCreate modal
  			// $(this).remove();
	    },
	});

    function makeDraggable(){
		$('#external-events .fc-event').each(function() {
	    	// make the event draggable using jQuery UI
		    $(this).draggable({
		        zIndex: 999,
		        revert: true,      // will cause the event to go back to its
		        revertDuration: 0  //  original position after the drag
		    });
		});
	}

    function eventCreate(start, end){
    	// toggle the createModal and autofill the dates
		$("#createModal").modal();
		var start_select = moment(start).format('MM/DD/YYYY h:mm A');
		var end_select = moment(end).format('MM/DD/YYYY h:mm A');
		document.getElementById('calen_Date').value = start_select + " - " + end_select;
		
		// update the hidden dateInputFields accoding to selected dates
		var start_element=document.getElementById("startTimeCreate");
        start_element.setAttribute("value", start.format('YYYY-MM-DD HH:mm'));
        var end_element=document.getElementById("endTimeCreate");
        end_element.setAttribute("value", end.format('YYYY-MM-DD HH:mm'));
    };


    // AJAX POST
    $("#createEvent").click(function (event) {
    	event.preventDefault();
    	 // Get form
        var form = $('#fileUploadForm')[0];
		// Create an FormData object
        var data = new FormData(form);
        // get the patient ID from selected_patients
        var patID = $("#patients option[value='" + $("input[name=selected_patient]").val() + "']").attr('data-id');
        
        // Append the patID to data
        data.append("patID", patID);

        // only if the patient is selected, then make post 
        if (!patID==""){
	        $.ajax({
	            type: "POST",
	            url: "/calendar/post",
	            dataType: "json",
	            data: data,
	            enctype: 'multipart/form-data',
	            processData: false,
	            contentType: false,
	            cache: false,

	            success: function(){
	            	$('#createModal').modal('toggle');
	            	document.getElementById("patName").value = '';
	            	getEvents();
	            },
	        });
	    }
    });


	// AJAX PULL
	var lastClickedEventID;
    function pullEvent(eventID){
    	$.ajax({
	        type: 'GET',
	        url:'/calendar/pull', 
	        data: {'docID' : eventID},

	        success: function(data){
	        	lastClickedEventID=eventID;
	        	$("#pullModal").modal();
	        	var pos = data.patAddress.indexOf(",");
                var start = data.patAddress.slice(0, pos+1)+' '+ data.patExtAdd;
                var end = data.patAddress.slice(pos+1);
                document.getElementById("patAddressPull").innerHTML = start +'</br>'+ end;
	        	
	        	document.getElementById("patNamePull").innerHTML = 
	        	'<a href="http://127.0.0.1:8000/dir/'+ data.patID +'">'+ data.patName + '</a>';
	        	document.getElementById("eventSpan").innerHTML = data.eventStart + "</br>" + data.eventEnd;
	        	document.getElementById("patNumber").innerHTML ='<a href="tel:'+data.patNumber+'">'+data.patNumber+'</a>';
	        	if (data.completed){
	        		document.getElementById('deleteEvent').style="display:none;";
	        	}else{
	        		document.getElementById('deleteEvent').style="display:inline-block;";
	        	};
	        },
    	});
    };


    // when deleteEvent is clicked
    $("#deleteEvent").click(function(){ 
    	$('#pullModal').modal('toggle'); 
    	deleteEvent(lastClickedEventID); 
    });
    
    // AJAX DELETE
    function deleteEvent(eventID){
    	$.ajax({
            type: "POST",
            url: "/calendar/delete",
            dataType: "json",
            data: {'docID': eventID },
            success: function(){ getEvents() },
    	});
    };

    // AJAX UPDATE
    function updateEvent(event, isDrop){
    	// logic to drop and resize events
    	if (event.allDay && isDrop && event.end-event.start<=3600000){
		    event.end=moment(event.start).add(1, 'days');
		}else if (!event.allDay && isDrop && event.end-event.start<=3600000 ){
		    event.end=moment(event.start).add(2, 'hours');
		};
	       
        var data = {
        	'docID' 			: event.id,
        	'docNewDateStart' 	: event.start.format('YYYY-MM-DD HH:mm'),
        	'docNewDateEnd' 	: event.end.format('YYYY-MM-DD HH:mm'), 
        };

		$.ajax({
            type: "POST",
            url: "/calendar/update",
            dataType: "json",
            data: data,
    	});
    };

    // AJAX RETRIVE
	function getEvents(){
		// clear all previous events
	    $('#calendar').fullCalendar('removeEvents');
	    // clear the suggestion bar on each viewChange
	    document.getElementById('external-events').innerHTML='';

		var date_format = "YYYY-MM-DD HH:mm";
		var view = $('#calendar').fullCalendar('getView');
		var range = {	"start": view.start.format(date_format), 
						"end": view.end.format(date_format) 		};
	    // AJAX GET
	    $.ajax({
	        type: 'GET',
	        url:'/calendar/get', 
	        data: range,
	        success: function(data){
	        	// append the new data
				for(i = 0; i < data.events.length; i++){
					var event = {
						id 		: data.events[i].id,
						title 	: data.events[i].name,
						start 	: data.events[i].start,
						end 	: data.events[i].end,
						color 	: data.events[i].completed ? "slateblue" : "orange",
						allDay 	: data.events[i].allDay,
						stick 	: true 		};

					$('#calendar').fullCalendar('renderEvent', event);
					$('#calendar').fullCalendar('unselect');
            	};
            	//for each suggestion, append the HTML values
            	for (i = 0; i < data.suggests.length; i++){
            		var last = document.getElementById('external-events').innerHTML;
            		document.getElementById('external-events').innerHTML = last + '<div class="fc-event" name="' + 
            			data.suggests[i].patName + '">'+ data.suggests[i].patName +'</br> Due: '
            			+ data.suggests[i].nextVisit +'</div>';
            	};
            	// make the appended suggestions draggable
            	makeDraggable();
	    	},
		});
	};
	


	// CSRF code for update and delete ajax requests
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    }); 
});
