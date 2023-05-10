IMAGE:=car-valuation-service

build:
	@docker build -t ${IMAGE} .
run:
	@docker run -p 8080:8080 ${IMAGE}