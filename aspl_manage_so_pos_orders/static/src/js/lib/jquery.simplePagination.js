/**
 * jquery.simplePagination.js
 * @version: v1.0.0
 * @author: Sebastian Marulanda http://marulanda.me
 * @see: https://github.com/smarulanda/jquery.simplePagination
 */

(function($) {

	$.fn.simplePagination = function(options) {
		
		var defaults = {
			perPage: 5,
			containerClass: '',
			previousButtonClass: '',
			nextButtonClass: '',
			previousButtonText: 'Previous',
			nextButtonText: 'Next',
			currentPage: 1,
		};
		
		$.fn.simplePagination.destroy = function(){
		}
		var settings = $.extend({}, defaults, options);

		return this.each(function() {
			var $rows = $('tbody tr', this);
			var pages = Math.ceil($rows.length/settings.perPage);
			
			var container = document.getElementById('pagination');
			var bPrevious = document.getElementById('previous');
			var bNext = document.getElementById('next');
			var bFirst = document.getElementById('first');
			var bLast = document.getElementById('last');
			var of = document.getElementById('text');
				
			bPrevious.innerHTML = settings.previousButtonText;
			bNext.innerHTML = settings.nextButtonText;

			container.className = settings.containerClass;
			bPrevious.className = settings.previousButtonClass;
			bNext.className = settings.nextButtonClass;

			bPrevious.style.marginRight = '8px';
			bPrevious.style.background = '#59697d';
			bPrevious.style.color = '#FFF';
			bNext.style.marginLeft = '8px';
			bNext.style.background = '#59697d';
			bNext.style.color = '#FFF';
			bFirst.style.marginRight = '8px';
			bFirst.style.background = '#59697d';
			bFirst.style.color = '#FFF';
			bLast.style.marginLeft = '8px';
			bLast.style.background = '#59697d';
			bLast.style.color = '#FFF';
			container.style.textAlign = "center";
			container.style.marginBottom = '20px';

			container.appendChild(bFirst);
			container.appendChild(bPrevious);
			container.appendChild(of);
			container.appendChild(bNext);
			container.appendChild(bLast);
			$('.sale-order-list-scroll').after(container);

			update();

			$(bNext).click(function() {
				if (settings.currentPage + 1 > pages) {
					settings.currentPage = pages;
				} else {
					settings.currentPage++;
				}

				update();
			});

			$(bPrevious).click(function() {
				if (settings.currentPage - 1 < 1) {
					settings.currentPage = 1;
				} else {
					settings.currentPage--;
				}

				update();
			});
			$(bFirst).click(function(){
				settings.currentPage = 1;
				update();
			});
			
			$(bLast).click(function(){
				settings.currentPage = pages;
				update();
			});

			
			function update() {
				var from = ((settings.currentPage - 1) * settings.perPage) + 1;
				var to = from + settings.perPage - 1;

				if (to > $rows.length) {
					to = $rows.length;
				}

				$rows.hide();
				$rows.slice((from-1), to).show();

				of.innerHTML = from + ' to ' + to + ' of ' + $rows.length + ' entries';

				if ($rows.length <= settings.perPage) {
					$(container).hide();
				} else {
					$(container).show();
				}
			}
		});

	}

	$.fn.orderPagination = function(options) {

		var defaults = {
			orderPerPage: 5,
			orderContainerClass: '',
			orderPreviousButtonClass: '',
			orderNextButtonClass: '',
			orderPreviousButtonText: 'Previous',
			orderNextButtonText: 'Next',
			orderCurrentPage: 1,
		};

		$.fn.orderPagination.destroy = function(){
		}
		var settings = $.extend({}, defaults, options);

		return this.each(function() {
			var $rows = $('tbody tr', this);
			var pages = Math.ceil($rows.length/settings.orderPerPage);

			var orderContainer = document.getElementById('order-pagination');
			var orderbPrevious = document.getElementById('order-previous');
			var orderbNext = document.getElementById('order-next');
			var orderbFirst = document.getElementById('order-first');
			var orderbLast = document.getElementById('order-last');
			var orderof = document.getElementById('order-text');

			orderbPrevious.innerHTML = settings.orderPreviousButtonText;
			orderbNext.innerHTML = settings.orderNextButtonText;

			orderContainer.className = settings.orderContainerClass;
			orderbPrevious.className = settings.orderPreviousButtonClass;
			orderbNext.className = settings.orderNextButtonClass;

			orderbPrevious.style.marginRight = '8px';
			orderbPrevious.style.background = '#59697d';
			orderbPrevious.style.color = '#FFF';
			orderbNext.style.marginLeft = '8px';
			orderbNext.style.background = '#59697d';
			orderbNext.style.color = '#FFF';
			orderbFirst.style.marginRight = '8px';
			orderbFirst.style.background = '#59697d';
			orderbFirst.style.color = '#FFF';
			orderbLast.style.marginLeft = '8px';
			orderbLast.style.background = '#59697d';
			orderbLast.style.color = '#FFF';
			orderContainer.style.textAlign = "center";
			orderContainer.style.marginBottom = '20px';

			orderContainer.appendChild(orderbFirst);
			orderContainer.appendChild(orderbPrevious);
			orderContainer.appendChild(orderof);
			orderContainer.appendChild(orderbNext);
			orderContainer.appendChild(orderbLast);
			$('.order-list-scroll').after(orderContainer);

			orderUpdate();

			$(orderbNext).click(function() {
				if (settings.orderCurrentPage + 1 > pages) {
					settings.orderCurrentPage = pages;
				} else {
					settings.orderCurrentPage++;
				}

				orderUpdate();
			});

			$(orderbPrevious).click(function() {
				if (settings.orderCurrentPage - 1 < 1) {
					settings.orderCurrentPage = 1;
				} else {
					settings.orderCurrentPage--;
				}

				orderUpdate();
			});
			$(orderbFirst).click(function(){
				settings.orderCurrentPage = 1;
				orderUpdate();
			});

			$(orderbLast).click(function(){
				settings.orderCurrentPage = pages;
				orderUpdate();
			});


			function orderUpdate() {
				var orderFrom = ((settings.orderCurrentPage - 1) * settings.orderPerPage) + 1;
				var orderTo = orderFrom + settings.orderPerPage - 1;

				if (orderTo > $rows.length) {
					orderTo = $rows.length;
				}

				$rows.hide();
				$rows.slice((orderFrom-1), orderTo).show();

				orderof.innerHTML = orderFrom + ' to ' + orderTo + ' of ' + $rows.length + ' entries';

				if ($rows.length <= settings.orderPerPage) {
					$(orderContainer).hide();
				} else {
					$(orderContainer).show();
				}
			}
		});

	}

}(jQuery));