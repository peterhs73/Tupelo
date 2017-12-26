// the script aims to fix issues of the image link problem
console.log("localpath.js is loaded");
var check_images = document.getElementsByTagName("img");
var check_links = document.getElementsByTagName("a");
try {
    var base_url_name = window.location.pathname.substring(1);
    var base_url = base_url_name.split("/");
    var base_dir = "/";
	for (i = 0; i < base_url.length - 2; i++) { // the split function returns two empty strings and need to get rid of the last path 
  		base_dir += base_url[i];
  		base_dir += "/";
	}
    	for (var i = 0; i < check_images.length; i++) {
           var src_var =  check_images[i].src;
           if (src_var.startsWith("http://localhost") && !src_var.endsWith('logoc.png')){
        	  console.log(src_var)
            var src_short = src_var.replace("http://localhost:1313/","").replace(base_url_name,"");
        	  console.log(src_short)
            var src_new = base_dir + src_short;
            console.log(src_new)
            check_images[i].src = src_new;
            console.log(check_images[i].src)
            }
        }

        for (var i = 0; i < check_links.length; i++) {
           var link_var =  check_links[i].href;
           if (link_var.startsWith("http://localhost")){
               var link_short = link_var.replace("http://localhost:1313/","").replace(base_url_name,"");
               if (!link_short.startsWith("/") && !link_short.startsWith("#") && !link_short.length == 0){
                  var link_new = base_dir + link_short;
                  check_links[i].href = link_new;
                }
            }
        }
} catch(err) {
	console.log("some error");
}