# Docker With GitLab Secrets

Example usage:
```bash

# Config will default to ~/.dwgs.conf if not specified
docker-with-gitlab-secrets --dwgs-config /somewhere/dwgs.conf --dwgs-tenant hgi-ci \
    --rm --env-file /higher/precedence -e HIGHEST_PRECEDENCE 123 -it run ubuntu bash
```

Example configuration:
```yml
gitlab:
  url: https://gitlab.example.com
  token: my-token
  tenant: hgi-ci    # Optional default tenant, which will be overriden by if `dwgs-tenant` is specified
```