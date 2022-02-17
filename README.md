# Lines of Code counter badge 
![](https://img.shields.io/endpoint?url=https://inobstudios.com/LOCCounterBadge/LOCCounterBadge/responses/shields_v1) <br>
This application aims to allow you to create badges to display on github for lines of code in a repository.
It is a flask web-server that can be set up against github webhooks, so that when a push event happens the lines of code count served will update. This can be output through [shields.io](https://shields.io/endpoint) to show a badge for the response.
<br><br>
Since it is a self-hosted service, it also supports private repositories, and other CI pipelines or badge suppliers can be added relatively easily
## Installation
You will need the following packages
*   `sudo apt install cloc git`
*   `pip3 install flask pybadges gunicorn`
    * (Unfortunately Flask 2.0x has conflicting dependencies with pybadges 2.2.1, therefore pip won't allow install though a `requirements.txt`.
      I have not noticed any problems)
## Usage
1. Make `conf.d/config.cfg` out of `conf.d/config.cfg.template`
    * Setup your repositories
2. Test that the server works `./LOCCounterBadge.py`
    * On startup it should clone the repositories, and shutdown if any errors happen
3. Create webhooks for your repositories, making sure that the `secret` in the config matches the webhook
    * Every time a push event is registered for the `branch` given in the config, the LoC will be updated
    * The endpoint for the webhook is `/<repository>/actions/github`
    * The endpoint for a shields response is `/<repository>/responses/shields_v1` which can be wrapped according to [shields.io - custom endpoint](https://shields.io/endpoint)

Please take note that shields.io requires https, so I would recommend running the application through reverse proxy. In apache this can be achieved through this
```
    ProxyPass /LOCCounterBadge/ http://127.0.0.1:20300/
    ProxyPassReverse /LOCCounterBadge/ http://127.0.0.1:20300/
```
in my case giving me the endpoint used for this repository as
```
https://inobstudios.com/LOCCounterBadge/LOCCounterBadge/responses/shields_v1
```