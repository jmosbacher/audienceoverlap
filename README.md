# Audience overlapper
A simple little SPA to visualize audience overlap.
## Spin up a single server instance with Docker
 - git clone this repo.
 - Make sure you have Docker and docker-compose installed.
 - create a folder called "credentials" under the app/audienceoverlap folder.
 - copy your google.json credentials file into the credentials folder.
 - open a terminal in the repo root directory and run "make up" **.
 - go to `your-ip`:5006/ in your browser from anywhere in the network. If you are on the same computer running the server you can also use localhost:5006
 - shut down and clean up image by running "make down"
 - Report all the bugs you find.
* tested on OpenSUSE Linux.
** You may need to use "sudo make up" if you havent added your user to the Docker group.

## Coming soon to a location near you
 - Support for pulling data from a Database.
 - Api for pulling plots from existing webapps.