# Copyright 2014 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import os

TAG = 'version_4'
HASH = '30A7B04652239BCCFF3CB1FA7CD8AE602791B5F502A96DF39585C13EBC4BB2B64BA1598C0D1F5382028D94E04A5CA02185EA06BF7F4B3520F6DF4CC253F9DD24'

deps = ['sdl2']


def needed(settings):
  return settings.USE_SDL_IMAGE == 2


def get(ports, settings, shared):
  sdl_build = os.path.join(ports.get_build_dir(), 'sdl2')
  assert os.path.exists(sdl_build), 'You must use SDL2 to use SDL2_image'
  ports.fetch_project('sdl2_image', 'https://github.com/tytgatlieven/SDL2_image/archive/' + TAG + '.zip', 'SDL2_image-' + TAG, sha512hash=HASH)

  settings.SDL2_IMAGE_FORMATS.sort()
  formats = '-'.join(settings.SDL2_IMAGE_FORMATS)

  libname = 'libSDL2_image'
  if formats != '':
    libname += '_' + formats
  libname += '.a'

  def create(final):
    src_dir = os.path.join(ports.get_dir(), 'sdl2_image', 'SDL2_image-' + TAG)
    ports.install_headers(src_dir, target='SDL2')
    srcs = '''IMG.c IMG_bmp.c IMG_gif.c IMG_jpg.c IMG_lbm.c IMG_pcx.c IMG_png.c IMG_pnm.c IMG_tga.c
              IMG_tif.c IMG_xcf.c IMG_xpm.c IMG_xv.c IMG_webp.c IMG_ImageIO.m'''.split()
    commands = []
    o_s = []
    defs = []

    for fmt in settings.SDL2_IMAGE_FORMATS:
      defs.append('-DLOAD_' + fmt.upper())

    if 'png' in settings.SDL2_IMAGE_FORMATS:
      defs += ['-s', 'USE_LIBPNG=1']

    if 'jpg' in settings.SDL2_IMAGE_FORMATS:
      defs += ['-s', 'USE_LIBJPEG=1']

    for src in srcs:
      o = os.path.join(ports.get_build_dir(), 'sdl2_image', src + '.o')
      commands.append([shared.EMCC, '-c', os.path.join(src_dir, src),
                       '-O2', '-s', 'USE_SDL=2', '-o', o, '-w'] + defs)
      o_s.append(o)
    shared.safe_ensure_dirs(os.path.dirname(o_s[0]))
    ports.run_commands(commands)
    ports.create_lib(final, o_s)

  return [shared.Cache.get_lib(libname, create, what='port')]


def clear(ports, settings, shared):
  shared.Cache.get_path('libSDL2_image.a')


def process_dependencies(settings):
  settings.USE_SDL = 2
  if 'png' in settings.SDL2_IMAGE_FORMATS:
    deps.append('libpng')
    settings.USE_LIBPNG = 1
  if 'jpg' in settings.SDL2_IMAGE_FORMATS:
    deps.append('libjpeg')
    settings.USE_LIBJPEG = 1


def process_args(ports):
  return []


def show():
  return 'SDL2_image (USE_SDL_IMAGE=2; zlib license)'
