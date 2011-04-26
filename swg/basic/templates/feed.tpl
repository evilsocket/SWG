<?xml version="1.0" encoding="UTF-8"?> 
<rss version="2.0"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:atom="http://www.w3.org/2005/Atom"
	xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
	xmlns:slash="http://purl.org/rss/1.0/modules/slash/"
	> 
 
<channel> 
	<title>${config.sitename}</title> 
	<atom:link href="${config.siteurl}/feed.xml" rel="self" type="application/rss+xml" /> 
	<link>${config.siteurl}</link> 
	<description>If you can&#039;t understand it, it doesn&#039;t mean it&#039;s wrong ...</description> 
	<lastBuildDate>${config.now.strftime("%a, %d %b %Y %H:%M:%S GMT")}</lastBuildDate> 
	<language>it</language> 
	<sy:updatePeriod>hourly</sy:updatePeriod> 
	<sy:updateFrequency>1</sy:updateFrequency> 

  %for page in pages[0:25]:
  <item> 
    <title>${page.title | h}</title>
	  <description><![CDATA[${page.abstract}]]></description> 
	  <link>${config.siteurl}${page.url}</link> 
    <pubDate>${page.datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")}</pubDate> 
    <dc:creator>${page.author.username | h}</dc:creator> 
    <guid isPermaLink="true">${config.siteurl}${page.url}</guid> 
    %for category in page.categories:    
      <category><![CDATA[${category.title}]]></category>
    %endfor
  </item> 
  %endfor

</channel> 
</rss> 
