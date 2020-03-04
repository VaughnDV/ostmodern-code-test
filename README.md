# Ostmodern Python Code Test

The idea is to build a platform on which your users can buy and sell Starships.
To make this process more transparent, it has been decided to source some
technical information about the Starships on sale from the [Starship
API](https://swapi.co/documentation#starships).

## Getting started

```shell
# For Docker
docker-compose up
# You can run `manage.py` commands using the `./manapy` wrapper

# For Vagrant
vagrant up
vagrant ssh
# Inside the box
./manage.py runserver 0.0.0.0:8008
```
* The default Django "It worked!" page should now be available at
  http://localhost:8008/

## Usage

* To import Starships data from the from the StarWars API run:
  
  ```shell
  docker-compose run --rm code-test ./manage.py fetch_starships
  ```
  
* To run the tests:

    ```shell
    docker-compose run --rm code-test ./manage.py test
    ```
  
* A potential buyer can browse all Starships:

    ```shell
    http://localhost:8008/shiptrader/starships/
  ```

     
* A potential buyer can browse all the listings

    ```shell
    http://localhost:8008/shiptrader/starships/
    ```

* A potential buyer can browse all the listings for a given `starship_class`

    ```shell
    http://localhost:8008/shiptrader/listings/?search=your_starship_class
    ```
    
        
* A potential buyer can sort listings by price or time of listing
    ```shell
    # Ascending:
    http://localhost:8008/shiptrader/listings/?ordering=price
    http://localhost:8008/shiptrader/listings/?ordering=created_at
    
    # Descending:
    http://localhost:8008/shiptrader/listings/?ordering=-price
    http://localhost:8008/shiptrader/listings/?ordering=-created_at
  ```
    
* Filtering and sorting can be combined:
 
    ```shell 
    http://localhost:8008/shiptrader/listings/?search=ship_type&ordering=-price
    ```
    
* To list/create a Starship as for sale, the user has to `POST` the Starship name and
  list price to the listings endpoint, ship type is optional
  
  Example body:
  ```shell
  {"name": "May Awesome Ship", "price": "999", "ship_type": 12}
  ```
  
  listings endpoint:
  ```http://localhost:8008/shiptrader/listings/```
  
* A seller can deactivate and reactivate their listing by sending a `PATCH` to the manage listing endpoint

   Example body:
  ```shell
  {"active": "true"}
  ```
  
   Example manage listing url, with the required listing id at the end:
   ```http://localhost:8008/shiptrader/listings/12```
   
   Note that only the listing `active` state can be updated. Other fields if supplied will be ignored
    

