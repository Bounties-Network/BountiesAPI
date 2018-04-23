import React from 'react';
import ReactDOM from 'react-dom';

import { createStore, applyMiddleware, compose } from 'redux';
import createSagaMiddleware from 'redux-saga';
import { Provider } from 'react-redux';

import reducer from './redux';
import watcherSaga from './sagas';

import App from './App';
import registerServiceWorker from './registerServiceWorker';

// create the saga middleware
const sagaMiddleware = createSagaMiddleware();

// create a redux store with our reducer above and middleware
const store = createStore(
  reducer,
  compose(applyMiddleware(sagaMiddleware))
);

// run the saga
sagaMiddleware.run(watcherSaga);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);
registerServiceWorker();
