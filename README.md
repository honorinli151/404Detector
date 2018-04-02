# Description

This tool recognize 404 error according to the html content.
Useful when using Selenium webdriver.
You need to first train the model using the dataset given in ./data

# Auto-sklearn install on Ubuntu

	sudo apt-get install build-essential swig
	curl https://raw.githubusercontent.com/automl/auto-sklearn/master/requirements.txt | xargs -n 1 -L 1 pip install
	pip install auto-sklearn

# Dependencies

    pip install ./wm-dist/*.tar.gz