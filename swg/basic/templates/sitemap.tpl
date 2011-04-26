# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

<url> 
	<loc>${config.siteurl}${index.url}</loc> 
	<lastmod>${config.now.strftime("%Y-%m-%d")}</lastmod> 
	<changefreq>daily</changefreq> 
	<priority>1.0</priority> 
</url> 
%for pagen in range( 2, pages[0].author.npages + 1 ):
<url> 
  <loc>${config.siteurl}/index-${pagen}.${config.page_ext}</loc> 
  <lastmod>${config.now.strftime("%Y-%m-%d")}</lastmod> 
  <changefreq>daily</changefreq> 
  <priority>1.0</priority> 
</url> 
%endfor

<url> 
	<loc>${config.siteurl}${pages[0].author.url}</loc> 
	<lastmod>${config.now.strftime("%Y-%m-%d")}</lastmod> 
	<changefreq>daily</changefreq> 
	<priority>1.0</priority> 
</url> 
%for pagen in range( 2, pages[0].author.npages + 1 ):
<url> 
  <loc>${config.siteurl}/members/${pages[0].author.name}-${pagen}.${config.page_ext}</loc> 
  <lastmod>${config.now.strftime("%Y-%m-%d")}</lastmod> 
  <changefreq>daily</changefreq> 
  <priority>1.0</priority> 
</url> 
%endfor

%for category in categories:
<url> 
	<loc>${config.siteurl}${category.url}</loc> 
	<lastmod>${config.now.strftime("%Y-%m-%d")}</lastmod> 
	<changefreq>daily</changefreq> 
	<priority>1.0</priority> 
</url> 
%for pagen in range( 2, category.npages + 1 ):
<url> 
  <loc>${config.siteurl}/categories/${category.name}-${pagen}.${config.page_ext}</loc> 
  <lastmod>${config.now.strftime("%Y-%m-%d")}</lastmod> 
  <changefreq>daily</changefreq> 
  <priority>1.0</priority> 
</url> 
%endfor
%endfor

%for tag in tags:
<url> 
	<loc>${config.siteurl}${tag.url}</loc> 
	<lastmod>${config.now.strftime("%Y-%m-%d")}</lastmod> 
	<changefreq>daily</changefreq> 
	<priority>1.0</priority> 
</url> 
%for pagen in range( 2, tag.npages + 1 ):
<url> 
  <loc>${config.siteurl}/tags/${tag.name}-${pagen}.${config.page_ext}</loc> 
  <lastmod>${config.now.strftime("%Y-%m-%d")}</lastmod> 
  <changefreq>daily</changefreq> 
  <priority>1.0</priority> 
</url> 
%endfor
%endfor

%for page in pages:
<url> 
	<loc>${config.siteurl}${page.url}</loc> 
	<lastmod>${page.datetime.strftime("%Y-%m-%d")}</lastmod> 
	<changefreq>monthly</changefreq> 
	<priority>0.2</priority> 
</url> 
%endfor

</urlset>

