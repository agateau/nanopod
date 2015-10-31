# Nanopod

A minimalist command-line podcast downloader, designed to be run from a crontab.

## Requirements

- Python 2
- Modules listed in requirements.txt

## Usage

Install Nanopod requirements:

    pip install -r requirements.txt

Install Nanopod:

    ./setup.py install

Create a nanopod.yaml file (or any other name actually), wherever works best
for you, with content like this:

    default:
        # Where to save podcasts
        download_dir: /home/media/podcasts

        # How many podcasts to keep
        max_count: 5
    podcasts:
        - url: http://feeds.gitminutes.com/gitminutes-podcast
        - url: http://cdn2-europe1.new2.ladmedia.fr/var/exports/podcasts/sound/revue-de-presque.xml

Let Nanopod download them:

    nanopod -c /path/to/nanopod.yaml

It will create in `/home/media/podcasts` one directory per podcast, and in this
directory, one file per podcast, named using the following format:
`<year>-<month>-<day> - <slugified-version-of-title>.mp3`.

If there are more than `max_count` mp3 files in the podcast dir, the oldest one
will be removed.

## Motivation

I was looking for a podcast download tool with the following features:
- Crontab friendly: run from the command-line, without needing a particular
  user
- Capable of handling the "La revue de presque de Nicolas Canteloup" podcast,
  which has the particularity of having all its episodes named "podcast.mp3"
  (hence the renaming feature)
- Would run on the Debian Wheezy of my home server

I tried quite a few tools, could not find one which satisfied my needs, so ended
up writing Nanopod in an evening.

## License

BSD
