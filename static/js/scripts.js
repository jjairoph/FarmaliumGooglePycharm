$(window).load(function() {
  $('.banner').unslider({
        fluid: true,
        dots: true,
        speed: 500,
        delay: 4000
      });
  if(window.chrome) {
        $('.banner li').css('background-size', '100% 100%');
      }
});

$(function() {
  var pull = $('#pull');
  var menu = $('nav ul');
        
          $(pull).on('click', function(e) {
              e.preventDefault();
              menu.slideToggle();
          });
      });
$(window).resize(function(){
  var menu = $('nav ul');
  var w = $(window).width();
    if(w > 320 && menu.is(':hidden')) {
          menu.removeAttr('style');
        }
      });

$(document).ready(function(){
 
var counter = 0,
$items = $('.slideshow figure'),
numItems = $items.length;
 
var showCurrent = function(){
var itemToShow = Math.abs(counter%numItems);
$items.removeClass('show');
$items.eq(itemToShow).addClass('show');
};
 
$('.next').on('click', function(){
counter++;
showCurrent();
});
 
$('.prev').on('click', function(){
counter--;
showCurrent();
});
 
});

$(document).ready(function(){
 
var counter = 0,
$items = $('.quote-slideshow figure'),
numItems = $items.length;
 
var showCurrent = function(){
var itemToShow = Math.abs(counter%numItems);
$items.removeClass('show');
$items.eq(itemToShow).addClass('show');
};
 
$('.quote-next').on('click', function(){
counter++;
showCurrent();
});
 
$('.quote-prev').on('click', function(){
counter--;
showCurrent();
});
 
});




 
jQuery.fn.animateAuto = function(prop, speed, callback){
   var elem, height, width;
   return this.each(function(i, el){
      el = jQuery(el), elem = el.clone().css({"height":"auto","width":"auto"}).appendTo("body");
      height = elem.css("height"),
      width = elem.css("width"),
      elem.remove();
      if(prop === "height")
         el.animate({"height":height}, speed, callback);
      else if(prop === "width")
         el.animate({"width":width}, speed, callback);  
      else if(prop === "both")
         el.animate({"width":width,"height":height}, speed, callback);
   });  
}
$(window).ready(function(){
   $('section').click(function(){
      if($(this).next().hasClass('desplegado')){
         $(this).next().removeClass('desplegado').animate({height:0},500);
      }else{
         $(this).next().addClass('desplegado').animateAuto("height",500);
      }
   })
})

$(".animateHeight").bind("click", function(e){
    $(".test").animateAuto("height", 1000); 
});

$(".animateWidth").bind("click", function(e){
    $(".test").animateAuto("width", 1000); 
});

$(".animateBoth").bind("click", function(e){
    $(".test").animateAuto("both", 1000); 
});
