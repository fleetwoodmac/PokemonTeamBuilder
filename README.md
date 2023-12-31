<h1 align="center">PokemonTeamBuilder</h1>
<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
  <a href="https://opensource.org/license/mit/" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>

> A hacked-together, barebones, locally-(or web)-hosted Pokemon Team Builder app. Mostly pure Python using Streamlit and PyZMQ.

### 🏠 [Homepage](https://github.com/fleetwoodmac/PokemonTeamBuilder)

## Table of contents
- [Feature List](https://github.com/fleetwoodmac/PokemonTeamBuilder#feature-list)
- [Software/Resources Used](https://github.com/fleetwoodmac/PokemonTeamBuilder#softwareresources-used)
- [Images](https://github.com/fleetwoodmac/PokemonTeamBuilder#images)
- [Preparation/Build Guide](https://github.com/fleetwoodmac/PokemonTeamBuilder#preparation-build-guide)
    - [Using Docker (easiest to run)](https://github.com/fleetwoodmac/PokemonTeamBuilder#using-docker-easiest-to-run)
    - [Using Python (bit more work)](https://github.com/fleetwoodmac/PokemonTeamBuilder#using-python-bit-more-work)
- [Usage](https://github.com/fleetwoodmac/PokemonTeamBuilder#usage)
    - [Using Docker](https://github.com/fleetwoodmac/PokemonTeamBuilder#using-docker)
    - [Using Python](https://github.com/fleetwoodmac/PokemonTeamBuilder#using-python)
- [Remove/Delete Program](https://github.com/fleetwoodmac/PokemonTeamBuilder#removedelete-program)
    - [Using Docker](https://github.com/fleetwoodmac/PokemonTeamBuilder#using-docker-1)
    - [Using Python](https://github.com/fleetwoodmac/PokemonTeamBuilder#using-python-1)
- [Notes](https://github.com/fleetwoodmac/PokemonTeamBuilder#notes)
- [Author](https://github.com/fleetwoodmac/PokemonTeamBuilder#author)
- [Contributing](https://github.com/fleetwoodmac/PokemonTeamBuilder#-contributing)
- [Show your Support](https://github.com/fleetwoodmac/PokemonTeamBuilder#show-your-support)
- [Acknowledgements](https://github.com/fleetwoodmac/PokemonTeamBuilder#acknowledgements)
- [License](https://github.com/fleetwoodmac/PokemonTeamBuilder#-license)

## Feature List
---
- Functional
  - Choose Pokemon
      - Get game desc
      - Get type
      - Get sprite
  - Choose Moves
      - get move desc
      - get power/acc
      - get type
  - Choose Held item
      - get sprite
      - get item desc
  - Get Smogon Dex Analysis Link
- User
    - tabbed or single page view

## Software/Resources Used
---
- Python 3.10
- [Streamlit](https://streamlit.io/)
- [PyZMQ](https://zeromq.org/languages/python/)
- [Docker](https://www.docker.com/)
- [PokeAPI](https://pokeapi.co/)

## Images
---
### Single Page View
<p align='center'>
  <img src=https://github.com/fleetwoodmac/PokemonTeamBuilder/assets/69140036/6977e517-7d88-4b55-8b80-ea6c1b2c1b49>
</p>

### Example Teamslot
<p align='center'>
  <img src=https://github.com/fleetwoodmac/PokemonTeamBuilder/assets/69140036/9f629b27-c88d-46ec-b0b7-fa6819f8d3af>
</p>

  
## Preparation (Build) Guide
---
### Using Docker (easiest to run) 
1. Install [Docker Desktop](https://www.docker.com/get-started/)
2. (optional) Install [Git](https://github.com/git-guides/install-git)
3. Clone this repo to a directory of your choice using the following command:
```sh
git clone https://github.com/fleetwoodmac/PokemonTeamBuilder.git
```
or by downloading repo as zip file and unzipping to desired to location 
<p align='center'>
  <img src=https://github.com/fleetwoodmac/PokemonTeamBuilder/assets/69140036/a7990b92-6831-469f-bbca-e9bb092b5e58 width='500'>
</p>
4. Make sure Docker Desktop is running and that you have space free before proceeding.<br \>
5.  In the root directory of the program, build using the following command:

```sh
docker build -t namehere .
```

where ```namehere``` is whatever you want the docker image to be called. For example, this guide will use ```pokemonteambuilder```. *Keep the* ```.``` *in the command*. 

6. Terminal/CMD should give a success message
<p align='center'>
  <img src=https://github.com/fleetwoodmac/PokemonTeamBuilder/assets/69140036/6b4aab95-a47d-427b-a8af-04a7b00d7542 width='500'>
</p>
Verify that the image built properly using command

```sh
docker images
```

<p align='center'>
  <img src=https://github.com/fleetwoodmac/PokemonTeamBuilder/assets/69140036/51473414-8646-4e08-8510-48b8a5cb7a82 width='300'>
</p>

### Using Python (bit more work)

To be updated

## Usage
---
### Using Docker 
1. **This is if you built the docker image.**
2. Run the following command
```sh
docker run -p 8501:8501 namehere
```
where ```namehere``` is the image name you used in step 5 of the docker build guide. You should see something like:

<p align='center'>
  <img src=https://github.com/fleetwoodmac/PokemonTeamBuilder/assets/69140036/498f0dae-43b2-4110-b0dd-683277eb4913 width='500'>
</p>

3. Copy the URL (by default, this is http://0.0.0.0:8501). paste it into a browser, and you should see the webapp come up!
<br>

<br>
4. You can verify the docker container is running using

```sh
docker container ls
```
<p align='center'>
  <img src=https://github.com/fleetwoodmac/PokemonTeamBuilder/assets/69140036/78b4e31f-8803-47a0-bb95-4df777188823>
</p>

 5. Stop the container using the command

```sh
docker stop containername
```

where ```containername``` is the text from step 4 under NAMES. In the image above, it happened to be ```peaceful_leavitt```. You can also open Docker Desktop, go to the Containers tab, and stop the container there. 

### Using Python
To be updated

## Remove/Delete program
---
### Using Docker 
1. The easiest way to do this is using Docker Desktop. 
2. Open Docker Desktop. Make sure any containers running this program are stopped.
3. In the Containers tab,  check the box for the container that has this program in it, and hit Delete.
4. In the Images tab, check the box for the image containing this program, and hit Delete.
5. Delete the directory you cloned/files you directly downloaded in the Install guide.

### Using Python 
To be updated

## Notes
---
- **While I do not collect any sort of information, Streamlit collects usage telemetry by default. This is not disabled by default.**
   - If you want to disable this, see Streamlit's documentation on the subject [here](https://docs.streamlit.io/library/advanced-features/configuration#telemetry).

 - Changing the port or address the app runs on
     - You can change the port as well as the host URL you want to app to run on in the Dockerfile **before you build the image**. Also make sure to change the ```EXPOSE``` line in the Dockerfile if you change the default port.
  
 - Deploying as a web-hosted/public instance
   - I can do a more thorough write-up of how to deploy this as a public instance if there is interest but the general steps are:
     - Make a docker hub account and create a public repository. Name it whatever you want (ex: ```pokemonteambuilder-demo```). it should display a push command like ```docker push yourdockername/yourreponame```
     - Build a docker image locally following the steps in the build guide. Make sure that your image name matches your repo name, i.e for the image name/tag use ```yourdockerusername/yourimagename``` (or ```yourdockerusername/yourimagename:version``` where version is something like ```latest``` if you are actively tracking version history).
     - if you are compiling on an arm based machine like an M1 Mac, make sure you build an x86 version of the image (see Jaimyn Mayer's guide linked below).
     - push to docker hub using the docker push command you got earlier
     - sign up for the free tier of a hosting service like oracle cloud, google cloud run, etc.
     - I used google cloud run, so for that, once you are logged in, create a new project and name it whatever, then go to Google Cloud Run, hit create new service
     - for the container URL just put in your docker hub repo name, i.e ```yourdockerusername/yourreponame```. It should automatically pull the docker image from there (again, important that it is a public repo)
     - change the container port to 8501 (or whatever you changed it to in the dockerfile)
     - create the service, and it should eventually give you a URL. Go to that URL and you should have a public instance running.

- Note on debugging seg faults and pyarrow
  - one of Streamlit's dependencies is pyarrow, and as of the time of this readme being updated, pyarrow has been quite finicky. If you are getting segfaults or weird errors running Streamlit, it may be due to pyarrow. As of this update to the readme, the current version of pyarrow is 14.0.0. After installing streamlit, manually overwriting pyarrow with an older version (12.0.1 for example) made the app run perfectly after experiencing some seg faults while running the ```streamlit run``` command. 


## Author
---
👤 **fleetwoodmac**

* Website: https://github.com/fleetwoodmac/
* Github: [@fleetwoodmac](https://github.com/fleetwoodmac)

## 🤝 Contributing
---
Contributions, issues and feature requests are welcome! Please also feel free to fork and start developing on it more on your own!<br />Feel free to check [issues page](https://github.com/fleetwoodmac/PokemonTeamBuilder/issues). 

## Show your support
---
As mentioned, please feel free to fork this and start developing it more if you want--it's pretty barebones and sorta buggy in its current state. Give it a ⭐️ if you thought it was cool!

## Acknowledgements
---
- Streamlit's [documentation](https://docs.streamlit.io/)
- PokeAPI's [documentation](https://pokeapi.co/docs/v2)
- ZeroMQ's [documentation](https://zeromq.org/languages/python/)
- Image and misc. resources
    - Kelsey Oshiro's [Team Builder project](https://github.com/kelseymosh/pokemon-team-builder) for type images. Their [Github](https://github.com/kelseymosh).
    - Bulbapedia for Pokedex image [here](https://archives.bulbagarden.net/media/upload/3/37/RG_Pokédex.png), and move data when not available on PokeAPI.
    - [Smogon Strategy Pokedex](https://www.smogon.com/dex/) for competitive analysis 
- Docker resources
    - Isha Terdal's [streamlit app deployment guide](https://medium.com/@ishaterdal/deploying-a-streamlit-app-with-docker-db40a8dec84f). Their [Github](https://github.com/ishaterdal).
    - Streamlit's [Docker guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)
    - Jaimyn Mayer's [guide](https://blog.jaimyn.dev/how-to-build-multi-architecture-docker-images-on-an-m1-mac/) on how to build x86 and arm64 on M1 Macs. Their [Github](https://github.com/jabelone)
    - FayZ676's [guide](https://medium.com/@faizififita1/how-to-deploy-your-streamlit-web-app-to-google-cloud-run-ba776487c5fe) on deploying Streamlit docker images to Google Cloude Run.
- Carlos D Serrano's Streamlit [repeatable items guide](https://medium.com/streamlit/creating-repeatable-items-in-streamlit-cb8b6264e1e6). Their [Github](https://github.com/sqlinsights) (I think?).
- kefranagb's [readme-md-generator](https://github.com/kefranabg/readme-md-generator)

## 📝 License
---
Copyright © 2023 [fleetwoodmac](https://github.com/fleetwoodmac).<br />
This project is [MIT](https://opensource.org/license/mit/) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
