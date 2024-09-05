# kubernetes-manifest-clean
Python script that removes all keys:values ​​from a kubernetes manifest so it can be deployed to another cluster.

# Requirements
* Python3
* Library python3 yaml
* Library python3 os
* Library python3 sys

# Arguments
```
arg1: Name of the directory where all the subfolders with the kubernetes manifests to be cleaned are.
arg2: Name of the new folder where the clean kubernetes manifests will be stored. 
```

# Script execution
```python
python3 kubernetes-manifests-clean.py arg1 arg2
```
