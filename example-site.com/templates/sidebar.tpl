# -*- coding: utf-8 -*-
<div id="sidebar">
	<div class="padder">

  <div id="text-6" class="widget widget_text">
    <h3 class="widgettitle">CERCA NEL SITO</h3>			
    <div class="textwidget">
      <center>
        <form method="GET" action="/">
          <input type="text" name="s"/>
        </form>
      </center>
     </div>
  </div>

  <div id="text-3" class="widget widget_text">
    <h3 class="widgettitle">Articoli Recenti</h3>
    <div class="textwidget">
      <ul>
        %for page in pages[0:10]:
          <li><a href="${config.siteurl}${page.url}" title="${page.title | h}">${page.title | h}</a></li>
        %endfor
      </ul>
    </div>
	</div>
  
  <div id="text-3" class="widget widget_text">
    <h3 class="widgettitle">Tags</h3>
    <div class="textwidget"> 
     %for i, tag in enumerate( tags[0:50] ):
        <a href="${config.siteurl}${tag.url}" class="tag-link" title="${len(tag.items)} argomenti">${tag.title | h}</a>
      %endfor
    </div>
	</div>

	</div><!-- .padder -->
</div><!-- #sidebar -->
