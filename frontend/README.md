# Susun Jadwal Frontend

## Requirements

1. `Node.js` and `npm`

## Configuration

### Development

1. Install all dependencies using `npm install`
2. Run the project by using `npm start`


### Development with Docker

1. Start the container with `docker-compose up --build`
2. Access the app at port 3001, e.g. `localhost:3001`

### Unit Testing

1. Run the unit test by using `npm run test`
2. Run the unit test with showing code coverage by using `npm run test -- --coverage`

### Linter and fixes files

1. Run linter by using `npm run lint`
2. Force to fix code `npm run lint --fix`

### Production

1. Run `npm run build`
2. Set your Nginx (or other server of your choice) to serve `build` folder. For example:

```
location /susunjadwal {
    alias /path/to/susunjadwal/frontend/build;
    try_files $uri /index.html =404;
}
```

## License

See LICENSE.md. This software actually goes a long way back, thank you so much to everyone involved.
