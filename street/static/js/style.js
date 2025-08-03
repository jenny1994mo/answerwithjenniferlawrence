// // Changing Images
var slideIndex = 0;
imagechanging();
 function imagechanging(){
  var i;
  var x = document.getElementsByClassName("mySlides");
  for (i = 0; < x.length; i++){
    x[i].style.display = "none";
  }
  slideIndex++;
  if (slideIndex > x.length){slideIndex=1}
    x[slideIndex-1].style.display = "block";
  setTimeout(imagechanging, 200);
 }

 function openLinks(evt,tabName){
	var i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++){
    tabcontent[i].style.display = "none";

  }
  tablinks = document.getElementsByClassName("tablinks");
  for(i = 0; i < tablinks.length; i++){
    tablinks[i].className = tablinks[i].className.replace(" active","");
  }

  document.getElementById(tabName).style.display="block";
	}

  $(document).ready(function(){
    url = location.href;
    hash= url.split('#/');
    myLink= '#/'+hash[1];
    if(hash[1]){
      $('#myTab a[href="' + myLink +'"]')
        document.getElementById(hash['1']).style.display="block";
    }

}); 
  
  // Search Toggle
	setTimeout(fade_out, 2000)
      function fade_out(){
        $(".alert").fadeOut().empty()
      }
    $(document).ready(function(){
      $(".search").click(function(){
        $(".showform").toggle(700);
      });
    });
    $(document).ready(function(){
      $('input').val("");
    });
 
//stop
