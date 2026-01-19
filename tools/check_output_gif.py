from PIL import Image
import os, sys
p='output.gif'
if not os.path.exists(p):
    print('MISSING')
    sys.exit(2)
im = Image.open(p)
print('format', im.format, 'size_bytes', os.path.getsize(p), 'frames', getattr(im, 'n_frames', 1))
print('info', im.info)
print('transparency_present', 'transparency' in im.info, 'transparency_value', im.info.get('transparency'))
