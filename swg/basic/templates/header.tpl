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

    %if pager != UNDEFINED and pager.getTotalPages() > 2 and pager.getCurrentPageNumber() != 1:
      | Page ${pager.getCurrentPageNumber()} 
    %endif
    </title>

    %if page != UNDEFINED and page.title != 'index':
      <meta name="keywords" content="${ ', '.join( [ t.title for t in page.tags ] ) }" />
      <%
        import re

        description = re.sub( r'<[^>]*?>', ' ', page.content ).strip()[:150]
      %>
      <meta name="description" content="${description | h}" />  
    %else:
      <meta name="keywords" content="${ ', '.join( config.keywords ) }" />
      <meta name="description" content="${config.sitename | h}" />
    %endif
    
    <meta name="generator" content="SWG ${config.version}" />

    <link rel="stylesheet" href="${config.siteurl}/css/style.css" type="text/css" media="screen" /> 
    <link rel="alternate" type="application/rss+xml"  href="${config.siteurl}feed.xml" title="${config.sitename | h} RSS Feeds" />
    <link rel='index' title="${config.sitename}" href="${config.siteurl}" />
    
    %if page != UNDEFINED and page.title != 'index':
      <link rel="canonical" href="${config.siteurl}${page.url}" />
    %endif
    </head>

    <body>
    <div id="wrapper">

    <div id="header2">
      <div id="header">
        <div id="logo">
          <h1 id="title"><a href="${config.siteurl}">${config.sitename | h}</a></h1>
        </div>
      </div>
    </div>

    <div class="container">

      <div id="mainmenu">
        <ul>
          <li
          %if page != UNDEFINED and page.title == 'index':
            class="cat-item current-cat"  
          %else:
            class="cat-item"
          %endif    
          >  
            <a href='${config.siteurl}/index.${config.page_ext}'>Home</a>
          </li>

          %for cat in categories:
            %if category != UNDEFINED and category.title == cat.title:
              <li class="cat-item current-cat"><a href="${config.siteurl}${cat.url}" title="View category ${cat.title | h} archive">${cat.title | h}</a></li> 
            %else:
              <li class="cat-item"><a href="${config.siteurl}${cat.url}" title="View category ${cat.title | h} archive">${cat.title | h}</a></li> 
            %endif
          %endfor

          <li
          %if author != UNDEFINED:
            class="cat-item current-cat"  
          %else:
            class="cat-item"
          %endif    
          >  
            <a href='${config.siteurl}/members/your-name-here.${config.page_ext}'>About Me</a>
          </li>

          <li
          %if page != UNDEFINED and page.title == 'Instructions':
            class="cat-item current-cat"  
          %else:
            class="cat-item"
          %endif    
          >  
            <a href='${config.siteurl}${swg.getPageByTitle('Instructions').url}'>Instructions</a>
          </li>

        </ul>
      </div>
      
      <div class="posts-wrap">
