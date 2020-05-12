.PHONY: data

data/glove.6B.50d.txt:
	aws s3 cp s3://advancedpythonproject/glove.6B.50d.txt data/ --request-payer=requester