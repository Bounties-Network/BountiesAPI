import { takeLatest, call, put } from 'redux-saga/effects';
import axios from 'axios';

const dateFormat = 'YYYY-MM-DD';

// function that makes the api request and returns a Promise for response
function fetchData(schema, fromDate, toDate) {
  if (schema === 'test') {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(Object.assign({}, {
          data: [{
            date: '2016-01-01',
            bounties_issued: 44,
            fulfillments_submitted: 23,
            fulfillments_accepted: 21,
            fulfillments_pending_acceptance: 2,
            fulfillment_acceptance_rate: .91,
            bounty_fulfilled_rate: .83,
            avg_fulfiller_acceptance_rate: .73,
            avg_fulfillment_amount: 45.32,
            total_fulfillment_amount: 184,
            bounty_draft: 11,
            bounty_active: 48,
            bounty_completed: 22,
            bounty_expired: 5,
            bounty_dead: 11
          }, {
            date: '2016-01-02',
            bounties_issued: 44,
            fulfillments_submitted: 23,
            fulfillments_accepted: 21,
            fulfillments_pending_acceptance: 2,
            fulfillment_acceptance_rate: .91,
            bounty_fulfilled_rate: .83,
            avg_fulfiller_acceptance_rate: .73,
            avg_fulfillment_amount: 45.32,
            total_fulfillment_amount: 184,
            bounty_draft: 11,
            bounty_active: 48,
            bounty_completed: 22,
            bounty_expired: 5,
            bounty_dead: 11
          }]
        }));
      }, 1000);
    });
  }
  return axios({
    method: 'get',
    params: {
      publish_date__range: `${fromDate},${toDate}`,
      schema
    },
    url: 'https://api.bounties.network/analytics/stats'
  });
}

// worker saga: makes the api call when watcher saga sees the action
function* workerSaga(params) {
  try {
    const response = yield call(
      fetchData,
      params.schema,
      params.range[0].format(dateFormat),
      params.range[1].format(dateFormat)
    );

    // dispatch a success action to the store with the new data
    yield put({ type: 'API_CALL_SUCCESS', data: response.data });
  } catch (error) {
    // dispatch a failure action to the store with the error
    yield put({ type: 'API_CALL_FAILURE', error });
  }
}

// watcher saga: watches for actions dispatched to the store, starts worker saga
export default function* watcherSaga() {
  yield takeLatest('API_CALL_REQUEST', workerSaga);
}
