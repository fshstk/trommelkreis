# Digitaler Trommelkreis Website

This is the repository for [trommelkreis.club](https://trommelkreis.club), a website for a biweekly
music production workshop based on Django.

While you are welcome to deploy your own version, or fork the project and play around with it, its
main purpose is to power the original [trommelkreis.club](https://trommelkreis.club) site, so don't
expect anything in the way of documentation.

## Features

Every occurence of the workshop represents a *session*. Every session has an associated *challenge*,
where users must create and submit a musical track within a certain time frame. When uploads are
open, users may upload their track in MP3 format to the public archive. A single *challenge* may be
connected to any number of *sessions*.

ID3 metadata is automatically parsed by the upload script and written to the database. If the user
enters a custom artist name during upload, the ID3 data is overwritten by the user input.

The Django admin interface makes it easy to add *sessions*/*challenges*, as well as manage uploaded
files.

A basic API for the archive exists, and a [Discord bot](https://github.com/fshstk/trommelbot) has
been developed for group listening sessions after each workshop is concluded.

## Deployment

You should be able to deploy this app in three easy steps:

1. `docker build . -t trommelkreis`;
2. `docker run -p 8000:8000 trommelkreis`;
3. [http://localhost:8000](http://localhost:8000).

## Environment

You must make sure the following env variables are set in your app dashboard.

### App

- `DEBUG` (1 or 0)
- `SECRET_KEY` (unique app key required by Django)

### Media

- `MEDIA_PASSWORD` (secret URL suffix for viewing copyright-protected sessions)
- `PREVIEW_PASSWORD` (secret URL suffix for viewing unpublished sessions)

### Storage

- `DATABASE_URL`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_S3_ENDPOINT_URL`
- `AWS_STORAGE_BUCKET_NAME`

## License

All code is licensed under GPLv3.
