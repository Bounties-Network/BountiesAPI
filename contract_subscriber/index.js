require("@babel/register")({ extensions: [".js", ".jsx", ".ts", ".tsx"] });

console.info("STARTING contract_subscriber");
const handler = require("./src/handler").default;

handler().catch(console.error);
