# -*- coding: utf-8 -*-
<%include file="header.tpl"/>
  <div class="post post-index" id="post" >
  <h2 class="entry-title index-entry-title">${page.title | h}</h2>        
                  
  <div class="additional-meta">
    <div class="meta-date" >
      <span class="date">${page.datetime.strftime("%d/%m/%Y")}</span> 
      <span class="author"> Posted by <a href='${config.siteurl}${page.author.url}' title="${page.author.username | h}">${page.author.username | h}</a></span>  
    </div>        
    <div class="clear"></div>
  </div>
	
  <div class="entry-content entry-content-index">
    ${page.content}
  </div>

  <div class="entry-meta">
    <div class="meta_bot">
      <span class="category">Categories: 
      % for i, c in enumerate( page.categories ):
        <a href='${config.siteurl}${c.url}'>${c.title | h}</a>
        % if i != len(page.categories) - 1:
        ,
        % endif
      % endfor
      </span>
      <br/>
      <span class="tag">Tags: 
      % for i, t in enumerate( page.tags ):
        <a href='${config.siteurl}${t.url}'>${t.title | h}</a>
        % if i != len(page.tags) - 1:
        ,
        % endif
      % endfor
      </span>
    </div>

    <div  class="more"><a href="${config.siteurl}${page.url}" rel="bookmark" title="Permanent Link to ${page.title | h}" >Read More</a></div>
    <div class="clear"></div>
    </div>
  </div>
 
<%include file="footer.tpl"/>
