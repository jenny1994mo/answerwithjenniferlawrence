<script language="javascript">
$('#myCarousel').on('slide.bs.carousel', function (e) {
	var $e = $(e.relatedTarget);
	var idx = $e.index();
	var itemPerSlide = 4;
	var totalItems = $('carousel-item').length;

	if (idx >=totalItems - (itemPerSlide-1)){
		var it = itemPerSlide - (totalItems - idx);
		for (var i=0; i<it; i++){
			if (e.direction=="left"){
				$('.carousel-item'.eq(i).appendTo('.carousel-inner');
			}
			else{
				$('.carousel-item').eq(0).appendTo('.carousel-inner');
			}
		}
	}
})

	$(#myCarousel).carousel ({
		interval:2000
	});

	$(document).ready(function(){
		$('a.thumb').click(function(event){
			event.preventDefault();
			var content = $('.modal-body');
			content.empty();
			var title = $(this).attr("title");
			$('.modal-title').html(title);
			content.html($(this).html());
			$(".modal-profile").modal({show:true});
		});
	});
	</script>