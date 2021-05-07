document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.fixed-action-btn');
    var instances = M.FloatingActionButton.init(elems, {
        direction: 'top',
        hoverEnabled: true
    });

});
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.parallax');
    var instances = M.Parallax.init(elems,);
});

 
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems);
});



document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems,);
});

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.timepicker');
    var instances = M.Timepicker.init(elems,);
});


document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems, );
  });

  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.tabs');
    var instance = M.Tabs.init(elems,);
  });
document.addEventListener('DOMContentLoaded', function() {
	var elems = document.querySelectorAll('.sidenav');

	var instances = M.Sidenav.init(elems, 'left',{
		edge: 'left',
		draggable: true,
		preventScrolling: true
	});
});
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems,{coverTrigger: false});
  });

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function ajaxRequest(url,token,type,data,callback) {
    
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": token },
        dataType: "json",
        processData: true,
        contentType: "application/json",
        type: type, 
        data:JSON.stringify(data),
        success: function(d){
            console.log(d)
            return callback(d);
        },
        error: function(error_data){
            console.log("error")
            console.log(error_data)
        },
    })
}

function getUrl(url,data_string,api,token,callback) {
    
    $.ajax({
        url: url,
        headers: { "X-CSRFToken": token },
        dataType: "json",
        success: function(data){
            console.log(data[api])
            return callback(data[api],data_string);
        },
        error: function(error_data){
            console.log("error")
            console.log(error_data)
        },
    })
}

function getFields(form,callback) {
    var form = document.forms[form]
    let data = {};
    for (var i = 0; i < form.elements.length; i++) {
        var value = form.elements[i].value
        var name = form.elements[i].name
        if (name != "csrfmiddlewaretoken" & name != ""){
            var select = document.getElementById(form.elements[i].id)
            
            if (select.length > 1){
                var result = [];
                var options = select && select.options;
                var opt;

                for (var j=0;j < options.length; j++) {
                    opt = options[j];

                    if (opt.selected) {
                    result.push(opt.value);
                    }
                }
                console.log(name)
                console.log(result)
                //console.log(form.elements[i].length)
                data[name] = result;
            }else{
                console.log(name)
                console.log(value)
                data[name] = value;
            }
        }  
    }
    return callback(data);
}
function arrayContains(needle, arrhaystack)
{
    return (arrhaystack.indexOf(needle) > -1);
}
function addTd(data,exclude,tbody){
   
    var tr = '<tr>';
    for (const i in data){ 
        console.log(`${i}: ${data[i]}`);
        if (!(arrayContains(i, exclude))){
            tr += '<td>' + data[i] + '</td>';
        }
    }
    tr += '<td>edit</td><td>delete</td></tr>';
    tbody.innerHTML += tr
}