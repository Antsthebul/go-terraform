package main

import (
	"fmt"
	"killer"
	"log"
)

func main() {
	data := "admin"
	api_client, err := killer.NewClient(&data, &data)

	if err != nil {
		log.Println("Trash ", err)
		return
	}
	// p := killer.CreatePerson{
	// 	Name:   "Paco",
	// 	Age:    20,
	// 	Gender: "male",
	// }
	// v, _ := api_client.CreatePerson(p)

	// fmt.Printf("we got: %+v", v)

	api_client.GetPeople()
	res, _ := api_client.GetPerson(2)
	fmt.Printf("Got: %+v", res)
	// c.Auth.Username = "admin"
	// c.Auth.Password = "admin"
	// c.SignIn()

}
