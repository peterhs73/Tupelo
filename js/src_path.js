// the script aims to fix issues of the image link problem
console.log("src_path.js is loaded");
// var src_folder = document.head.querySelector("[name=src]").content;
var tupelo_images = document.getElementsByTagName("img");
var tupelo_links = document.getElementsByTagName("a");
var src_folder = document.head.querySelector("[name=src_folder]").content;
var dst_folder = document.head.querySelector("[name=dst_folder]").content;

try {
	for (var i = 1; i < tupelo_images.length; i++) { //starts with i = 1 to avoid the logo.png image
        var images_dst =  tupelo_images[i].src;
        if (!images_dst.startsWith("http://") && !images_dst.endsWith("https://")){
        var images_src = images_dst.replace(dst_folder, src_folder);
        tupelo_images[i].src = images_src;
        }
    }

    for (var i = 3; i < tupelo_links.length; i++) { //avoid the first three links (1.logo link, 2.sidenav_pt 3.javascript:void(0))
        console.log(tupelo_links[i].hash);
        console.log(tupelo_links[i].href);
        if (tupelo_links[i].hash == ""){
            var link_dst = tupelo_links[i].href;
            if (!link_dst.endsWith("https://") && !link_dst.startsWith("http://")){
            var link_src = link_dst.replace(dst_folder, src_folder);
            tupelo_links[i].href = link_src;
            }
        }
    }
} catch(err) {
	console.log("src_path.js went wrong, cannot redirect path");
}
