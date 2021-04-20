# AllegroTask3

## Installation

Code was tested on python 3.6.9 64-bit

This code requires library PyGitHub to run https://github.com/PyGithub/PyGithub

`
pip install PyGithub
`

## How to use
To run, use :
`
python server.py 
`
or
`
python server.py [<port>]
`
(default port is 8420)

### Example usage for user "Allegro" :

http://localhost:8420/repos/Allegro
For list of repositories and theirs star count.

http://localhost:8420/stars/Allegro
For sum of stars over all repositories by given user.

-------
I don't think this project needs much extensions as all this data can be already pulled from public REST APIs of GitHub. 