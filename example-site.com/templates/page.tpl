# -*- coding: utf-8 -*-
<%include file="header.tpl"/>
	<div id="content">
		<div class="padder">

		<div class="page" id="blog-single">

				<div class="post" id="post">

					<div class="author-box">
            <img src="${page.author.avatar}" alt="" class="avatar user-1-avatar" width="50" height="50">
						<p>by <a href='${config.siteurl}${page.author.url}'>${page.author.username}</a></p>
					</div>

					<div class="post-content">
					  <h2 class="posttitle"><a href="${config.siteurl}${page.url}" rel="bookmark" title="${page.title | h}">${page.title | h}</a></h2>

						<p class="date">il ${page.datetime.strftime("%d/%m/%Y")} alle ${page.datetime.strftime("%H:%M:%S")}
            <em> in 
            % for category in page.categories:
              <a href='${config.siteurl}${category.url}'>${category.title | h}</a>&nbsp;
            %endfor
            </em>
            </p>

						<div class="entry">
              ${page.content}
            </div>

						<p class="postmetadata">
              <span class="tags">Tags: 
              % for tag in page.tags:
                <a href='${config.siteurl}${tag.url}'>${tag.title | h}</a>&nbsp;
              %endfor
              </span>
            </p>
					</div>

				</div>

		</div>

		</div><!-- .padder -->
	</div><!-- #content -->
  
  <%include file="sidebar.tpl"/> 

<%include file="footer.tpl"/>
