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

*tested on OpenSUSE Linux.
**You may need to use "sudo make up" if you havent added your user to the Docker group.
***WARNING: Server is configured to accept connections from all ips and all session ids. This is meant to be run inside a secure network. Running securely on an Internet facing server is possible but requires some small changes including creating a secret key and accepting only signed seesion-ids. A seperate app needs to handle authentication and session-id signing. For help with this you can contact me at joe.mosbacher@gmail.com.
****load balancing is possible by running multiple instances of the server and changing the nginx reverse proxy config file.

## Coming soon to a location near you
 - Support for pulling data from a Database.
 - Api for pulling plots from existing webapps.