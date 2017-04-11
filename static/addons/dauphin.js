    /** Dauphin - Premium Responsive Bootstrap Admin Template **/

    "use strict"

    //Shrink/enlarge left navigation menu if width < 1024px 
    if ($(window).width() < 768) {
        $("body").removeClass("left-nav-minimized");
    } else if ($(window).width() < 1024) {
        $("body").addClass("left-nav-minimized");
    } else {
        $("body").removeClass("left-nav-minimized");
    }

    //Document ready functions
    $(document).ready(function () {

        //Shrink/enlarge left navigation menu if width < 1024px (on resize)
        $(window).on('resize', function() {
            if ($(window).width() < 768) {
                $("body").removeClass("left-nav-minimized");
            } else if ($(window).width() < 1024) {
                $("body").addClass("left-nav-minimized");
            } else {
                $("body").removeClass("left-nav-minimized");
            }
        });

        // Remove transition hold (fix IE rendering bug)
        $('body').removeClass('hold-transition');


        // Breadcrumb slide in effect
        function breadcrumb(){
            $('.breadcrumb li:last-child a', '.navbar').css({'opacity' : '1', 'margin-left' : "0px"});
        }; 

        // Call breadcrumb slide in effect
        $('body').delay(200).queue(function(){
            breadcrumb();
            $(this).dequeue();
        });

        // Toggle left navigation menu
        $('.left-nav-toggle', '.navigation').on('click', function(event){
            event.preventDefault();
            $("body").toggleClass("left-nav-minimized");
        });

        // Set left navigation menu item active on page load/refresh
        var checkActive = function(){
            var path = window.location.href,
                path = decodeURI(path),
                firstIndex = path.lastIndexOf('/'),
                path = path.substring(firstIndex, path.length).slice(1)

            if ( window.location.pathname.indexOf(path) > -1 ) {
                $('.navigation .nav li a[href="'+path+'"]').parent().addClass('active');
                $('.navigation .nav li a:not([href="'+path+'"])').parent().removeClass('active');
            }
        };

	    checkActive();   

        // Keep left navigation menu item expanded and active if child is active;
        var primaryLi = function() {
	        if ($('.primary li', '.navigation').hasClass('active')) {
	        	$('.primary li.active', '.navigation').parentsUntil('.primary').addClass('in');
	        }
	    };

		primaryLi();

        // Sidebar time
        if ($('.time', '.navigation').length > 0) {
            var datetime = null,
            	datetime1 = null,
                date = null;
            var update = function () {
                var d = new Date(),
                date = moment(new Date());
                datetime.html(date.format('LL '));
            };
            datetime = $('.current-time')
            update();
            setInterval(update, 60000);

            var update = function () {
                var date = moment(new Date());
                datetime1.html(date.format('h:mm a'));
            };
            datetime1 = $('.current-time2')
            update();
            setInterval(update, 10000);

            $('.time', '.navigation').on('click', function(){
                $(this).toggleClass('non-visible');
            });
        }


        //Scroll up button
        var scrollUp = $('.scroll-up');

        if (scrollUp.length > 0) {
            $(document).scroll(function(){
                if($('body').scrollTop() > 200) {
                    scrollUp.addClass('active');
                    scrollUp.on('click', function(){
                        $('body').stop().animate({scrollTop:0}, 150, 'swing');
                    });
                } else {
                    scrollUp.removeClass('active');
                }
            });
        }


        // Panels drag, collapse and close; 
        // Messages categories toggle active, New message create and close 
        var panelActions = function(){

	        // Toggle Panel
	        $('.panel-toggle').on('click', function(event){
	            event.preventDefault();
	            var panel = $(event.target).closest('div.panel');
	            var icons = $(event.target).closest('i');
	            var body = panel.find('div.panel-body');
	            var footer = panel.find('div.panel-footer');
	            body.slideToggle(200);
	            footer.slideToggle(100);

	            // Toggle icon from up to down
	            icons.toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
	            panel.toggleClass('').toggleClass('panel-collapse');
	            setTimeout(function () {
	                panel.resize();
	            }, 15);
	        });

	        // Close Panel
	        $('.panel-close').on('click', function(event){
	            event.preventDefault();
	            var panel = $(event.target).closest('div.panel');
	            panel.remove();
	        });

	        // Draggable panels

	        var element = ".draggable";
	        var handle = ".panel-heading";
	        var connect = ".draggable";
	        $(element).sortable(
	                {
	                    handle: handle,
	                    connectWith: connect,
	                    tolerance: 'pointer',
	                    forcePlaceholderSize: true,
	                    opacity: 0.8,
	                    placeholder: 'sortable-placeholder',
			            start: function(e, ui){
				                if($(this).children().hasClass('panel')){
				                	$('.sortable-placeholder').css('margin-bottom', '20px');
				                } else {
				                    $('.sortable-placeholder').html($(this).children());
				                }
			            	}
			            })
	                .disableSelection();

            // Messages categories toggle
            $(".inbox-categories div", '.messages-panel').on('click', function(){
                $(this).addClass('active');
                $(this).siblings().removeClass('active');
            });

            // New message show and close 
            $('.new-message', '.messages-panel').on('click', function(){
                $(this).next('.new-message-wrapper').show();
            });

            $('.close-new-message', '.messages-panel').on('click', function(){
                event.preventDefault();
                var panel = $(event.target).closest('.new-message-wrapper');
                panel.hide();
	        });
        };

        panelActions();

        //Timeline collapse hide/show middle line
        $('.timeline-content.collapse:not(.in)').closest('.timeline').addClass('no-line');

        $('.timeline-heading', '.timeline').on('click', function(){
            if ($(this).closest('.timeline').hasClass('no-line')){
                $(this).closest('.timeline').removeClass('no-line');
            } else {
                $(this).closest('.timeline').addClass('no-line');
            }
        });

        //Button to previous page
        $('.previous-page').click(function(){
            parent.history.back();
            return false;
        });
    });
