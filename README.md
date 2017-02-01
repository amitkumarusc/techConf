# TechConf

[![N|Solid](https://secure.gravatar.com/avatar/7273c58dc017eec83667b50742ff6368?s=80)](https://nodesource.com/products/nsolid)

TechConf is a slack app which helps in finding technical conferences in a region. It also notifies about the upcoming conferences in advance on your slack channel so that you don't miss one.

TechConf is built on python-flask. Mongodb for storing conference details.

TechConf is open source with a [public repository][giturl] on GitHub.

### Installation
1. To install python-flask and other dependencies I would suggest to use `virtualenv`. Install `virtualenv` via `pip`:

    ```sh
    $ pip install virtualenv
    ```
2. Clone the current project 

     ```sh
    $ git clone https://github.com/amitasviper/techConf
    ```
3. Create a virtual environment for a project:

    ```sh
    $ cd techConf
    $ virtualenv venv
    ```
4. To begin using the virtual environment, it needs to be activated:

    ```sh
    $ source venv/bin/activate
    ```
5. To install all required dependencies, execute the following command

     ```sh
    $ pip install -r requirements.txt
    ```
6. To run the application use following command.

    ```sh
    $ python run.py
    ```
7. If you are done working in the virtual environment for the moment, you can deactivate it:

    ```sh
    $ deactivate
    ```

   [giturl]: <https://github.com/amitasviper/techConf>
