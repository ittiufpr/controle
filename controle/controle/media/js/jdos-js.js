function searchTable(idtable, idinput) {
  // Declare variables
  var input, filter, table, tr, td, i,j,flag, txtValue;
  input = document.getElementById(idinput);
  filter = input.value.toUpperCase();
  table = document.getElementById(idtable);
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 1; i < tr.length; i++) {
    flag=0;
    for(j=0;j< tr[i].getElementsByTagName("td").length;j++){
      td = tr[i].getElementsByTagName("td")[j];
        if (td) {
          txtValue = td.textContent || td.innerText;
          //console.log(txtValue);
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          flag=1;
        } 
      }
    }
    if (flag==1) {
      tr[i].style.display = "";
    } else {
      tr[i].style.display = "none";
    }

  }
}


function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("example");
  switching = true;
  //Set the sorting direction to ascending:
  dir = "asc"; 
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /*check if the two rows should switch place,
      based on the direction, asc or desc:*/
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchcount ++;      
    } else {
      /*If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again.*/
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

function exportTableToCSV($table, filename) {

    var $rows = $table.find('tr:has(td)'),

      // Temporary delimiter characters unlikely to be typed by keyboard
      // This is to avoid accidentally splitting the actual contents
      tmpColDelim = String.fromCharCode(11), // vertical tab character
      tmpRowDelim = String.fromCharCode(0), // null character

      // actual delimiter characters for CSV format
      colDelim = '";"',
      rowDelim = '"\r\n"',

      // Grab text from table into CSV formatted string
      csv = '"' + $rows.map(function(i, row) {
        var $row = $(row),
          $cols = $row.find('td');

        return $cols.map(function(j, col) {
          var $col = $(col),
            text = $col.text();

          return text.replace(/"/g, '""'); // escape double quotes

        }).get().join(tmpColDelim);

      }).get().join(tmpRowDelim)
      .split(tmpRowDelim).join(rowDelim)
      .split(tmpColDelim).join(colDelim) + '"';

     // var blob = new Blob([csv],{encoding:"UTF-8",type:"text/plain;charset=UTF-8"});
    var blob = new Blob(["\ufeff"+csv], { type: 'text/csv;charset=utf-8;' });

      if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, filename);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
  }

/*
$(document).ready( function() {

$(".data").click(function () {
      var url = $("#example").attr("data-itens-equipamento-url");  // get the url of the load_subcategorias view
      console.log(url);
      var teste = this;
      var id_item = $(this).children().first().text();  // get the selected  ID click
      console.log("ITEM:", id_item);
      $.ajax({                       // initialize an AJAX request
        url:url ,                    // set the url of the request 
        data: {
          'id_item': id_item       // add the categoria id to the GET parameters
        },
        success: function (data) {   // `data` is the return
          if (document.getElementById("itens_equipamento_"+id_item)==null){
            $("<tr><td id=itens_equipamento_"+ id_item + " \" colspan='9'>"+ data+ "</td></tr>").insertAfter(teste);
          }
          else{
            $("#itens_equipamento_"+ id_item).toggle();
          }

        }
      });

    });
});
*/