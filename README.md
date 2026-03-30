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
The input folder was then automatically ignored by Git,
`calkit compress input -o .calkit/dvc/zip/input.zip` was run on it,
and the information was added to `.calkit/dvc/path-ops.yaml`.

When the Calkit pipeline is compiled to DVC, any path ops stages are added
automatically.
That is, we get a stage like:

```yaml
"calkit.dvc.unzip(input)":
  cmd: calkit uncompress .calkit/dvc/zip/input.zip -o input
  deps:
    - .calkit/dvc/zip/input.zip
  outs:
    - input:
        cache: false
        persist: false
```

## UX

We need to make sure unzips run on any pull and zips run on any adds?

This should be transparent to the user. The unzipped folders should not need
to be thought about.

When should zips happen?

- When a folder is added to the repo (`calkit add my-large-folder-small-files`)
- When a pipeline stage runs that has a `dvc-zip` output

When should unpacks happen?

- When a project is cloned
- When the pipeline is run, and the unzipped folder has been modified
- When a packed folder is updated by a pull
- When we check out a different branch (this should do a dvc pull anyway)

## Alternate approach

If we don't want to add "hidden" DVC stages,
Calkit could manage the zip/unzip on its own, but when?
It could happen when the pipeline is run and on pull/push.

We could also possibly do this as part of the `ck` remote type, but
that would then make this feature not available to regular DVC remote users.
