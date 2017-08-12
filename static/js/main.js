function go(addr) {
		     var width = 600
			var height = 700
			var leftPx = ( screen.availWidth - width ) / 2;
			var topPx = ( screen.availHeight - height ) / 2;
			var params = "width=" +width+ ", height=" +height+ ", resizable=yes, scrollbars=yes, top=" +topPx+ ", left=" +leftPx;
			window.open(addr,"MyWin", params);
		  };

function go_sticker(addr) {
		    var width = 300
			var height = 150
			var leftPx = ( screen.availWidth - width ) / 2;
			var topPx = ( screen.availHeight - height ) / 2;
			var params = "width=" +width+ ", height=" +height+ ", resizable=yes, scrollbars=yes, top=" +topPx+ ", left=" +leftPx;
			window.open(addr,"MyWin", params);
		  };

function go_fin(addr) {
		     var width = 1200
			var height = 800
			var leftPx = ( screen.availWidth - width ) / 2;
			var topPx = ( screen.availHeight - height ) / 2;
			var params = "width=" +width+ ", height=" +height+ ", resizable=yes, scrollbars=yes, top=" +topPx+ ", left=" +leftPx;
			window.open(addr,"MyWin", params);
		  };


$('.dropdown-toggle').dropdown()


function PaidEngineer() {
  var indicator = $('#ajax-progress-indicator');

  $('.is_paid input[type="checkbox"]').click(function(event){
    var box = $(this);
    $.ajax(box.data('url'), {
      'type': 'POST',
      'async': true,
      'dataType': 'json',
      'data': {
        'pk': box.data('repair-id'),
        'paid_engineer': parseFloat(box.data('repair-pay')).toPrecision(2),
        'is_paid': box.is(':checked') ? '1': '',
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
      },
      'beforeSend': function(xhr, settings){
        indicator.show();
      },
      'error': function(xhr, status, error){
        alert(error);
        indicator.hide();
      },
      'success': function(data, status, xhr){
      alert('ok');
        indicator.hide();
      }
    });
  });
}

function CloseOrder() {

  $('.is_money input[type="checkbox"]').click(function(event){
    var box = $(this);
    $.ajax(box.data('url'), {
      'type': 'POST',
      'async': true,
      'dataType': 'json',
      'data': {
        'is_money': box.is(':checked') ? '1': '',

      },
      'beforeSend': function(xhr, settings){
        indicator.show();
      },
      'error': function(xhr, status, error){
        alert(error);
        indicator.hide();
      },
      'success': function(data, status, xhr){
      alert('pay_engineer');
        indicator.hide();
      }
    });
  });
}




 $(function() {
           // Bootstrap DateTimePicker v4
           $('input.dateinput').datetimepicker({
                 format: 'YYYY-MM-DD',
           });
        });

$(function() {
           $(document).ready(function(){
               $("#myTab li:eq(0) a").tab('show');
          });
        });



function AjaxForm() {
        $('#forminput').submit(function() {

            $.ajax({ // create an AJAX call...
                data: $(this).serialize(), // get the form data
                type: $(this).attr('method'), // GET or POST
                url: $(this).attr('action'), // the file to call
                async: true,
                success: function(data, textStatus, jqXHR) {

                    window.close();

                    window.opener.location.reload();

                } ,
          error: function() {
              alert('Не всі обовязкові* поля заповнені');
          }


            });
            return false;
        });
    };

function initEditOrderPage() {
  $('a.kvant-edit-form-link').click(function(event){
    var link = $(this);
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr){
        // check if we got successfull response from the server
        if (status != 'success') {
          alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
          return false;
        }

        // update modal window with arrived content from the server
        var modal = $('#myModal'),
        html = $(data), form = html.find('.form-horizontal');
        modal.find('.modal-title').html("<h3>Форма редагування</h3>");
        modal.find('.modal-body').html(form);

        // init our edit form
        initEditOrderForm(form, modal);

        // setup and show modal window finally
        modal.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
        });
      },
      'error': function(){
          alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
          return false
      }
    });

    return false;
  });
}

function initEditOrderForm(form, modal) {

  // close modal window on Cancel button click
  form.find('input[name="cancel_button"]').click(function(event){
    modal.modal('hide');
    return false;
  });

  // make form work in AJAX mode
  form.ajaxForm({
    'dataType': 'html',
    'error': function(){
        alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
        return false;
    },
    'success': function(data, status, xhr) {
      var html = $(data), newform = html.find('#content-column form');

      // copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));

      // copy form to modal if we found it in server response
      if (newform.length > 0) {
        modal.find('.modal-body').append(newform);

        // initialize form fields and buttons
        initEditStudentForm(newform, modal);
      } else {
        // if no form, it means success and we need to reload page
        // to get updated students list;
        // reload after 2 seconds, so that user can read success message
        setTimeout(function(){location.reload(true);}, 500);
      }
    }
  });
}



$(document).ready(function(){
  AjaxForm();
  PaidEngineer();
  initEditOrderPage();

 });


