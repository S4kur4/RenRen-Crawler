# RenRen-Crawler
**今天人人网被卖了，唉，啥也不说了。**

**那么多照片，丢了太可惜了，不如爬下来吧。**

使用方法如下，`-u`和`-p`指定用户名密码，然后`-a`指定要爬取的相册URL即可：
```bash
crawler.py -u 12345@qq.com -p 123456 -a http://photo.renren.com/photo/123456789/album-123456789/v7
```
依赖：`requests`和`selenium`，自然也是需要[Chromedrive](https://sites.google.com/a/chromium.org/chromedriver/home)的。