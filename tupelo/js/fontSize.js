console.log("fontSize.js is loaded");

// Load change font size function

// function increaseFontSizeBy100px() {
//     document.getElementById('a').style.fontSize = "100px";
// }

function increaseFontSizeBy1px() {
	console.log("executed")
    var id = document.getElementById('ap');
    var style = window.getComputedStyle(id, null).getPropertyValue('font-size');
    var currentSize = parseInt(style);
    currentSize++;
    document.getElementById('ap').style.fontSize = currentSize.toString();
}
