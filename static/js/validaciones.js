function len8(e,id) {
    if (document.getElementById(id).value.length + 1 == 9 || e.key == 'e' || e.key == '+' || e.key == '-') {
        e.preventDefault();
    }
}