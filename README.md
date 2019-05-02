# Audience overlapper
A simple little SPA to visualize audience overlap.
## Spin up a single server instance with Docker-machine
 - git clone this repo.
 - Make sure you have your docker-machine environment setup Docker, docker-compose installed.
 - If you want to pull data from google sheets, create a folder called "credentials" under the bokeh_app/audienceoverlap folder and copy your google.json credentials file into it.
 - run `bash deploy.sh "machine_name"` to deploy to an existing docker machine.
 - Report all the bugs you find.

*tested on OpenSUSE Linux and aws docker instance.  
**You may need to use "sudo" if you havent added your user to the Docker group.  
***WARNING: Server is configured to accept http connections, meaning you will need to setup https termination with a proxy such as nginx for https support. It is also possible to configure the existing server for https. For help with this you can contact me at joe.mosbacher@gmail.com.   
****load balancing is possible by running multiple instances of the server and changing the nginx reverse proxy config file.   

## Coming soon to a location near you
 - Support for pulling data from a Database.
 - Api for pulling plots from existing webapps.