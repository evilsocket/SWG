# -*- coding: utf-8 -*-
<%include file="header.tpl"/>
  <br/>
  <h2 class="archive-title">${author.username | h}</h2>


  <div class="entry-content entry-content-index">
    <img src="${author.avatar}" style="float:left; margin: 5px;" />
    ${author.content}
  </div>
  <div class="additional-meta"><b>email :</b> ${author.email.replace( '@', ' [at] ' ).replace( '.', ' [dot] ')}</div>
  
  <br/>
  <h3 class="entrytitle">I wrote ${len(author.items)} articles:</h3>
  <br/>
  % for page in pager.getCurrentPages( includeStatic = True ):
  <div class="post post-index" id="post" >
    <h2 class="entry-title index-entry-title"><a href="${config.siteurl}${page.url}" title="${page.title | h}">${page.title | h}</a> </h2>        
                    
    <div class="additional-meta">
      <div class="meta-date" >
        <span class="date">${page.datetime.strftime("%d/%m/%Y")}</span> 
        <span class="author"> Posted by <a href='${config.siteurl}${page.author.url}' title="${page.author.username | h}">${page.author.username | h}</a></span>  
      </div>        
      <div class="clear"></div>
    </div>
		
    <div class="entry-content entry-content-index">
      ${page.abstract}
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
      </div>

      <div  class="more"><a href="${config.siteurl}${page.url}" rel="bookmark" title="Permanent Link to ${page.title | h}" >Read More</a></div>
      <div class="clear"></div>
      </div>
    </div>
  % endfor

  % if pager.getTotalPages() > 1:
  <div id="pagenavi">
    <label>PAGES</label>
    % for pagen in range( 1, pager.getTotalPages() + 1 ):
      % if pagen == pager.getCurrentPageNumber():
        <b>${ pagen }</b>
      % elif pagen == 1:
        <a href='${config.siteurl}${author.url}'>${ pagen }</a>
      % else:
        <a href='${config.siteurl}/members/${author.name}-${pagen}.${config.page_ext}'>${ pagen }</a>
      % endif
    % endfor
  </div>
  % endif

<%include file="footer.tpl"/>
