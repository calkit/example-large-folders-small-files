# Large folders of small files example

This example project shows how to handle tracking large folder of small files
in DVC, either as pipeline outputs or raw version-controlled inputs.

The `input` folder is a large dataset consisting of many small files.
It was added to the project with:

```sh
calkit add input
```

Calkit automatically determined the `--to` option should be `dvc-zip`,
since it is a large folder with many small files in it.

The pipeline in `calkit.yaml` also creates an output folder `results`,
which is large in total size but consists of many small files.
That output therefore uses the `dvc-zip` storage type to remain efficient.
The only tradeoff is that the folder is then tracked as one unit, so
if only one file within changes, the entire thing needs to be synced
with the DVC remote.
