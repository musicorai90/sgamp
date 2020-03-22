if (window.location.pathname == '/') {
    document.getElementById('f-back-btn').style.display = 'none'
}

$(document).ready(function(){
    $('.NavLateral-DropDown').on('click', function(e){
        e.preventDefault();
        var DropMenu=$(this).next('ul');
        var CaretDown=$(this).children('i.NavLateral-CaretDown');
        DropMenu.slideToggle('fast');
        if(CaretDown.hasClass('NavLateral-CaretDownRotate')){
            CaretDown.removeClass('NavLateral-CaretDownRotate');    
        }else{
            CaretDown.addClass('NavLateral-CaretDownRotate');    
        }
         
    });
    $('.tooltipped').tooltip({delay: 50});
    $('.ShowHideMenu').on('click', function(){
        var MobileMenu=$('.NavLateral');
        if(MobileMenu.css('opacity')==="0"){
            MobileMenu.addClass('Show-menu');   
        }else{
            MobileMenu.removeClass('Show-menu'); 
        }   
    }); 
    $('.btn-ExitSystem').on('click', function(e){
        e.preventDefault();
        swal({ 
            title: "¿Está seguro de salir?",   
            //text: "The current session will be closed and will leave the system",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#1b5e20",   
            confirmButtonText: "Sí",
            animation: "slide-from-top",   
            closeOnConfirm: false,
            cancelButtonText: "No"
        }, function(){   
            window.location='/logout'; 
        });
    });
    $('#solicitud-acep').on('click', function(e){
        e.preventDefault();
        swal({ 
            title: "¿Está seguro?",   
            //text: "The current session will be closed and will leave the system",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#1b5e20",   
            confirmButtonText: "Sí",
            animation: "slide-from-top",   
            closeOnConfirm: false,
            cancelButtonText: "No"
        }, function(){
            document.getElementById('id_status').selectedIndex = '0';
            document.getElementById('f-btn-submit').click(); 
        });
    });
    $('.btn-Search').on('click', function(e){
        e.preventDefault();
        swal({   
            title: "What are you looking for?",   
            text: "Write what you want",   
            type: "input",   
            showCancelButton: true,   
            closeOnConfirm: false,   
            animation: "slide-from-top",   
            inputPlaceholder: "Write here",
            confirmButtonText: "Search",
            cancelButtonText: "Cancel" 
        }, function(inputValue){   
            if (inputValue === false) return false;      
            if (inputValue === "") {     swal.showInputError("You must write something");     
            return false   
            }      
            swal("Nice!", "You wrote: " + inputValue, "success"); 
        });    
    });
    $('.btn-Notification').on('click', function(){
        var NotificationArea=$('.NotificationArea');
        if(NotificationArea.hasClass('NotificationArea-show')){
            NotificationArea.removeClass('NotificationArea-show');
        }else{
            NotificationArea.addClass('NotificationArea-show');
        }
    });     
});
(function($){
    $(window).load(function(){
        $(".NavLateral-content").mCustomScrollbar({
            theme:"light-thin",
            scrollbarPosition: "inside",
            autoHideScrollbar: true,
            scrollButtons:{ enable: true }
        });
        $(".ContentPage, .NotificationArea").mCustomScrollbar({
            theme:"dark-thin",
            scrollbarPosition: "inside",
            autoHideScrollbar: true,
            scrollButtons:{ enable: true }
        });
    });
})(jQuery);

function verVisibles() {
    var inputs = document.getElementById('f-galeria-inputs').children;
    var fotos = document.getElementsByClassName('nGY2GThumbnail');
    for (var i = inputs.length - 1; i >= 0; i--) {
        fotos[i].appendChild(inputs[i]);
    }
    document.getElementById('f-galeria-guardar').style.display = "inline-block";
    var newInputs = document.getElementsByClassName('f-galeria-input');
    console.log(newInputs);
    for (var i = newInputs.length - 1; i >= 0; i--) {
        newInputs[i].addEventListener('click',function() {
            //console.log('Hola');
        });
    }
}