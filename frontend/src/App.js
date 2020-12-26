import React from 'react';
import { Provider } from 'react-redux';
import { Router } from 'react-router';
import { createBrowserHistory } from 'history';

import MediaQuery from 'containers/MediaQuery';
import Loading from 'containers/Loading';

import config from 'config';
import Routes from './routes';
import store from './redux/store';

import './app.css';

const history = createBrowserHistory({ basename: config.BASE_URL });

function App() {
  return (
    <Router history={history}>
      <Provider store={store}>
        <Routes />
        <MediaQuery />
        <Loading />
      </Provider>
    </Router>
  );
}

export default App;
