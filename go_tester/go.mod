module killer/test

go 1.22.2

replace killer => ../go_sdk

require killer v0.0.0-00010101000000-000000000000

require (
	github.com/go-resty/resty/v2 v2.12.0 // indirect
	golang.org/x/net v0.23.0 // indirect
)
