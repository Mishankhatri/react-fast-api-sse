# react-fast-api-sse

A simple implementation of SSE in react - fastapi

## 🏁 Getting Started <a name = "getting_started"></a>

- Clone the repository or download the zip file

### For server

- For zip file extract it, then cd into the `server` directory 

- Create new virtualenv using python's [virtualenv](https://pypi.org/project/virtualenv/) package:

    ```
    virtualenv venv

    venv\Scripts\activate (in windows) or $source venv/bin/activate (in Mac OS/linux)

    ```

- Install all dependencies by executing the following command:

    ```pwsh
    $pip install -r requirements.txt
    ```

- For running the application simply execute the following commands:

    ```pwsh
    $uvicorn server:app --reload
    ```

### For client 
- cd into the `client` directory 

-   Install all node modules
    ```pwsh
    $npm install 
    ```
-   To run
    ```pwsh
    $npm run dev 
    ```


