window.onscroll = function() {headerSticky()}

function headerSticky() {
	if (window.pageYOffset > 0) {
		document.getElementById('lan-header').classList.add('sticky');
		document.getElementById('lan-btn-sticky').style.display = "inline-block";
		setTimeout(function() {
			document.getElementById('lan-btn-sticky').style.opacity = "1";
		},1);
	} else {
		document.getElementById('lan-header').classList.remove('sticky');
		document.getElementById('lan-btn-sticky').style.opacity = "0";
		setTimeout(function() {
			document.getElementById('lan-btn-sticky').style.display = "none";
		},300);
	}
}

var lanFotos = document.getElementById('lan-galeria-fotos');
var lanFotosTotal = 12;
for (var i = lanFotos.children.length - 1; i >= 0; i--) {
	if (lanFotos.children[i].tagName == 'IMG') {
		lanFotosTotal += lanFotos.children[i].offsetWidth + 12;		
	}
}

if (lanFotosTotal > lanFotos.offsetWidth) {
	document.getElementById('lan-galeria-fotos-next').classList.add('active');
}

function lanFotosNext() {
	if (!document.getElementById('lan-galeria-fotos-back').classList.contains('active')) {
		document.getElementById('lan-galeria-fotos-back').classList.add('active');
	}
	var elem = document.getElementById('lan-galeria-fotos');
	document.getElementById('lan-galeria-fotos-next').classList.remove('active');
	if (elem.clientWidth * 2 >= elem.scrollWidth) {
		var elemTrasl = elem.lastElementChild.style.transform;
		if (elemTrasl) {
			var lista = elemTrasl.split("(");
			var pixeles = (elem.scrollWidth - elem.clientWidth) + Number(lista[1].slice(1,lista[1].length - 3));
		} else {
			var pixeles = elem.scrollWidth - elem.clientWidth;
		}
	} else {
		var elemTrasl = elem.lastElementChild.style.transform;
		if (elemTrasl) {
			document.getElementById('lan-galeria-fotos-next').classList.add('active');
			var lista = elemTrasl.split("(");
			var pixeles = Number(lista[1].slice(1,lista[1].length - 3)) + elem.clientWidth;
		} else {
			document.getElementById('lan-galeria-fotos-next').classList.add('active');
			var pixeles = elem.clientWidth;
		}		
	}
	for (var i = elem.children.length - 1; i >= 0; i--) {
		if (elem.children[i].tagName == 'IMG') {
			elem.children[i].style.transform = "translateX(-"+pixeles+"px)";
		}
	}
}

function lanFotosBack() {
	document.getElementById('lan-galeria-fotos-back').classList.remove('active');
	if (!document.getElementById('lan-galeria-fotos-next').classList.contains('active')) {
		document.getElementById('lan-galeria-fotos-next').classList.add('active');
	}
	var elem = document.getElementById('lan-galeria-fotos');
	for (var i = elem.children.length - 1; i >= 0; i--) {
		if (elem.children[i].tagName == 'IMG') {
			elem.children[i].style.transform = "";
		}
	}
}