"use strict";
require("@babel/register")({ extensions: [".js", ".jsx", ".ts", ".tsx"] });

const handler = require("./src/handler").default;

handler().catch(console.error);
