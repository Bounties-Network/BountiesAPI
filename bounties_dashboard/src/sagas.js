import { takeLatest, call, put } from 'redux-saga/effects';
import axios from 'axios';
import moment from 'moment';

const dateFormat = 'YYYY-MM-DD';

function dummy(fromDate, toDate) {
  const data = [];
  let date = moment(fromDate, dateFormat);

  while (date < moment(toDate, dateFormat)) {
    data.push({
      date: date.format(dateFormat),
      bounties_issued: Math.floor(Math.random() * 44),
      fulfillments_submitted: Math.floor(Math.random() * 23),
      fulfillments_accepted: Math.floor(Math.random() * 21),
      fulfillments_pending_acceptance: Math.floor(Math.random() * 5),
      fulfillment_acceptance_rate: Math.random(),
      bounty_fulfilled_rate: Math.random(),
      avg_fulfiller_acceptance_rate: Math.random(),
      avg_fulfillment_amount: Math.random(),
      total_fulfillment_amount: Math.floor(Math.random() * 184),
      bounty_draft: Math.floor(Math.random() * 11),
      bounty_active: Math.floor(Math.random() * 48),
      bounty_completed: Math.floor(Math.random() * 22),
      bounty_expired: Math.floor(Math.random() * 5),
      bounty_dead: Math.floor(Math.random() * 11)
    });
    date = date.add(1, 'days');
  }
  return data;
}

function fetchData(schema, fromDate, toDate) {
  if (schema === 'test') {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(Object.assign({}, {
          data: dummy(fromDate, toDate)
        }));
      }, 1000);
    });
  }
  return axios({
    method: 'get',
    params: {
      publish_date__range: `${fromDate},${toDate}`,
      schema: (schema === 'all' ? null : schema)
    },
    url: 'https://api.bounties.network/analytics/stats'
  });
}

function parseData(raw) {
  const bountyDraft = [];
  const bountyActive = [];
  const bountyCompleted = [];
  const bountyExpired = [];
  const bountyDead = [];

  const fulfillmentAcceptanceRate = [];
  const bountyFulfilledRate = [];
  const avgFulfillerAcceptanceRate = [];

  const bountiesIssued = [];
  const fulfillmentsSubmitted = [];
  const fulfillmentsAccepted = [];
  const fulfillmentsPendingAcceptance = [];
  const avgFulfillmentAmount = [];

  for (let i = 0; i < raw.length; i += 1) {
    const date = Date.parse(raw[i].date);
    bountyDraft.push([date, raw[i].bounty_draft]);
    bountyActive.push([date, raw[i].bounty_active]);
    bountyCompleted.push([date, raw[i].bounty_completed]);
    bountyExpired.push([date, raw[i].bounty_expired]);
    bountyDead.push([date, raw[i].bounty_dead]);

    fulfillmentAcceptanceRate.push([date, raw[i].fulfillment_acceptance_rate]);
    bountyFulfilledRate.push([date, raw[i].bounty_fulfilled_rate]);
    avgFulfillerAcceptanceRate.push([date, raw[i].avg_fulfiller_acceptance_rate]);

    bountiesIssued.push([date, raw[i].bounties_issued]);
    fulfillmentsSubmitted.push([date, raw[i].fulfillments_submitted]);
    fulfillmentsAccepted.push([date, raw[i].fulfillments_accepted]);

    fulfillmentsPendingAcceptance.push([date, raw[i].fulfillments_pending_acceptance]);
    avgFulfillmentAmount.push([date, raw[i].avg_fulfillment_amount]);
  }

  return {
    bountyDraft,
    bountyActive,
    bountyCompleted,
    bountyExpired,
    bountyDead,

    fulfillmentAcceptanceRate,
    bountyFulfilledRate,
    avgFulfillerAcceptanceRate,

    bountiesIssued,
    fulfillmentsSubmitted,
    fulfillmentsAccepted,

    fulfillmentsPendingAcceptance,
    avgFulfillmentAmount
  };
}

// function that makes the api request and returns a Promise for response
function getData(schema, fromDate, toDate) {
  return fetchData(schema, fromDate, toDate)
    .then(res => parseData(res.data));
}

// worker saga: makes the api call when watcher saga sees the action
function* workerSaga(params) {
  try {
    const data = yield call(
      getData,
      params.schema,
      params.range[0].format(dateFormat),
      params.range[1].format(dateFormat)
    );

    // dispatch a success action to the store with the new data
    yield put({ type: 'API_CALL_SUCCESS', data });
  } catch (error) {
    // dispatch a failure action to the store with the error
    yield put({ type: 'API_CALL_FAILURE', error });
  }
}

// watcher saga: watches for actions dispatched to the store, starts worker saga
export default function* watcherSaga() {
  yield takeLatest('API_CALL_REQUEST', workerSaga);
}
