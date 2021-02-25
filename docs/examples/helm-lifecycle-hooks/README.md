# Bitops Operations Repo

Welcome to Bitops! This serves as a starting point for deploying your application to the cloud.

This repo can be run as is with
```
docker run \
-e ENVIRONMENT="test" \
-e PROVIDERS="none" \
-v $(pwd):/opt/bitops_deployment \
bitovi/bitops:latest
```

For more information, check out official bitops docs https://bitovi.github.io/bitops/
