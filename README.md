### References
- [treasure-data/digdag](https://github.com/treasure-data/digdag) 
- [docs.digdag.io](https://docs.digdag.io/)
- [EMBULK PLUGINS BY CATEGORY](https://plugins.embulk.org/)

### Usage
- build Docker image
```
docker bulid -t digdag-ecs .
```
- turn up digdag and embulk
```
docker-compose up
```
digdag UI is accessible on the  http://x.x.x.x:5000

- close digdag
  - exit from digdag with the ctrl-c or ctrl-z
  - shut down the containers running in background
```
docker-compose down -v
```

