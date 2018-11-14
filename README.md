# RenRen-Crawler
**今天，人人网被卖了，啥也不说了。**

**那么多照片，丢了太可惜了，不如爬下来吧。**

参数说明如下，使用`-u`和`-p`指定用户名密码，然后`-a`指定相册URL即可：
```python
usage: crawler.py [-h] [-u USERNAME] [-p PASSWORD] [-a ALBUM_URL]

Example: crawler.py -u 12345@qq.com -p 123456 -a \
http://photo.renren.com/photo/123456789/album-123456789/v7

Options:
  -h, --help            Show Help Message And Exit
  -u USERNAME, --username USERNAME
                        Specify RenRen Username
  -p PASSWORD, --password PASSWORD
                        Specify Corresponding Password
  -a ALBUM_URL, --album ALBUM_URL
                        Specify Album URL Of Yours Or Your Friends
```