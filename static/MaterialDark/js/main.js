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
            document.getElementById('id_status').selectedIndex = '2';
            document.getElementById('f-btn-submit').click(); 
        });
    });
    $('#solicitud-actu').on('click', function(e){
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
    $('#bien-acep').on('click', function(e){
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
            document.getElementById('id_nucleo').selectedIndex = '2';
            document.getElementById('f-btn-submit').click(); 
        });
    });
    $('#desincorporacion-rech').on('click', function(e){
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
            document.getElementById('id_status').selectedIndex = '2';
            document.getElementById('f-btn-submit').click(); 
        });
    });
    $('#desincorporacion-acep').on('click', function(e){
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
    $('#pro-acep').on('click', function(e){
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
            document.getElementById('id_tipo').selectedIndex = '2';
            document.getElementById('f-btn-submit').click(); 
        });
    });
    $('#alu-acep').on('click', function(e){
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
            document.getElementById('id_tipo').selectedIndex = '1';
            document.getElementById('f-btn-submit').click(); 
        });
    });
    $('#asig-acep').on('click', function(e){
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
            document.getElementById('f-btn-submit').click(); 
        });
    });
    $('#part-acep').on('click', function(e){
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
            document.getElementById('f-btn-submit').click(); 
        });
    });
    $('#main-acep').on('click', function(e){
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
            document.getElementById('f-btn-submit').click(); 
        });
    });
    $('#cambiar-acep').on('click', function(e){
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
            document.getElementById('f-btn-submit').click(); 
        });
    });
    $('#modificar-acep').on('click', function(e){
        e.preventDefault();
        swal({ 
            title: "¿Está seguro?",   
            //text: "The current session will be closed and will leave the system",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#1b5e20",   
            confirmButtonText: "Sí",
            animation: "slide-from-top",   
            closeOnConfirm: true,
            cancelButtonText: "No"
        }, function(){
            if (document.getElementById('id_telefono').value.length < 12) {
                alert('El teléfono es incompleto');
            } else {
                document.getElementById('f-btn-submit').click(); 
            }        
        });
    });
    $('#pass-acep').on('click', function(e){
        e.preventDefault();
        swal({ 
            title: "¿Está seguro?",   
            //text: "The current session will be closed and will leave the system",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#1b5e20",   
            confirmButtonText: "Sí",
            animation: "slide-from-top",   
            closeOnConfirm: true,
            cancelButtonText: "No"
        }, function(){
            if (document.getElementById('log-form-password-2').value != document.getElementById('log-form-password-3').value) {
                alert('La confirmación de contraseña es incorrecta.');
            } else {
                document.getElementById('orq-form').submit();
            }
        });
    });
    $('#eliminar-coordinador').on('click', function(e){
        e.preventDefault();
        swal({ 
            title: "¿Está seguro?",   
            //text: "The current session will be closed and will leave the system",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#1b5e20",   
            confirmButtonText: "Sí",
            animation: "slide-from-top",   
            closeOnConfirm: true,
            cancelButtonText: "No"
        }, function(){
            document.getElementById('f-btn-submit').click(); 
        });
    });
    $('#nuevo-coordinador').on('click', function(e){
        e.preventDefault();
        swal({ 
            title: "¿Está seguro?",   
            //text: "The current session will be closed and will leave the system",   
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#1b5e20",   
            confirmButtonText: "Sí",
            animation: "slide-from-top",   
            closeOnConfirm: true,
            cancelButtonText: "No"
        }, function(){
            if (document.getElementById('id_telefono').value.length < 12) {
                alert('El teléfono es incompleto');
            } else {
                document.getElementById('f-btn-submit').click(); 
            }
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

function changeToInput(padre,num) {
    for (var i = padre.children.length - 1; i >= 0; i--) {
        padre.removeChild(padre.children[i]);
        padre.innerHTML = `
            <input placeholder="Nombre" type="text" id="bien-nuevo-${num}" name="bien-nuevo-${num}" class="validate" autofocus required>
            <label>Nuevo bien</label>
        `
    }
}