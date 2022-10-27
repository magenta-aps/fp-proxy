# `fp_proxy`

## What is this?

A system called
[Publication](https://www.firstagenda.com/loesninger/firstagenda-publication),
made by [FirstAgenda](https://www.firstagenda.com/), is widely used by the
Danish public sector to publish notes and minutes from official meetings.

Unfortunately, Publication is built from the ground up to use JavaScript. If
you want to automatically traverse the documents published by your organisation
to look for information that hasn't been redacted correctly, for example, you
can't use a normal web crawler -- the files returned by the server are blank
templates, filled out in a browser with the results of an API call.

That's where `fp_proxy` comes in. It makes the same API calls as the JavaScript
web app, but it renders the results of those calls on the server and returns
them as a normal series of linked web pages, making it crawler-friendly.

## How do I set this up?

`fp_proxy` is designed to be used as a Docker image, so its configuration is
driven by a few simple environment variables:

| Variable | Meaning |
| -------- | ------- |
| `FPP_SERVER_URL` | The root URL of the FirstAgenda Publication instance that should be scanned |

Define those in your deployment environment (or, if you just want to try it out
locally, in `docker-compose.yml`) before starting the system up.

## How do I try this out?

`fp_proxy` is actually a very simple Flask app, behind the scenes, so you have
a few options:

* start it up as a Docker image using the provided `docker-compose.yml` file:
  run `docker-compose up`, then visit http://localhost:8019/

* run the Flask development web server in any other Python environment: run
  `python -m flask --app src/fp_proxy.py run`, then visit
  http://localhost:5000/

(Try not to be too impolite, though -- in particular, don't crawl a FirstAgenda
Publication instance without talking to its operator first.)

## Who's behind this?

`fp_proxy` is brought to you by [Magenta ApS](https://www.magenta.dk/), the
largest pure-play open source developer in Scandinavia. We have offices in
Copenhagen, Aarhus, and Nuuk, and we have customers -- colossal, tiny, and
everything in between -- from the public and private sector across all of
Denmark and Greenland.

Since we started in 1999, we've released all of our products under open source
and free software licences, and it'll stay that way! You deserve to know what
the programs you depend on are doing, and to be able to change them if you want
them to do something else.

`fp_proxy` has been developed for use alongside
[OS2datascanner](https://os2datascanner.magenta.dk/), the advanced GDPR
compliance and data scanning tool we maintain and develop for the
[OS2 consortium](https://os2.eu/).

If you'd like to talk to us about any of our products, our plans for them, or
even about financing the development of a feature you need, you can always get
in touch with us at info@magenta.dk.

----

`fp_proxy` is copyright © Magenta ApS 2022, and its use is subject to the terms
of the Mozilla Public License, v. 2.0. See the `LICENSE` file for more details.
