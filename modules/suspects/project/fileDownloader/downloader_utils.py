
'''Info Header Start
Name : downloader_utils
Author : Wieland@AMB-ZEPH15
Saveorigin : WebUtils.toe
Saveversion : 2022.32660
Info Header End'''
def convert_size(size_bytes):
   
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def convert_time( seconds ):
    rest_seconds = math.floor(seconds % 60)
    minutes = math.floor( seconds / 60 )
    rest_minutes = math.floor(minutes % 60)
    hours = math.floor(minutes / 60)
    return f"{hours:02}:{rest_minutes:02}:{rest_seconds:02}"