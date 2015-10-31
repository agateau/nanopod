#!/usr/bin/env python
# encoding: utf-8

# Python 2/3 compatibility
from __future__ import division, absolute_import, print_function, unicode_literals

import argparse
import os
import sys
import urllib2

import feedparser
import time
import yaml

from slugify import slugify


DEFAULTS = {
    'max_count': 10
}


def load_config(config_file):
    default_cfg = dict(DEFAULTS)
    with open(config_file) as f:
        config = yaml.load(f.read())
        default_cfg.update(config['default'])

    podcasts = []
    for podcast in config['podcasts']:
        cfg = dict(default_cfg)
        cfg.update(podcast)
        podcasts.append(cfg)
    return podcasts


def download(url, final_path, quiet=False):
    final_dir = os.path.dirname(final_path)
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    inf = urllib2.urlopen(url)
    with open(final_path, 'wb') as outf:
        chunk = inf.read()
        if not chunk:
            return
        outf.write(chunk)


def process_podcast_item(item, download_dir, dry_run=False, quiet=False):
    title = item.title

    # Find url
    url = None
    for link in item.links:
        if link.rel == 'enclosure':
            url = link.href
            break
    if not url:
        if not quiet:
            print('No enclosure found in {}'.format(title))
        return

    pub_date_string = time.strftime('%Y-%m-%d', item.published_parsed)
    item_filename = pub_date_string + ' - ' + slugify(title) + '.mp3'

    final_path = os.path.join(download_dir, item_filename)

    if os.path.exists(final_path):
        if not quiet:
            print('Already downloaded {}'.format(item_filename))
        return

    if not quiet:
        print('Downloading {}'.format(item_filename))

    if not dry_run:
        download(url, final_path, quiet=quiet)


def process_podcast(podcast, dry_run=False, quiet=False):
    feed = feedparser.parse(podcast['url'])
    feed_title = feed.feed.title
    download_dir = os.path.join(podcast['download_dir'], slugify(feed_title))
    max_count = podcast['max_count']

    items = sorted(feed.entries, key=lambda x: x.published_parsed, reverse=True)
    for item in items[:max_count]:
        process_podcast_item(item, download_dir, dry_run=dry_run, quiet=quiet)

    filenames = [x for x in os.listdir(download_dir) if x.endswith('.mp3')]
    filenames = sorted(filenames, reverse=True)
    for filename in filenames[max_count:]:
        if not quiet:
            print('Removing {}'.format(filename))
        if not dry_run:
            os.unlink(os.path.join(download_dir, filename))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', dest='config',
        help='Path to config FILE', metavar='FILE')

    parser.add_argument('-n', '--dry-run', action='store_true',
        help='Simulate')

    parser.add_argument('-q', '--quiet', action='store_true',
        help='Be quiet')

    args = parser.parse_args()

    podcasts = load_config(args.config)
    for podcast in podcasts:
        process_podcast(podcast, dry_run=args.dry_run, quiet=args.quiet)

    return 0


if __name__ == '__main__':
    sys.exit(main())
# vi: ts=4 sw=4 et
