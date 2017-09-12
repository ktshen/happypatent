from django import template


register=template.Library()

@register.filter(name='get_extension')
def get_extension(filename):
    extension= filename.rsplit(".", 1)[1].lower()
    if extension in ["xltx","rar",'gzip',"odf","wps","tar"]:
        extension="files"
        return extension
    else:
        return extension

@register.filter(name='get_filesize')
def get_filesize(size):
    calc=lambda x,y:round(x/10**y,2)
    if size < 1024:
        return str(calc(size,0)) + " Bytes"
    elif size >= 1024 and size < 1048576:
        return str(calc(size,3)) + " kB"
    else:
        return str(calc(size,6)) + " MB"
