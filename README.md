# Lines of Code counter badge 
![](https://img.shields.io/endpoint?url=https://inobstudios.com/LOCCounterBadge/LOCCounterBadge/responses/shields_v1)
This application aims to allow you to create badges to display on github for lines of code in a repository.
It is a flask web-server that can be set up against github actions, so that when a push happens the lines of code count served will update. This can be output through [shields.io](https://shields.io/endpoint) to show a badge for the response.
<br><br>
Since it is a self-hosted service, it also supports private repositories, and other CI pipelines or badge suppliers can be added relatively easily