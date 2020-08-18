//Formulario itens

$(document).on("click", "#id_categoria", function() {

$("#id_categoria").change(function () {
      var url = $("#ModalItem").attr("data-load-categorias-url") ;  // get the url of the load_subcategorias view
  
      var id_categoria = $(this).val();  // get the selected categoria ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url:url ,                    // set the url of the request (= localhost:8000/ajax/load_subcategorias/)
        data: {
          'id_categoria': id_categoria       // add the categoria id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_subcategorias` view function
          $("#id_subcategoria").html(data);  // replace the contents of the subcategoria input with the data that came from the server
        }
      });

    });



});

//Formulario Novo Equipamentos

$(document).on("click", "#id_item-categoria", function() {

$("#id_item-categoria").change(function () {
      var url = $("#ModalItem").attr("data-load-categorias-url") ;  // get the url of the load_subcategorias view
      
      var id_categoria = $(this).val();  // get the selected categoria ID from the HTML input

      $.ajax({                       // initialize an AJAX request
        url:url ,                    // set the url of the request (= localhost:8000/ajax/load_subcategorias/)
        data: {
          'id_categoria': id_categoria       // add the categoria id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_subcategorias` view function
          $("#id_item-subcategoria").html(data);  // replace the contents of the subcategoria input with the data that came from the server
        }
      });

    });


});




























