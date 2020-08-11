$(document).ready( function() {
//quando clica sobre as linhas com a classe .data pega o id do equipamento e retorna os itens
$(".data").click(function () {
      var url = $("#example").attr("data-itens-equipamento-url");  // get the url of the load_subcategorias view
      //console.log(url);
      var teste = this;
      var id_item = $(this).children().first().text();  // get the selected  ID click
      //console.log("ITEM:", id_item);
      if (document.getElementById("itens_equipamento_"+id_item)==null){ //verifica se os dados já foram carregados
          $.ajax({                       // initialize an AJAX request
            url:url ,                    // set the url of the request 
            data: {
              'id_item': id_item       // add the categoria id to the GET parameters
            },
            success: function (data) {   // `data` is the return
              console.log(data);
                $("<tr><td id=itens_equipamento_"+ id_item + " \" colspan='10'>"+ data+ "</td></tr>").insertAfter(teste);
      
            }
          });
        }
       else{//caso os dados já foram carregados apenas esconde ou mostra as informações
            $("#itens_equipamento_"+ id_item).toggle();
          }

    });
});
