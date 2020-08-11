
function deleteQuestion (url) {
  var url = url;  // get the url of the load_subcategorias view
      console.log(url);
          $.ajax({                       // initialize an AJAX request
              url:url ,                    // set the url of the request 
              success: function (data) {   // `data` is the return
                //console.log(data);
                document.getElementById("aviso").innerHTML = data;
                }
              })
        }


function ajaxreturn (url) {
  var url = url;  // get the url of the load_subcategorias view
      console.log(url);
          $.ajax({                       // initialize an AJAX request
              url:url ,                    // set the url of the request 
              success: function (data) {   // `data` is the return
                //console.log(data);
                document.getElementById("aviso").innerHTML = data;
                },
                 error: function (data) {
                document.getElementById("aviso").innerHTML = data.responseJSON.error; 
            }
              })
        }

  


function loadDoc (url) {
  var url = url;  // get the url of the load_subcategorias view
      console.log(url);
          $.ajax({                       // initialize an AJAX request
              url:url ,                    // set the url of the request 
              success: function (data) {   // `data` is the return
                console.log(data);
                document.getElementById("demo").innerHTML = data;
                }
              })
        };


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

