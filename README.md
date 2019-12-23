# Icons Visualizer

A quick and simple UI and API to search and display icons. Can be used in an offline environment thanks to Docker.

![Interface example](./interface.png)

Written in Python (Flask RESTPlus / Swagger) and ReactJS.

## Get started

First, import the icons you want in the `icons/` directory.

:warning: **The names of your files** are very important : the search engine is based on filenames to find keywords as you type the icon you're looking for in the UI searchbar.

You now just have to run :

```do
docker-compose up -d
```

You can access the UI at `localhost:8080`
