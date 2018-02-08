JUPYTER_FULL = {
	'header' : """
		{% extends 'basic.tpl'%}
		{%- block header -%}
		<!DOCTYPE html>
		<html>
		<head>
		{%- block html_head -%}
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
		<script type="text/x-mathjax-config">
			MathJax.Hub.Config({
				tex2jax: {
						inlineMath: [ ['$','$'], ["\\(","\\)"] ],
						displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
						processEscapes: true,
						processEnvironments: true
				},
				// Center justify equations in code and markdown cells. Elsewhere
				// we use CSS to left justify single line equations in code cells.
				displayAlign: 'center',
				"HTML-CSS": {
						styles: {'.MathJax_Display': {"margin": 0}},
						linebreaks: { automatic: true }
				}
			});
		</script>
		{%- endblock html_head %}
	""",
	'headerjs':"""
		<link rel="stylesheet" href="{tupelo_dir}/css/jupyter.css" media="all">
		<link rel="stylesheet" href="{tupelo_dir}/css/googlefonts.css">
		<link rel="stylesheet" href="{tupelo_dir}/css/default.css" media="all">
	""",
	'bodyheader': """
		</head>
		{%- endblock header -%}
		{% block body %}
		<body>
			 <button onclick="topFunction()" id="toTop" title="Go to top">Top</button>
		<div class = "wrapper">
		<header class="header">
		<nav class="nav">
	""",
	'bodylogo':"""
		<a href="{dst_folder}/index.html" class="nav-logo">
		<img src="{tupelo_dir}/images/tupelo.png"
						 width="75px"
						 height="75px"
						 alt="home_logo">
		</a>
		<ul class="nav-links">
	""",
	'navlinks':"""			
		<li><a href="index.html#{category}">{category}</a></li>			
	""",
	'content':"""
		</ul>
		</nav>
		</header>
		</div>
		<main class="content" role="main">
			<div tabindex="-1" id="notebook" class="border-box-sizing">
				<div class="container" id="notebook-container">
		{{ super() }}
				</div>
			</div>
		</main>
		</body>
	""",
	'bodyjs':"""
		<script src="{tupelo_dir}/js/scrollsTop.js"></script>
	""",
	'footer':"""
		{%- endblock body %}
		{% block footer %}
		{{ super() }}
			<footer class="footer">
				<span>Cogito ergo sum.</span>
			</footer>
		</html>
		{% endblock footer %}
	"""
}






