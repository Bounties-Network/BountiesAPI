import Rollbar from "rollbar";

const rollbarToken = process.env["rollbar_token"];
const rollbar = new Rollbar({
  enabled: rollbarToken ? true : false,
  payload: {
    environment: process.env["environment"] || "local"
  },
  accessToken: rollbarToken,
  captureUncaught: true,
  captureUnhandledRejections: true
});

export default rollbar;
