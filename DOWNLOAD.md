Dataset **CLVOS23** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](/supervisely-supervisely-assets-public/teams_storage/H/j/nZ/qPEhOC9xpy0kPCnXn2aXX5lyQu0FjKOh9XoKntfU9Pb7JDJOh04InSODMkKpqPCxF2Z1il9ItSqiRHk8rWYrOOq9bf22CHTG3FMIYSFfVS8hNANiYXd8MAOh6lxL.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='CLVOS23', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/amir4d/clvos23/download?datasetVersionNumber=1).