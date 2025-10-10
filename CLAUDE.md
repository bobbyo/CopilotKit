## Testing
### Python sdk testing

```
cd sdk-python/
poetry install
poetry run pytest -v
```


### e2e for coagent-starter with thread management

#### Launch a copy of the services the e2e test will need to test
The e2e tests require first launching the target service, with env variables that set ports, api keys, etc.
Copy a reference example file and adjust ports to some that are unused.
E.g. 
 - realpath examples/coagents-starter/.env  # if already filled in with passwords
 - realpath examples/coagents-starter/env.examples

```bash
cat ./examples/e2e/app-configs.json
echo "The ports above need to be consistent with the env file we edit below for the coresponding app we will test"

ENV_FILE=`realpath examples/coagents-starter/.env.test`
cp -vi examples/coagents-starter/env.examples "$ENV_FILE"
nano "$ENV_FILE"

###### Use the custom script that lanuches the example with linking to the local codebase and runs all services:

echo "Launching services before testing examples/coagents-starter"
export ENV_FILE && \
set -a && \
echo "ENV_FILE=${ENV_FILE}" && \
source ${ENV_FILE} && \
set +a && \
pushd ./CopilotKit && \
pnpm i && \
./scripts/develop/example.sh coagents-starter
```

Then, after those services run and no errors are observed in launching them, follow the instructions to run e2e tests on those services in examples/e2e/README.md. 
The e2e tests will fail if the services are not pre-launched as described above. Common failure modes are ports already in use, failing to export env vars so the services can see thenm, or trying a different way to launch the services so that the local copy of CopilotKit/ and sdk-python code are not used. 

