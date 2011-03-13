# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

<url> 
	<loc>${config.siteurl}/</loc> 
	<lastmod>${config.now}</lastmod> 
	<changefreq>daily</changefreq> 
	<priority>1.0</priority> 
</url> 

<url> 
	<loc>${config.siteurl}/${pages[0].author.url}</loc> 
	<lastmod>${config.now}</lastmod> 
	<changefreq>daily</changefreq> 
	<priority>1.0</priority> 
</url> 

%for category in categories:
<url> 
	<loc>${config.siteurl}/${category.url}</loc> 
	<lastmod>${config.now}</lastmod> 
	<changefreq>daily</changefreq> 
	<priority>1.0</priority> 
</url> 
%endfor

%for tag in tags:
<url> 
	<loc>${config.siteurl}/${tag.url}</loc> 
	<lastmod>${config.now}</lastmod> 
	<changefreq>daily</changefreq> 
	<priority>1.0</priority> 
</url> 
%endfor

%for page in pages:
<url> 
	<loc>${config.siteurl}/${page.url}</loc> 
	<lastmod>${page.datetime}</lastmod> 
	<changefreq>monthly</changefreq> 
	<priority>0.2</priority> 
</url> 
%endfor

</urlset>

