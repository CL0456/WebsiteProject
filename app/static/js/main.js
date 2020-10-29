$(document).ready(function(){
	
	var $grid = $('.grid').masonry({
		gutter: 30
	});
	
	// layout Masonry after each image loads //
	$grid.imagesLoaded().progress( function() {
		$grid.masonry('layout');
	});

	// Code for liking system //
	$('i.like').click(function(e) {
	
		e.stopPropagation();
		e.preventDefault();
	
		var like = $(this).hasClass('far');
		var image_id = $(this).data('image');
		var _this = $(this);
	
		//our ajax call
		$.getJSON(
			$SCRIPT_ROOT + '/like',
			{
				like: like,
				image_id: image_id
			}, 
			function(result) {
				if (result) {
					if (like) {
						_this.removeClass('far');
						_this.addClass('fas');
					} else {
						_this.removeClass('fas');
						_this.addClass('far');
					}
				}
			}
		);
		return false;
	});

	// Code for pop-ups//
	$('.grid-item figure').click(function(){
		//Fetch image data
		var image_data = $(this).closest('.grid-item').data(image);
		var image = image_data.image;
	
		//Build HTML from image data//
		var description = `<p>${image.description}</p>`;
		var title = `<h5 class="modal-title">${image.name}<i class="fa fa-times" class="close" data-dismiss="modal" aria-label="Close" aria-hidden="true"></i></h5>`;
		var img = ` <figure class="filter-${image.filter}">
						<img class="modal-img" src="${iamge.upload_location}" alt="${image.name}, ${image.description}">
					</figure>`;
	
		//Add to modal and open modal//
		$('#image-modal .modal-body').html(img + title + description);
		$('.modal').modal('show');
	});
	// Loads correct selected value for filter //
	if ($('#filter-select').length > 0 ) {
		var filter = $('#filter-select').data('filter');
		$('#filter-select').val(filter);
	}
	// Loads correct selected value for category //
	if ($('#category').length > 0 ) {
		var category = $('#category').data('category');
		$('#category').val(category);
	}
	// Alters live preview of Filter //
	$('#filter-select').change(function(e) {
		var new_filter = 'filter-' + this.value;
		$('#image figure').removeClass();
		$('#image figure').addClass(new_filter);
	});

});