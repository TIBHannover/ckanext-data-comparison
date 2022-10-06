# ckanext-data-comparision

The ckan plugin for data (CSV/XLSX) comparing via visualization. 


## Requirements


Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.8 and earlier | not tested    |
| 2.9             | Yes    |



## Installation

To install ckanext-data-comparision:

1. Activate your CKAN virtual environment, for example:

        . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

        git clone https://github.com//ckanext-data-comparision.git
        cd ckanext-data-comparision
        pip install -e .
        pip install -r requirements.txt

3. Add `data_comparision` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Install chartJs (https://www.chartjs.org/) via npm for the plugin.

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

        sudo service supervisor reload
        sudo service nginx reload

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
