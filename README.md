# ckanext-data-comparision

A CKAN extension for comparing uploaded CSV and XLSX resources and visualizing selected columns.


## Requirements


Compatibility with core CKAN versions:

| CKAN version | Python | Compatible? |
| ------------ | ------ | ----------- |
| 2.10         | 3.8-3.11 | Yes |
| 2.11         | 3.10-3.12 | Yes |

Only resources uploaded to CKAN's local FileStore are supported. Linked remote resources must be uploaded before they can be compared.
The visualization pages load Chart.js 3.9.1 from cdnjs with Subresource Integrity verification.



## Installation

To install ckanext-data-comparision:

1. Activate your CKAN virtual environment, for example:

        . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

        git clone https://github.com/TIBHannover/ckanext-data-comparison.git
        cd ckanext-data-comparison
        pip install -r requirements.txt
        pip install -e .

3. Add `data_comparision` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

        sudo service supervisor reload
        sudo service nginx reload

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
