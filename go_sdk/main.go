package killer

import (
	"encoding/json"
	"fmt"
	"log"
	"strconv"

	"github.com/go-resty/resty/v2"
)

type Person struct {
	ID     int    `json:"id"`
	Name   string `json:"name"`
	Age    int    `json:"age"`
	Gender string `json:"gender"`
}

type CreatePerson struct {
	Name   string `json:"name"`
	Age    int    `json:"age"`
	Gender string `json:"gender"`
}

type People struct {
	People []Person `json:"people"`
}

type Client struct {
	Token      string
	HTTPClient *resty.Client
	Auth       AuthStruct
}

type AuthStruct struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type AuthResponse struct {
	Username string `json:"username"`
	Token    string `json:"token"`
}

func NewClient(username, password *string) (*Client, error) {
	c := Client{
		HTTPClient: resty.New(),
	}
	c.Auth = AuthStruct{Username: *username, Password: *password}

	ar, err := c.SignIn()

	if err != nil {
		return nil, err
	}

	c.Token = ar.Token
	return &c, nil
}

func (c *Client) SignIn() (*AuthResponse, error) {

	// rb, err := json.Marshal(c.Auth)
	// if err != nil {
	// 	return nil, err
	// }

	resp, err := c.HTTPClient.R().
		SetBody(c.Auth).
		Post("http://localhost:8000/signin")

	if err != nil {
		log.Println("bad ", err)
		return nil, err
	}

	if resp.StatusCode() != 200 {
		return nil, fmt.Errorf("you suck thje most %s", resp.Body())
	}
	var ar AuthResponse
	json.Unmarshal(resp.Body(), &ar)
	return &ar, nil

}

func (c *Client) GetPeople() (People, error) {
	var people People

	resp, err := c.HTTPClient.R().
		EnableTrace().
		Get("http://localhost:8000/")

	err = json.Unmarshal(resp.Body(), &people)
	return people, err
}

func (c *Client) GetPerson(id int) (Person, error) {
	var person Person

	resp, _ := c.HTTPClient.R().
		EnableTrace().
		Get(fmt.Sprintf("http://localhost:8000/%s", strconv.Itoa(id)))

	err := json.Unmarshal(resp.Body(), &person)
	return person, err
}

func (c *Client) CreatePerson(cp CreatePerson) (Person, error) {

	personMap := map[string]interface{}{
		"name":   cp.Name,
		"age":    cp.Age,
		"gender": cp.Gender,
	}

	// marshalled, _ :=json.Marshal(Person{name, age, gender})

	resp, _ := c.HTTPClient.R().
		SetBody(personMap).
		Post("http://localhost:8000/")

	var p Person
	err := json.Unmarshal(resp.Body(), &p)
	return p, err
}

func (c *Client) UpdatePerson(cp Person) (Person, error) {

	personMap := map[string]interface{}{
		"name":   cp.Name,
		"age":    cp.Age,
		"gender": cp.Gender,
	}

	// marshalled, _ :=json.Marshal(Person{name, age, gender})

	resp, _ := c.HTTPClient.R().
		SetBody(personMap).
		Put(fmt.Sprintf("http://localhost:8000/%s", strconv.Itoa(cp.ID)))

	var p Person
	err := json.Unmarshal(resp.Body(), &p)
	return p, err
}

func (c *Client) DeletePerson(id int) error {
	_, err := c.HTTPClient.R().
		Delete(fmt.Sprintf("http://localhost:8000/%s", strconv.Itoa(id)))

	return err

}
