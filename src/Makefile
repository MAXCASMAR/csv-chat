install-lambda:
	pip install awscli
	npm install -g serverless
	aws configure
	serverless plugin install -n serverless-latest-layer-version
	serverless plugin install -n serverless-python-requirements
	serverless plugin install -n serverless-prune-plugin

deploy-lambda:
	sls deploy