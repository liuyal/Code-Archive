  // Scrolling Effect
  /* $(window).on("scroll", function () {
       if ($(window).scrollTop()) {
           $('nav').addClass('black');
       } else {
           $('nav').addClass('black');
       }
   })*/

  window.onload = function () {
      $('#logoJL').hide();
      setTimeout(function () {
          $('body').addClass('loaded');
          $('h1').css('color', '#222222');
          $('nav').addClass('black');
          $('#logoJL').fadeIn('slow');
      }, 4000);
  };

  $(document).ready(function () {
      $(this).scrollTop(0);
      setTimeout(function () {
          $('body').addClass('loaded');
          $('h1').css('color', '#222222');
      }, 3000);

      $(".menu-icon").on("click", function () {
          $("nav ul").toggleClass("showing");
      });
  });

  $(document).ready(function () {
      $("a").on('click', function (event) {
          if (this.hash !== "") {
              event.preventDefault();
              var hash = this.hash;
              $('html, body').animate({
                  scrollTop: $(hash).offset().top
              }, 750, function () {
                  window.location.hash = hash;
              });
          }
      });
  });


  $(document).scroll(function () {
      // Where's the scroll at?
      var currentPosition = $(this).scrollTop();

      // Remove highlights from all
      $('a[href*=#]').removeClass('highlighted');

      // Loop over each section
      $('.section').each(function () {
          // Calculate the start and end position of the section
          var sectionStart = $(this).offset().top;
          var sectionEnd = sectionStart + $(this).height();

          // If the current scroll lies between the start and the end of this section

          if (currentPosition >= sectionStart && currentPosition < sectionEnd) {
              // Highlight the corresponding anchors
              $('a[href=#' + $(this).attr('id') + ']').addClass('highlighted');
          }
          
      });
  });
