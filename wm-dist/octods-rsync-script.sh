ssh -t -p 2222 hayj@212.129.44.40 "/usr/bin/yes | pew in 404detector-venv pip uninstall 404detector"
rsync -e 'ssh -p 2222' -avh ../error404detector/* hayj@212.129.44.40:~/wm-dist-tmp/404Detector/error404detector/
