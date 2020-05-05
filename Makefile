.PHONY: data



data/glove.6B.100d.txt:
	aws s3 cp s3://object/advancedpythonproject/glove.6B.100d.txt data/ --request-payer=requester

data/glove.6B.200d.txt:
	aws s3 cp s3://object/advancedpythonproject/glove.6B.200d.txt data/ --request-payer=requester

data/glove.6B.300d.txt:
	aws s3 cp s3://object/advancedpythonproject/glove.6B.300d.txt data/ --request-payer=requester


data/glove.6B.400d.txt:
	aws s3 cp s3://object/advancedpythonproject/glove.6B.400d.txt data/ --request-payer=requester