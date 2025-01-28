Developer Environment Setup

Install pyenv https://github.com/pyenv/pyenv

e.g. on a mac

```
brew update
brew install pyenv
```

Configure pyenv for your choice of terminal 

e.g. for ksh
```
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
  echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
  echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc
```


Use pyenv to download 3.12 version of Python.
```
pyenv install 3.12
``` 

Set this version of Python to be used:
```
pyenv local 3.12
```

Check that it's set
```
python --version
```
should output something like:
```
julianleonard@Julians-Laptop case-study % python --version
Python 3.12.8
```

Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate
```

To use CDK you will need to install Node.  I recommend using `nvm` (https://github.com/nvm-sh/nvm) to install and manage your node version (similar to `pyenv` above).  For this case study I am using node `v.22.11.0`.


Also, this readme assumes you have an AWS account and the `aws cli` installed already: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html


* Install the CDK:

```
npm install -g aws-cdk
```
Check the version that is installed:
```
(myenv) julianleonard@Julians-Laptop case-study % cdk version
2.177.0 (build b396961)
```

I used VS Code so I installed the AWS Toolkit which has support for CDK.


```
pip install -r requirements.txt
```

If you working in an AWS environment which has not been bootstrapped for CDK, you'll need to run this command: `cdk bootstrap aws://<aws-account-id>/<region>` e.g.
```
cdk bootstrap aws://1234567890/eu-central-1
```

Install django framework
```
python -m pip install Django
```

```
django-admin startproject mysite
```

Start apache serverapachectl
```
sudo apachectl start
```

Follow the steps here: https://aws.amazon.com/getting-started/hands-on/build-react-app-amplify-graphql/module-one/



Create skeleton react app
```
npm create vite@latest notesapp -- --template react
```

Scaffolding project in /Users/julianleonard/repos/case-study/frontend/notesapp...

Done. Now run:

  cd notesapp
  npm install
  npm run dev

Install amplify libraries
```
npm create amplify@latest -y
```

WSGIScriptAlias / /Users/julianleonard/repos/case-study/backend/mysite/mysite/wsgi.py
WSGIPythonHome /Users/julianleonard/repos/case-study/backend/venv
WSGIPythonPath /Users/julianleonard/repos/case-study/backend/mysite

<Directory /Users/julianleonard/repos/case-study/backend/mysite/mysite>
<Files wsgi.py>
Require all granted
</Files>
</Directory>