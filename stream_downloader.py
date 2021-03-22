from os import sep
import logging
import argparse

import livestream_saver.download
import livestream_saver.merge
from livestream_saver.util import get_cookie

logger = logging.getLogger("livestream_saver")
logger.setLevel(logging.DEBUG)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='Youtube URL to download.')
    parser.add_argument('-c', '--cookie', action='store',
        default="./cookie.txt", type=str,
        help='Path to cookie file.')
    parser.add_argument('-q', '--max_video_quality', action='store',
        default=None, type=int,
        help='Use best available video resolution up to this height in pixels.')
    parser.add_argument('-o', '--output_dir', action='store',
        default="./", type=str,
        help='Output directory where to write downloaded chunks.')
    parser.add_argument('-d', '--delete_source', action='store',
        default=False, type=bool,
        help='Delete source files once final merge has been done.')
    levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    parser.add_argument('--log', action='store', default="INFO", choices=levels,
        help='Log level. [DEBUG, INFO, WARNING, ERROR, CRITICAL]')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    # FIXME Not a very useful logger, might delete later.
    logfile = logging.FileHandler(\
        filename=args.output_dir + sep + "downloader.log", delay=True)
    logfile.setLevel(logging.DEBUG)
    formatter = logging.Formatter(\
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    logfile.setFormatter(formatter)
    logger.addHandler(logfile)

    conhandler = logging.StreamHandler()
    conhandler.setLevel(log_level)
    conhandler.setFormatter(formatter)
    logger.addHandler(conhandler)

    cookie = get_cookie(args.cookie) if args.cookie else {}

    dl = livestream_saver.download.YoutubeLiveStream(
        url=args.url,\
        output_dir=args.output_dir,\
        max_video_quality=args.max_video_quality,\
        cookie=cookie,
        log_level=args.log
    )
    dl.download()

    # TODO make sure number of segment match the last numbered segment
    # Merge segments into one file
    if dl.done:
        merge(info=dl.video_info, data_dir=dl.output_dir, delete_source=args.delete_source)