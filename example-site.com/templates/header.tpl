# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head profile="http://gmpg.org/xfn/11">
		<meta http-equiv="Content-type" content="text/html; charset=${config.charset}" />
    <meta http-equiv="Content-language" content="${config.language}" />
  
		<title>
    %if page != UNDEFINED and page.title != 'index':
      ${config.sitename | h} | ${page.title | h}
    %elif category != UNDEFINED:
      ${config.sitename | h} | ${category.title | h}
    %elif tag != UNDEFINED:
      ${config.sitename | h} | ${tag.title | h}
    %elif author != UNDEFINED:
      ${config.sitename | h} | ${author.username | h}
    %else:
      ${config.sitename | h}
    %endif
    </title>

    <meta name="keywords" content="${', '.join( config.keywords )}" />

		<meta name="generator" content="SWG ${config.version}" />

		<link rel="stylesheet" href="${config.siteurl}/css/style.css" type="text/css" media="screen" /> 
    <link rel="alternate" type="application/rss+xml"  href="${config.siteurl}/feed.xml" title="${config.sitename | h} RSS Feeds">

	</head>

	<body class="logged-in single single-post" id="bp-default">
		<div id="header">
			<h1 id="logo"> <span style='text-shadow: #3DBEDD 0px 0px 15px; font-size:14px; font-weight:normal; '>My kung-fu is stronger than yours!</span></h1>
			<ul id="nav">
				<li
        %if page != UNDEFINED and page.title == 'index':
          class="selected"  
        %endif    
        >  
          <a href='${config.siteurl}/index.${config.page_ext}'>Home</a>
        </li>
        %for cat in categories:
          %if category != UNDEFINED and category.title == cat.title:
            <li class="selected"><a href="${config.siteurl}${cat.url}" title="Visualizza tutti gli articoli archiviati in ${cat.title | h}">${cat.title | h}</a></li> 
          %else:
            <li class="cat-item"><a href="${config.siteurl}${cat.url}" title="Visualizza tutti gli articoli archiviati in ${cat.title | h}">${cat.title | h}</a></li> 
          %endif
        %endfor

        <li
        %if author != UNDEFINED:
          class="selected"  
        %endif    
        >  
          <a href='${config.siteurl}/members/example-author.${config.page_ext}'>About Me</a>
        </li>
			</ul>
		</div>

		<div id="container">
