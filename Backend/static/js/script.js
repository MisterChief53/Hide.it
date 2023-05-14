class item {
    constructor(id, selected) {
        this.id = id;
        this.selected = selected;
    }

    clic1() {
        this.selected = true;
        document.getElementById("itOne").style.border = "solid white";
    }

    clic2() {
        this.selected = true;
        document.getElementById("itOne").style.border = "none";
    }
}

function verificarArchivo() {
    var archivoInput = document.getElementById('archivo');
    var archivoSeleccionado = archivoInput.files[0];

    if (archivoSeleccionado) {
        // console.log('Se ha seleccionado un archivo:', archivoSeleccionado.name);
        document.getElementById("videUploaded").style.display = "flex";
        document.getElementById("selectHide").style.display = "flex";
        document.getElementById("newVideo").style.display = "flex";
    }
}

function clicItem(id) {
    var itemX;
    itemX = new item(id, selected);

    // no supe cómo hacerlo con los items dinámicos
}