# -*- coding: utf-8 -*-
<%include file="header.tpl"/>

	<div id="content">
		<div class="padder">

		<div class="page" id="blog-latest">
        <h3 class="pagetitle">${author.username | h}</h3>
        
        <p>${author.content}</p>
  
        <h3 class="pagetitle">email : ${author.email.replace( '@', ' [at] ' ).replace( '.', ' [dot] ')}</h3>

        <h3 class="pagetitle">Ha scritto ${len(author.items)} articoli:</h3>
				% for page in author.items:
					<div class="post" id="post">
						<div class="post-content">
							<h2 class="posttitle"><a href="${config.siteurl}${page.url}" rel="bookmark" title="${page.title | h}">${page.title | h}</a></h2>

							<p class="date">il ${page.datetime.strftime("%d/%m/%Y")} alle ${page.datetime.strftime("%H:%M:%S")}
                <em> in 
                % for cat in page.categories:
                  <a href='${config.siteurl}${cat.url}'>${cat.title | h}</a>&nbsp;
                %endfor
                </em>
                <br/><br/>
                <span class="tags">Tags: 
                % for tag in page.tags:
                  <a href='${config.siteurl}${tag.url}'>${tag.title | h}</a>&nbsp;
                %endfor
                </span>
              </p>
						</div>

					</div>
				% endfor

		</div>

		</div><!-- .padder -->
	</div><!-- #content -->
  
  <%include file="sidebar.tpl"/>

<%include file="footer.tpl"/>
