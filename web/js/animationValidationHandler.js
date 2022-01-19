// transition to dynamic display and halt:
$( document ).ready(function() {
    $('.hud').one("animationend", function(){
        setTimeout(function() {
          // now start adding the dropdown.
          addDropButtons();
          // confetti();
          // $('#container').remove(); use this to remove
        }, 0);
      }
    );
});


//---------------------------------------------------------------------------------------------------
async function onClickTypeButton(value){
  $('.textValidationType').append("<span/>").html(value);
  textValidationType = value;
}
//---------------------------------------------------------------------------------------------------
async function onClickChooseFileCSVButton(){
  // console.log("GO!")
  var path = await eel.pythonGoButtonClicked()();
   if (path) {
     // console.log(path);
     $(".fileTextBox1").val(path)
     filename = path
   }
}
async function onClickChooseFileqPCRButton(){
  // console.log("GO!")
  var path = await eel.pythonGoButtonClicked()();
   if (path) {
     // console.log(path);
     $(".fileTextBox3").val(path)
     filePathway = path
   }
}

async function onClickGoButton(){
  let finalDataFrame = await eel.Captureto96WellFormat(filename,filePathway);
  const start = () => {
    setTimeout(function() {
        confetti.start()
    }, 3000); // 1000 is time that after 1 second start the confetti ( 1000 = 1 sec)
  };

  start();
  $('#inputMapModal').modal("show")
  }

function addDropButtons(){
  // console.log('FIXME: add dropdown buttons')
  $('.hud').append($("<div/>").addClass("dropDownRow row").attr({"style": "padding-bottom: 10px"})
                  .append($("<div/>").addClass("col-15").attr({"style": "text-align: center;"})
                          .append($("<div/>").addClass("btn-group")
                                  .append($("<button/>").addClass("btn btn-primary dropdown-toggle animate__animated animate__fadeInUp").attr({'data-toggle': "dropdown", "aria-haspopup": "true", "aria-expanded": "false"}).html("AE6 Data Analysis"))
                                  .append($("<div/>").addClass("dropdown-menu")
                                          .append($("<a/>").addClass("dropdown-item").attr({"href":"#"}).html("AE3 Worklist Generator").click(function(){onClickTypeButton("AE3_Worklist")}))
                                          .append($("<a/>").addClass("dropdown-item").attr({"href":"#"}).html("AE6 Data Manipulator").click(function(){onClickTypeButton("AE6_Data")}))
                                          .append($("<a/>").addClass("dropdown-item").attr({"href":"#"}).html("AE7 Worklist Generator").click(function(){onClickTypeButton("AE7_Worklist")}))
                                          )
                                  )
                            ) 
  )    

  $('.hud').append($("<div/>").addClass("row")
                    .append($("<div/>").addClass("col-12")
                            .append($("<div/>").addClass("input-group mb-3").attr({"style": "display:table; text-align: center;"})
                                    .append($("<div/>").addClass("custom-file")
                                            .append($("<button/>").addClass("btn btn-outline-light").attr({"type": "button", "id": "inputGroupFile02"}).html("Choose input worklist").click(function(){onClickChooseFileCSVButton()}))
                                            .append($("<input/>").addClass("fileTextBox1").attr({"disabled": true}))
                                          )
                                  )
                           )
                  )
  $('.hud').append($("<div/>").addClass("row")
                .append($("<div/>").addClass("col-12")
                        .append($("<div/>").addClass("input-group mb-3").attr({"style": "display:table; text-align: center;"})
                                .append($("<div/>").addClass("custom-file")
                                        .append($("<button/>").addClass("btn btn-outline-light").attr({"type": "button", "id": "inputGroupFile04"}).html("Choose Biorad CSV File").click(function(){onClickChooseFileqPCRButton()}))
                                        .append($("<input/>").addClass("fileTextBox3").attr({"disabled": true}))
                                      )
                              )
                       )
              )
                          .append($("<div/>").addClass("col-15 goButton").attr({"style": "text-align: center;"})
                                  .append($("<button/>").addClass("btn btn-outline-success animate__animated animate__fadeInUp").html("Go!").click(function(){onClickGoButton()}))
                                )
}