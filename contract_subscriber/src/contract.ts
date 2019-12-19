const contract: { version: { [key: string]: any } } = {
  version: {
    v1: {
      mainNet: "0x2af47a65da8CD66729b4209C22017d6A5C2d2400",
      rinkeby: "0xf209d2b723b6417cbf04c07e733bee776105a073",
      consensysrinkeby: "0x12708d61650c2462f2e10276e0e65239d9b0df4e",
      rinkebystaging: "0xdd1636b88e9071507e859e61991ed4be6647f420",
      interfaces: {
        StandardBounties: [
          {
            constant: false,
            inputs: [{ name: "_bountyId", type: "uint256" }],
            name: "killBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_bountyId", type: "uint256" }],
            name: "getBountyToken",
            outputs: [{ name: "", type: "address" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_data", type: "string" }
            ],
            name: "fulfillBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_newDeadline", type: "uint256" }
            ],
            name: "extendDeadline",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "getNumBounties",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillmentId", type: "uint256" },
              { name: "_data", type: "string" }
            ],
            name: "updateFulfillment",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_newFulfillmentAmount", type: "uint256" },
              { name: "_value", type: "uint256" }
            ],
            name: "increasePayout",
            outputs: [],
            payable: true,
            stateMutability: "payable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_newFulfillmentAmount", type: "uint256" }
            ],
            name: "changeBountyFulfillmentAmount",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_newIssuer", type: "address" }
            ],
            name: "transferIssuer",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_value", type: "uint256" }
            ],
            name: "activateBounty",
            outputs: [],
            payable: true,
            stateMutability: "payable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_issuer", type: "address" },
              { name: "_deadline", type: "uint256" },
              { name: "_data", type: "string" },
              { name: "_fulfillmentAmount", type: "uint256" },
              { name: "_arbiter", type: "address" },
              { name: "_paysTokens", type: "bool" },
              { name: "_tokenContract", type: "address" }
            ],
            name: "issueBounty",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_issuer", type: "address" },
              { name: "_deadline", type: "uint256" },
              { name: "_data", type: "string" },
              { name: "_fulfillmentAmount", type: "uint256" },
              { name: "_arbiter", type: "address" },
              { name: "_paysTokens", type: "bool" },
              { name: "_tokenContract", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "issueAndActivateBounty",
            outputs: [{ name: "", type: "uint256" }],
            payable: true,
            stateMutability: "payable",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_bountyId", type: "uint256" }],
            name: "getBountyArbiter",
            outputs: [{ name: "", type: "address" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_value", type: "uint256" }
            ],
            name: "contribute",
            outputs: [],
            payable: true,
            stateMutability: "payable",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "owner",
            outputs: [{ name: "", type: "address" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_newPaysTokens", type: "bool" },
              { name: "_newTokenContract", type: "address" }
            ],
            name: "changeBountyPaysTokens",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_bountyId", type: "uint256" }],
            name: "getBountyData",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillmentId", type: "uint256" }
            ],
            name: "getFulfillment",
            outputs: [
              { name: "", type: "bool" },
              { name: "", type: "address" },
              { name: "", type: "string" }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_newArbiter", type: "address" }
            ],
            name: "changeBountyArbiter",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_newDeadline", type: "uint256" }
            ],
            name: "changeBountyDeadline",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillmentId", type: "uint256" }
            ],
            name: "acceptFulfillment",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "", type: "uint256" }],
            name: "bounties",
            outputs: [
              { name: "issuer", type: "address" },
              { name: "deadline", type: "uint256" },
              { name: "data", type: "string" },
              { name: "fulfillmentAmount", type: "uint256" },
              { name: "arbiter", type: "address" },
              { name: "paysTokens", type: "bool" },
              { name: "bountyStage", type: "uint8" },
              { name: "balance", type: "uint256" }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_bountyId", type: "uint256" }],
            name: "getBounty",
            outputs: [
              { name: "", type: "address" },
              { name: "", type: "uint256" },
              { name: "", type: "uint256" },
              { name: "", type: "bool" },
              { name: "", type: "uint256" },
              { name: "", type: "uint256" }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_bountyId", type: "uint256" },
              { name: "_newData", type: "string" }
            ],
            name: "changeBountyData",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_bountyId", type: "uint256" }],
            name: "getNumFulfillments",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            inputs: [{ name: "_owner", type: "address" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "constructor"
          },
          {
            anonymous: false,
            inputs: [{ indexed: false, name: "bountyId", type: "uint256" }],
            name: "BountyIssued",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "bountyId", type: "uint256" },
              { indexed: false, name: "issuer", type: "address" }
            ],
            name: "BountyActivated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "bountyId", type: "uint256" },
              { indexed: true, name: "fulfiller", type: "address" },
              { indexed: true, name: "_fulfillmentId", type: "uint256" }
            ],
            name: "BountyFulfilled",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" }
            ],
            name: "FulfillmentUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "bountyId", type: "uint256" },
              { indexed: true, name: "fulfiller", type: "address" },
              { indexed: true, name: "_fulfillmentId", type: "uint256" }
            ],
            name: "FulfillmentAccepted",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "bountyId", type: "uint256" },
              { indexed: true, name: "issuer", type: "address" }
            ],
            name: "BountyKilled",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "bountyId", type: "uint256" },
              { indexed: true, name: "contributor", type: "address" },
              { indexed: false, name: "value", type: "uint256" }
            ],
            name: "ContributionAdded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "bountyId", type: "uint256" },
              { indexed: false, name: "newDeadline", type: "uint256" }
            ],
            name: "DeadlineExtended",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [{ indexed: false, name: "bountyId", type: "uint256" }],
            name: "BountyChanged",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: true, name: "_newIssuer", type: "address" }
            ],
            name: "IssuerTransferred",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_newFulfillmentAmount", type: "uint256" }
            ],
            name: "PayoutIncreased",
            type: "event"
          }
        ],
        HumanStandardToken: [
          {
            constant: true,
            inputs: [],
            name: "name",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_spender", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "approve",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "totalSupply",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_from", type: "address" },
              { name: "_to", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "transferFrom",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "decimals",
            outputs: [{ name: "", type: "uint8" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "version",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_owner", type: "address" }],
            name: "balanceOf",
            outputs: [{ name: "balance", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "symbol",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_to", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "transfer",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_spender", type: "address" },
              { name: "_value", type: "uint256" },
              { name: "_extraData", type: "bytes" }
            ],
            name: "approveAndCall",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [
              { name: "_owner", type: "address" },
              { name: "_spender", type: "address" }
            ],
            name: "allowance",
            outputs: [{ name: "remaining", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            inputs: [
              { name: "_initialAmount", type: "uint256" },
              { name: "_tokenName", type: "string" },
              { name: "_decimalUnits", type: "uint8" },
              { name: "_tokenSymbol", type: "string" }
            ],
            payable: false,
            stateMutability: "nonpayable",
            type: "constructor"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: true, name: "_from", type: "address" },
              { indexed: true, name: "_to", type: "address" },
              { indexed: false, name: "_value", type: "uint256" }
            ],
            name: "Transfer",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: true, name: "_owner", type: "address" },
              { indexed: true, name: "_spender", type: "address" },
              { indexed: false, name: "_value", type: "uint256" }
            ],
            name: "Approval",
            type: "event"
          }
        ]
      }
    },
    v2: {
      mainNet: "0xE7F69EA2a79521136eE0bf3c50f6B5F1Ea0AB0cd",
      rinkebystaging: "0xa78c680ceaa0de08ee58a28c82193fcfae22379c",
      rinkeby: "0xa78c680ceaa0de08ee58a28c82193fcfae22379c",
      interfaces: {
        StandardBounties: [
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillmentId", type: "uint256" },
              { name: "_approverId", type: "uint256" },
              { name: "_tokenAmounts", type: "uint256[]" }
            ],
            name: "acceptFulfillment",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_approvers", type: "address[]" }
            ],
            name: "addApprovers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuers", type: "address[]" }
            ],
            name: "addIssuers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_approverId", type: "uint256" },
              { name: "_approver", type: "address" }
            ],
            name: "changeApprover",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuers", type: "address[]" },
              { name: "_approvers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_deadline", type: "uint256" }
            ],
            name: "changeBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_data", type: "string" }
            ],
            name: "changeData",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_deadline", type: "uint256" }
            ],
            name: "changeDeadline",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuerIdToChange", type: "uint256" },
              { name: "_newIssuer", type: "address" }
            ],
            name: "changeIssuer",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_amount", type: "uint256" }
            ],
            name: "contribute",
            outputs: [],
            payable: true,
            stateMutability: "payable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_amounts", type: "uint256[]" }
            ],
            name: "drainBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_approverId", type: "uint256" },
              { name: "_tokenAmounts", type: "uint256[]" }
            ],
            name: "fulfillAndAccept",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillers", type: "address[]" },
              { name: "_data", type: "string" }
            ],
            name: "fulfillBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_issuers", type: "address[]" },
              { name: "_approvers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_deadline", type: "uint256" },
              { name: "_token", type: "address" },
              { name: "_tokenVersion", type: "uint256" },
              { name: "_depositAmount", type: "uint256" }
            ],
            name: "issueAndContribute",
            outputs: [{ name: "", type: "uint256" }],
            payable: true,
            stateMutability: "payable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_issuers", type: "address[]" },
              { name: "_approvers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_deadline", type: "uint256" },
              { name: "_token", type: "address" },
              { name: "_tokenVersion", type: "uint256" }
            ],
            name: "issueBounty",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_data", type: "string" }
            ],
            name: "performAction",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_contributionId", type: "uint256" }
            ],
            name: "refundContribution",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_contributionIds", type: "uint256[]" }
            ],
            name: "refundContributions",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_contributionIds", type: "uint256[]" }
            ],
            name: "refundMyContributions",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_approvers", type: "address[]" }
            ],
            name: "replaceApprovers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuers", type: "address[]" }
            ],
            name: "replaceIssuers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [{ name: "_relayer", type: "address" }],
            name: "setMetaTxRelayer",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillmentId", type: "uint256" },
              { name: "_fulfillers", type: "address[]" },
              { name: "_data", type: "string" }
            ],
            name: "updateFulfillment",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          { inputs: [], payable: false, stateMutability: "nonpayable", type: "constructor" },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_creator", type: "address" },
              { indexed: false, name: "_issuers", type: "address[]" },
              { indexed: false, name: "_approvers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" },
              { indexed: false, name: "_deadline", type: "uint256" },
              { indexed: false, name: "_token", type: "address" },
              { indexed: false, name: "_tokenVersion", type: "uint256" }
            ],
            name: "BountyIssued",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_contributionId", type: "uint256" },
              { indexed: false, name: "_contributor", type: "address" },
              { indexed: false, name: "_amount", type: "uint256" }
            ],
            name: "ContributionAdded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_contributionId", type: "uint256" }
            ],
            name: "ContributionRefunded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_issuer", type: "address" },
              { indexed: false, name: "_contributionIds", type: "uint256[]" }
            ],
            name: "ContributionsRefunded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_issuer", type: "address" },
              { indexed: false, name: "_amounts", type: "uint256[]" }
            ],
            name: "BountyDrained",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfiller", type: "address" },
              { indexed: false, name: "_data", type: "string" }
            ],
            name: "ActionPerformed",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" },
              { indexed: false, name: "_fulfillers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" },
              { indexed: false, name: "_submitter", type: "address" }
            ],
            name: "BountyFulfilled",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" },
              { indexed: false, name: "_fulfillers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" }
            ],
            name: "FulfillmentUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" },
              { indexed: false, name: "_approver", type: "address" },
              { indexed: false, name: "_tokenAmounts", type: "uint256[]" }
            ],
            name: "FulfillmentAccepted",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_issuers", type: "address[]" },
              { indexed: false, name: "_approvers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" },
              { indexed: false, name: "_deadline", type: "uint256" }
            ],
            name: "BountyChanged",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_issuers", type: "address[]" }
            ],
            name: "BountyIssuersUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_approvers", type: "address[]" }
            ],
            name: "BountyApproversUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_data", type: "string" }
            ],
            name: "BountyDataChanged",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_deadline", type: "uint256" }
            ],
            name: "BountyDeadlineChanged",
            type: "event"
          },
          {
            constant: true,
            inputs: [{ name: "", type: "uint256" }],
            name: "bounties",
            outputs: [
              { name: "deadline", type: "uint256" },
              { name: "token", type: "address" },
              { name: "tokenVersion", type: "uint256" },
              { name: "balance", type: "uint256" },
              { name: "hasPaidOut", type: "bool" }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "callStarted",
            outputs: [{ name: "", type: "bool" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_bountyId", type: "uint256" }],
            name: "getBounty",
            outputs: [
              {
                components: [
                  { name: "issuers", type: "address[]" },
                  { name: "approvers", type: "address[]" },
                  { name: "deadline", type: "uint256" },
                  { name: "token", type: "address" },
                  { name: "tokenVersion", type: "uint256" },
                  { name: "balance", type: "uint256" },
                  { name: "hasPaidOut", type: "bool" },
                  {
                    components: [
                      { name: "fulfillers", type: "address[]" },
                      { name: "submitter", type: "address" }
                    ],
                    name: "fulfillments",
                    type: "tuple[]"
                  },
                  {
                    components: [
                      { name: "contributor", type: "address" },
                      { name: "amount", type: "uint256" },
                      { name: "refunded", type: "bool" }
                    ],
                    name: "contributions",
                    type: "tuple[]"
                  }
                ],
                name: "",
                type: "tuple"
              }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "metaTxRelayer",
            outputs: [{ name: "", type: "address" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "numBounties",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "owner",
            outputs: [{ name: "", type: "address" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [
              { name: "", type: "uint256" },
              { name: "", type: "uint256" }
            ],
            name: "tokenBalances",
            outputs: [{ name: "", type: "bool" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          }
        ],
        HumanStandardToken: [
          {
            constant: true,
            inputs: [],
            name: "name",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_spender", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "approve",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "totalSupply",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_from", type: "address" },
              { name: "_to", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "transferFrom",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "decimals",
            outputs: [{ name: "", type: "uint8" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "version",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_owner", type: "address" }],
            name: "balanceOf",
            outputs: [{ name: "balance", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "symbol",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_to", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "transfer",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_spender", type: "address" },
              { name: "_value", type: "uint256" },
              { name: "_extraData", type: "bytes" }
            ],
            name: "approveAndCall",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [
              { name: "_owner", type: "address" },
              { name: "_spender", type: "address" }
            ],
            name: "allowance",
            outputs: [{ name: "remaining", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            inputs: [
              { name: "_initialAmount", type: "uint256" },
              { name: "_tokenName", type: "string" },
              { name: "_decimalUnits", type: "uint8" },
              { name: "_tokenSymbol", type: "string" }
            ],
            payable: false,
            stateMutability: "nonpayable",
            type: "constructor"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: true, name: "_from", type: "address" },
              { indexed: true, name: "_to", type: "address" },
              { indexed: false, name: "_value", type: "uint256" }
            ],
            name: "Transfer",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: true, name: "_owner", type: "address" },
              { indexed: true, name: "_spender", type: "address" },
              { indexed: false, name: "_value", type: "uint256" }
            ],
            name: "Approval",
            type: "event"
          }
        ]
      }
    },
    "v2.1": {
      mainNet: "0x43ee232734097b07803ea605b49c6ee6bf10f8cc",
      rinkebystaging: "0x38f1886081759f7d352c28984908d04e8d2205a6",
      rinkeby: "0x38f1886081759f7d352c28984908d04e8d2205a6",
      interfaces: {
        StandardBounties: [
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillmentId", type: "uint256" },
              { name: "_approverId", type: "uint256" },
              { name: "_tokenAmounts", type: "uint256[]" }
            ],
            name: "acceptFulfillment",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_approvers", type: "address[]" }
            ],
            name: "addApprovers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuers", type: "address[]" }
            ],
            name: "addIssuers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_approverId", type: "uint256" },
              { name: "_approver", type: "address" }
            ],
            name: "changeApprover",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuers", type: "address[]" },
              { name: "_approvers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_deadline", type: "uint256" }
            ],
            name: "changeBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_data", type: "string" }
            ],
            name: "changeData",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_deadline", type: "uint256" }
            ],
            name: "changeDeadline",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuerIdToChange", type: "uint256" },
              { name: "_newIssuer", type: "address" }
            ],
            name: "changeIssuer",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_amount", type: "uint256" }
            ],
            name: "contribute",
            outputs: [],
            payable: true,
            stateMutability: "payable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_amounts", type: "uint256[]" }
            ],
            name: "drainBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_approverId", type: "uint256" },
              { name: "_tokenAmounts", type: "uint256[]" }
            ],
            name: "fulfillAndAccept",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillers", type: "address[]" },
              { name: "_data", type: "string" }
            ],
            name: "fulfillBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_issuers", type: "address[]" },
              { name: "_approvers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_deadline", type: "uint256" },
              { name: "_token", type: "address" },
              { name: "_tokenVersion", type: "uint256" },
              { name: "_depositAmount", type: "uint256" }
            ],
            name: "issueAndContribute",
            outputs: [{ name: "", type: "uint256" }],
            payable: true,
            stateMutability: "payable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_issuers", type: "address[]" },
              { name: "_approvers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_deadline", type: "uint256" },
              { name: "_token", type: "address" },
              { name: "_tokenVersion", type: "uint256" }
            ],
            name: "issueBounty",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_data", type: "string" }
            ],
            name: "performAction",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_contributionId", type: "uint256" }
            ],
            name: "refundContribution",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_contributionIds", type: "uint256[]" }
            ],
            name: "refundContributions",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_contributionIds", type: "uint256[]" }
            ],
            name: "refundMyContributions",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_approvers", type: "address[]" }
            ],
            name: "replaceApprovers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuers", type: "address[]" }
            ],
            name: "replaceIssuers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [{ name: "_relayer", type: "address" }],
            name: "setMetaTxRelayer",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillmentId", type: "uint256" },
              { name: "_fulfillers", type: "address[]" },
              { name: "_data", type: "string" }
            ],
            name: "updateFulfillment",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          { inputs: [], payable: false, stateMutability: "nonpayable", type: "constructor" },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_creator", type: "address" },
              { indexed: false, name: "_issuers", type: "address[]" },
              { indexed: false, name: "_approvers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" },
              { indexed: false, name: "_deadline", type: "uint256" },
              { indexed: false, name: "_token", type: "address" },
              { indexed: false, name: "_tokenVersion", type: "uint256" }
            ],
            name: "BountyIssued",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_contributionId", type: "uint256" },
              { indexed: false, name: "_contributor", type: "address" },
              { indexed: false, name: "_amount", type: "uint256" }
            ],
            name: "ContributionAdded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_contributionId", type: "uint256" }
            ],
            name: "ContributionRefunded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_issuer", type: "address" },
              { indexed: false, name: "_contributionIds", type: "uint256[]" }
            ],
            name: "ContributionsRefunded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_issuer", type: "address" },
              { indexed: false, name: "_amounts", type: "uint256[]" }
            ],
            name: "BountyDrained",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfiller", type: "address" },
              { indexed: false, name: "_data", type: "string" }
            ],
            name: "ActionPerformed",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" },
              { indexed: false, name: "_fulfillers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" },
              { indexed: false, name: "_submitter", type: "address" }
            ],
            name: "BountyFulfilled",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" },
              { indexed: false, name: "_fulfillers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" }
            ],
            name: "FulfillmentUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" },
              { indexed: false, name: "_approver", type: "address" },
              { indexed: false, name: "_tokenAmounts", type: "uint256[]" }
            ],
            name: "FulfillmentAccepted",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_issuers", type: "address[]" },
              { indexed: false, name: "_approvers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" },
              { indexed: false, name: "_deadline", type: "uint256" }
            ],
            name: "BountyChanged",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_issuers", type: "address[]" }
            ],
            name: "BountyIssuersUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_approvers", type: "address[]" }
            ],
            name: "BountyApproversUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_data", type: "string" }
            ],
            name: "BountyDataChanged",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_deadline", type: "uint256" }
            ],
            name: "BountyDeadlineChanged",
            type: "event"
          },
          {
            constant: true,
            inputs: [{ name: "", type: "uint256" }],
            name: "bounties",
            outputs: [
              { name: "deadline", type: "uint256" },
              { name: "token", type: "address" },
              { name: "tokenVersion", type: "uint256" },
              { name: "balance", type: "uint256" },
              { name: "hasPaidOut", type: "bool" }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "callStarted",
            outputs: [{ name: "", type: "bool" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_bountyId", type: "uint256" }],
            name: "getBounty",
            outputs: [
              {
                components: [
                  { name: "issuers", type: "address[]" },
                  { name: "approvers", type: "address[]" },
                  { name: "deadline", type: "uint256" },
                  { name: "token", type: "address" },
                  { name: "tokenVersion", type: "uint256" },
                  { name: "balance", type: "uint256" },
                  { name: "hasPaidOut", type: "bool" },
                  {
                    components: [
                      { name: "fulfillers", type: "address[]" },
                      { name: "submitter", type: "address" }
                    ],
                    name: "fulfillments",
                    type: "tuple[]"
                  },
                  {
                    components: [
                      { name: "contributor", type: "address" },
                      { name: "amount", type: "uint256" },
                      { name: "refunded", type: "bool" }
                    ],
                    name: "contributions",
                    type: "tuple[]"
                  }
                ],
                name: "",
                type: "tuple"
              }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "metaTxRelayer",
            outputs: [{ name: "", type: "address" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "numBounties",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "owner",
            outputs: [{ name: "", type: "address" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [
              { name: "", type: "uint256" },
              { name: "", type: "uint256" }
            ],
            name: "tokenBalances",
            outputs: [{ name: "", type: "bool" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          }
        ],
        HumanStandardToken: [
          {
            constant: true,
            inputs: [],
            name: "name",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_spender", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "approve",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "totalSupply",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_from", type: "address" },
              { name: "_to", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "transferFrom",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "decimals",
            outputs: [{ name: "", type: "uint8" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "version",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_owner", type: "address" }],
            name: "balanceOf",
            outputs: [{ name: "balance", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "symbol",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_to", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "transfer",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_spender", type: "address" },
              { name: "_value", type: "uint256" },
              { name: "_extraData", type: "bytes" }
            ],
            name: "approveAndCall",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [
              { name: "_owner", type: "address" },
              { name: "_spender", type: "address" }
            ],
            name: "allowance",
            outputs: [{ name: "remaining", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            inputs: [
              { name: "_initialAmount", type: "uint256" },
              { name: "_tokenName", type: "string" },
              { name: "_decimalUnits", type: "uint8" },
              { name: "_tokenSymbol", type: "string" }
            ],
            payable: false,
            stateMutability: "nonpayable",
            type: "constructor"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: true, name: "_from", type: "address" },
              { indexed: true, name: "_to", type: "address" },
              { indexed: false, name: "_value", type: "uint256" }
            ],
            name: "Transfer",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: true, name: "_owner", type: "address" },
              { indexed: true, name: "_spender", type: "address" },
              { indexed: false, name: "_value", type: "uint256" }
            ],
            name: "Approval",
            type: "event"
          }
        ]
      }
    },
    "v2.2": {
      mainNet: "0x6e77f91ba0ae5278763ec3f044a1f0e5f85fac0a",
      rinkebystaging: "0x9142dd986fe36952c1f8f5d68b814217dee45186",
      rinkeby: "0x9142dd986fe36952c1f8f5d68b814217dee45186",
      interfaces: {
        StandardBounties: [
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillmentId", type: "uint256" },
              { name: "_approverId", type: "uint256" },
              { name: "_tokenAmounts", type: "uint256[]" }
            ],
            name: "acceptFulfillment",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_approvers", type: "address[]" }
            ],
            name: "addApprovers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuers", type: "address[]" }
            ],
            name: "addIssuers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_approverId", type: "uint256" },
              { name: "_approver", type: "address" }
            ],
            name: "changeApprover",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuers", type: "address[]" },
              { name: "_approvers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_deadline", type: "uint256" }
            ],
            name: "changeBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_data", type: "string" }
            ],
            name: "changeData",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_deadline", type: "uint256" }
            ],
            name: "changeDeadline",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuerIdToChange", type: "uint256" },
              { name: "_newIssuer", type: "address" }
            ],
            name: "changeIssuer",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_amount", type: "uint256" }
            ],
            name: "contribute",
            outputs: [],
            payable: true,
            stateMutability: "payable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_amounts", type: "uint256[]" }
            ],
            name: "drainBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_approverId", type: "uint256" },
              { name: "_tokenAmounts", type: "uint256[]" }
            ],
            name: "fulfillAndAccept",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillers", type: "address[]" },
              { name: "_data", type: "string" }
            ],
            name: "fulfillBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_issuers", type: "address[]" },
              { name: "_approvers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_deadline", type: "uint256" },
              { name: "_token", type: "address" },
              { name: "_tokenVersion", type: "uint256" },
              { name: "_depositAmount", type: "uint256" }
            ],
            name: "issueAndContribute",
            outputs: [{ name: "", type: "uint256" }],
            payable: true,
            stateMutability: "payable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_issuers", type: "address[]" },
              { name: "_approvers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_deadline", type: "uint256" },
              { name: "_token", type: "address" },
              { name: "_tokenVersion", type: "uint256" }
            ],
            name: "issueBounty",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_data", type: "string" }
            ],
            name: "performAction",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_contributionId", type: "uint256" }
            ],
            name: "refundContribution",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_contributionIds", type: "uint256[]" }
            ],
            name: "refundContributions",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_contributionIds", type: "uint256[]" }
            ],
            name: "refundMyContributions",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_approvers", type: "address[]" }
            ],
            name: "replaceApprovers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuers", type: "address[]" }
            ],
            name: "replaceIssuers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [{ name: "_relayer", type: "address" }],
            name: "setMetaTxRelayer",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillmentId", type: "uint256" },
              { name: "_fulfillers", type: "address[]" },
              { name: "_data", type: "string" }
            ],
            name: "updateFulfillment",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          { inputs: [], payable: false, stateMutability: "nonpayable", type: "constructor" },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_creator", type: "address" },
              { indexed: false, name: "_issuers", type: "address[]" },
              { indexed: false, name: "_approvers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" },
              { indexed: false, name: "_deadline", type: "uint256" },
              { indexed: false, name: "_token", type: "address" },
              { indexed: false, name: "_tokenVersion", type: "uint256" }
            ],
            name: "BountyIssued",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_contributionId", type: "uint256" },
              { indexed: false, name: "_contributor", type: "address" },
              { indexed: false, name: "_amount", type: "uint256" }
            ],
            name: "ContributionAdded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_contributionId", type: "uint256" }
            ],
            name: "ContributionRefunded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_issuer", type: "address" },
              { indexed: false, name: "_contributionIds", type: "uint256[]" }
            ],
            name: "ContributionsRefunded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_issuer", type: "address" },
              { indexed: false, name: "_amounts", type: "uint256[]" }
            ],
            name: "BountyDrained",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfiller", type: "address" },
              { indexed: false, name: "_data", type: "string" }
            ],
            name: "ActionPerformed",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" },
              { indexed: false, name: "_fulfillers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" },
              { indexed: false, name: "_submitter", type: "address" }
            ],
            name: "BountyFulfilled",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" },
              { indexed: false, name: "_fulfillers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" }
            ],
            name: "FulfillmentUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" },
              { indexed: false, name: "_approver", type: "address" },
              { indexed: false, name: "_tokenAmounts", type: "uint256[]" }
            ],
            name: "FulfillmentAccepted",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_issuers", type: "address[]" },
              { indexed: false, name: "_approvers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" },
              { indexed: false, name: "_deadline", type: "uint256" }
            ],
            name: "BountyChanged",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_issuers", type: "address[]" }
            ],
            name: "BountyIssuersUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_approvers", type: "address[]" }
            ],
            name: "BountyApproversUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_data", type: "string" }
            ],
            name: "BountyDataChanged",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_deadline", type: "uint256" }
            ],
            name: "BountyDeadlineChanged",
            type: "event"
          },
          {
            constant: true,
            inputs: [{ name: "", type: "uint256" }],
            name: "bounties",
            outputs: [
              { name: "deadline", type: "uint256" },
              { name: "token", type: "address" },
              { name: "tokenVersion", type: "uint256" },
              { name: "balance", type: "uint256" },
              { name: "hasPaidOut", type: "bool" }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "callStarted",
            outputs: [{ name: "", type: "bool" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_bountyId", type: "uint256" }],
            name: "getBounty",
            outputs: [
              {
                components: [
                  { name: "issuers", type: "address[]" },
                  { name: "approvers", type: "address[]" },
                  { name: "deadline", type: "uint256" },
                  { name: "token", type: "address" },
                  { name: "tokenVersion", type: "uint256" },
                  { name: "balance", type: "uint256" },
                  { name: "hasPaidOut", type: "bool" },
                  {
                    components: [
                      { name: "fulfillers", type: "address[]" },
                      { name: "submitter", type: "address" }
                    ],
                    name: "fulfillments",
                    type: "tuple[]"
                  },
                  {
                    components: [
                      { name: "contributor", type: "address" },
                      { name: "amount", type: "uint256" },
                      { name: "refunded", type: "bool" }
                    ],
                    name: "contributions",
                    type: "tuple[]"
                  }
                ],
                name: "",
                type: "tuple"
              }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "metaTxRelayer",
            outputs: [{ name: "", type: "address" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "numBounties",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "owner",
            outputs: [{ name: "", type: "address" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [
              { name: "", type: "uint256" },
              { name: "", type: "uint256" }
            ],
            name: "tokenBalances",
            outputs: [{ name: "", type: "bool" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          }
        ],
        HumanStandardToken: [
          {
            constant: true,
            inputs: [],
            name: "name",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_spender", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "approve",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "totalSupply",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_from", type: "address" },
              { name: "_to", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "transferFrom",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "decimals",
            outputs: [{ name: "", type: "uint8" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "version",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_owner", type: "address" }],
            name: "balanceOf",
            outputs: [{ name: "balance", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "symbol",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_to", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "transfer",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_spender", type: "address" },
              { name: "_value", type: "uint256" },
              { name: "_extraData", type: "bytes" }
            ],
            name: "approveAndCall",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [
              { name: "_owner", type: "address" },
              { name: "_spender", type: "address" }
            ],
            name: "allowance",
            outputs: [{ name: "remaining", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            inputs: [
              { name: "_initialAmount", type: "uint256" },
              { name: "_tokenName", type: "string" },
              { name: "_decimalUnits", type: "uint8" },
              { name: "_tokenSymbol", type: "string" }
            ],
            payable: false,
            stateMutability: "nonpayable",
            type: "constructor"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: true, name: "_from", type: "address" },
              { indexed: true, name: "_to", type: "address" },
              { indexed: false, name: "_value", type: "uint256" }
            ],
            name: "Transfer",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: true, name: "_owner", type: "address" },
              { indexed: true, name: "_spender", type: "address" },
              { indexed: false, name: "_value", type: "uint256" }
            ],
            name: "Approval",
            type: "event"
          }
        ]
      }
    },
    "v2.3": {
      mainNet: "0xa7135d0a62939501b5304a04bf00d1a9a22f6623",
      rinkebystaging: "0x1ca6b906917167366324aed6c6a708131136bea9",
      rinkeby: "0x1ca6b906917167366324aed6c6a708131136bea9",
      interfaces: {
        StandardBounties: [
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillmentId", type: "uint256" },
              { name: "_approverId", type: "uint256" },
              { name: "_tokenAmounts", type: "uint256[]" }
            ],
            name: "acceptFulfillment",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_approvers", type: "address[]" }
            ],
            name: "addApprovers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuers", type: "address[]" }
            ],
            name: "addIssuers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_approverId", type: "uint256" },
              { name: "_approver", type: "address" }
            ],
            name: "changeApprover",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuers", type: "address[]" },
              { name: "_approvers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_deadline", type: "uint256" }
            ],
            name: "changeBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_data", type: "string" }
            ],
            name: "changeData",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_deadline", type: "uint256" }
            ],
            name: "changeDeadline",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuerIdToChange", type: "uint256" },
              { name: "_newIssuer", type: "address" }
            ],
            name: "changeIssuer",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_amount", type: "uint256" }
            ],
            name: "contribute",
            outputs: [],
            payable: true,
            stateMutability: "payable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_amounts", type: "uint256[]" }
            ],
            name: "drainBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_approverId", type: "uint256" },
              { name: "_tokenAmounts", type: "uint256[]" }
            ],
            name: "fulfillAndAccept",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillers", type: "address[]" },
              { name: "_data", type: "string" }
            ],
            name: "fulfillBounty",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_issuers", type: "address[]" },
              { name: "_approvers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_deadline", type: "uint256" },
              { name: "_token", type: "address" },
              { name: "_tokenVersion", type: "uint256" },
              { name: "_depositAmount", type: "uint256" }
            ],
            name: "issueAndContribute",
            outputs: [{ name: "", type: "uint256" }],
            payable: true,
            stateMutability: "payable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_issuers", type: "address[]" },
              { name: "_approvers", type: "address[]" },
              { name: "_data", type: "string" },
              { name: "_deadline", type: "uint256" },
              { name: "_token", type: "address" },
              { name: "_tokenVersion", type: "uint256" }
            ],
            name: "issueBounty",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_data", type: "string" }
            ],
            name: "performAction",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_contributionId", type: "uint256" }
            ],
            name: "refundContribution",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_contributionIds", type: "uint256[]" }
            ],
            name: "refundContributions",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_contributionIds", type: "uint256[]" }
            ],
            name: "refundMyContributions",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_approvers", type: "address[]" }
            ],
            name: "replaceApprovers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_issuerId", type: "uint256" },
              { name: "_issuers", type: "address[]" }
            ],
            name: "replaceIssuers",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [{ name: "_relayer", type: "address" }],
            name: "setMetaTxRelayer",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_sender", type: "address" },
              { name: "_bountyId", type: "uint256" },
              { name: "_fulfillmentId", type: "uint256" },
              { name: "_fulfillers", type: "address[]" },
              { name: "_data", type: "string" }
            ],
            name: "updateFulfillment",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          { inputs: [], payable: false, stateMutability: "nonpayable", type: "constructor" },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_creator", type: "address" },
              { indexed: false, name: "_issuers", type: "address[]" },
              { indexed: false, name: "_approvers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" },
              { indexed: false, name: "_deadline", type: "uint256" },
              { indexed: false, name: "_token", type: "address" },
              { indexed: false, name: "_tokenVersion", type: "uint256" }
            ],
            name: "BountyIssued",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_contributionId", type: "uint256" },
              { indexed: false, name: "_contributor", type: "address" },
              { indexed: false, name: "_amount", type: "uint256" }
            ],
            name: "ContributionAdded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_contributionId", type: "uint256" }
            ],
            name: "ContributionRefunded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_issuer", type: "address" },
              { indexed: false, name: "_contributionIds", type: "uint256[]" }
            ],
            name: "ContributionsRefunded",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_issuer", type: "address" },
              { indexed: false, name: "_amounts", type: "uint256[]" }
            ],
            name: "BountyDrained",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfiller", type: "address" },
              { indexed: false, name: "_data", type: "string" }
            ],
            name: "ActionPerformed",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" },
              { indexed: false, name: "_fulfillers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" },
              { indexed: false, name: "_submitter", type: "address" }
            ],
            name: "BountyFulfilled",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" },
              { indexed: false, name: "_fulfillers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" }
            ],
            name: "FulfillmentUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_fulfillmentId", type: "uint256" },
              { indexed: false, name: "_approver", type: "address" },
              { indexed: false, name: "_tokenAmounts", type: "uint256[]" }
            ],
            name: "FulfillmentAccepted",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_issuers", type: "address[]" },
              { indexed: false, name: "_approvers", type: "address[]" },
              { indexed: false, name: "_data", type: "string" },
              { indexed: false, name: "_deadline", type: "uint256" }
            ],
            name: "BountyChanged",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_issuers", type: "address[]" }
            ],
            name: "BountyIssuersUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_approvers", type: "address[]" }
            ],
            name: "BountyApproversUpdated",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_data", type: "string" }
            ],
            name: "BountyDataChanged",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: false, name: "_bountyId", type: "uint256" },
              { indexed: false, name: "_changer", type: "address" },
              { indexed: false, name: "_deadline", type: "uint256" }
            ],
            name: "BountyDeadlineChanged",
            type: "event"
          },
          {
            constant: true,
            inputs: [{ name: "", type: "uint256" }],
            name: "bounties",
            outputs: [
              { name: "deadline", type: "uint256" },
              { name: "token", type: "address" },
              { name: "tokenVersion", type: "uint256" },
              { name: "balance", type: "uint256" },
              { name: "hasPaidOut", type: "bool" }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "callStarted",
            outputs: [{ name: "", type: "bool" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_bountyId", type: "uint256" }],
            name: "getBounty",
            outputs: [
              {
                components: [
                  { name: "issuers", type: "address[]" },
                  { name: "approvers", type: "address[]" },
                  { name: "deadline", type: "uint256" },
                  { name: "token", type: "address" },
                  { name: "tokenVersion", type: "uint256" },
                  { name: "balance", type: "uint256" },
                  { name: "hasPaidOut", type: "bool" },
                  {
                    components: [
                      { name: "fulfillers", type: "address[]" },
                      { name: "submitter", type: "address" }
                    ],
                    name: "fulfillments",
                    type: "tuple[]"
                  },
                  {
                    components: [
                      { name: "contributor", type: "address" },
                      { name: "amount", type: "uint256" },
                      { name: "refunded", type: "bool" }
                    ],
                    name: "contributions",
                    type: "tuple[]"
                  }
                ],
                name: "",
                type: "tuple"
              }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "metaTxRelayer",
            outputs: [{ name: "", type: "address" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "numBounties",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "owner",
            outputs: [{ name: "", type: "address" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [
              { name: "", type: "uint256" },
              { name: "", type: "uint256" }
            ],
            name: "tokenBalances",
            outputs: [{ name: "", type: "bool" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          }
        ],
        HumanStandardToken: [
          {
            constant: true,
            inputs: [],
            name: "name",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_spender", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "approve",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "totalSupply",
            outputs: [{ name: "", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_from", type: "address" },
              { name: "_to", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "transferFrom",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "decimals",
            outputs: [{ name: "", type: "uint8" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "version",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [{ name: "_owner", type: "address" }],
            name: "balanceOf",
            outputs: [{ name: "balance", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "symbol",
            outputs: [{ name: "", type: "string" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_to", type: "address" },
              { name: "_value", type: "uint256" }
            ],
            name: "transfer",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              { name: "_spender", type: "address" },
              { name: "_value", type: "uint256" },
              { name: "_extraData", type: "bytes" }
            ],
            name: "approveAndCall",
            outputs: [{ name: "success", type: "bool" }],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [
              { name: "_owner", type: "address" },
              { name: "_spender", type: "address" }
            ],
            name: "allowance",
            outputs: [{ name: "remaining", type: "uint256" }],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            inputs: [
              { name: "_initialAmount", type: "uint256" },
              { name: "_tokenName", type: "string" },
              { name: "_decimalUnits", type: "uint8" },
              { name: "_tokenSymbol", type: "string" }
            ],
            payable: false,
            stateMutability: "nonpayable",
            type: "constructor"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: true, name: "_from", type: "address" },
              { indexed: true, name: "_to", type: "address" },
              { indexed: false, name: "_value", type: "uint256" }
            ],
            name: "Transfer",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              { indexed: true, name: "_owner", type: "address" },
              { indexed: true, name: "_spender", type: "address" },
              { indexed: false, name: "_value", type: "uint256" }
            ],
            name: "Approval",
            type: "event"
          }
        ]
      }
    },
    "v2.4": {
      mainNet: "0x51598ae36102010feca5322098b22dd5b773428b",
      rinkebystaging: "0x6ac6baf770b3ffe2ddb3c5797e47c17cebef2ec4",
      rinkeby: "0x6ac6baf770b3ffe2ddb3c5797e47c17cebef2ec4",
      interfaces: {
        StandardBounties: [
          {
            "inputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "constructor"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address",
                "name": "_fulfiller",
                "type": "address"
              },
              {
                "indexed": false,
                "internalType": "string",
                "name": "_data",
                "type": "string"
              }
            ],
            "name": "ActionPerformed",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address",
                "name": "_changer",
                "type": "address"
              },
              {
                "indexed": false,
                "internalType": "address[]",
                "name": "_approvers",
                "type": "address[]"
              }
            ],
            "name": "BountyApproversUpdated",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address",
                "name": "_changer",
                "type": "address"
              },
              {
                "indexed": false,
                "internalType": "address payable[]",
                "name": "_issuers",
                "type": "address[]"
              },
              {
                "indexed": false,
                "internalType": "address payable[]",
                "name": "_approvers",
                "type": "address[]"
              },
              {
                "indexed": false,
                "internalType": "string",
                "name": "_data",
                "type": "string"
              },
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_deadline",
                "type": "uint256"
              }
            ],
            "name": "BountyChanged",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address",
                "name": "_changer",
                "type": "address"
              },
              {
                "indexed": false,
                "internalType": "string",
                "name": "_data",
                "type": "string"
              }
            ],
            "name": "BountyDataChanged",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address",
                "name": "_changer",
                "type": "address"
              },
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_deadline",
                "type": "uint256"
              }
            ],
            "name": "BountyDeadlineChanged",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address",
                "name": "_issuer",
                "type": "address"
              },
              {
                "indexed": false,
                "internalType": "uint256[]",
                "name": "_amounts",
                "type": "uint256[]"
              }
            ],
            "name": "BountyDrained",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_fulfillmentId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address payable[]",
                "name": "_fulfillers",
                "type": "address[]"
              },
              {
                "indexed": false,
                "internalType": "string",
                "name": "_data",
                "type": "string"
              },
              {
                "indexed": false,
                "internalType": "address",
                "name": "_submitter",
                "type": "address"
              }
            ],
            "name": "BountyFulfilled",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address payable",
                "name": "_creator",
                "type": "address"
              },
              {
                "indexed": false,
                "internalType": "address payable[]",
                "name": "_issuers",
                "type": "address[]"
              },
              {
                "indexed": false,
                "internalType": "address[]",
                "name": "_approvers",
                "type": "address[]"
              },
              {
                "indexed": false,
                "internalType": "string",
                "name": "_data",
                "type": "string"
              },
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_deadline",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address",
                "name": "_token",
                "type": "address"
              },
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_tokenVersion",
                "type": "uint256"
              }
            ],
            "name": "BountyIssued",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address",
                "name": "_changer",
                "type": "address"
              },
              {
                "indexed": false,
                "internalType": "address payable[]",
                "name": "_issuers",
                "type": "address[]"
              }
            ],
            "name": "BountyIssuersUpdated",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_contributionId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address payable",
                "name": "_contributor",
                "type": "address"
              },
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
              }
            ],
            "name": "ContributionAdded",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_contributionId",
                "type": "uint256"
              }
            ],
            "name": "ContributionRefunded",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address",
                "name": "_issuer",
                "type": "address"
              },
              {
                "indexed": false,
                "internalType": "uint256[]",
                "name": "_contributionIds",
                "type": "uint256[]"
              }
            ],
            "name": "ContributionsRefunded",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_fulfillmentId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address",
                "name": "_approver",
                "type": "address"
              },
              {
                "indexed": false,
                "internalType": "uint256[]",
                "name": "_tokenAmounts",
                "type": "uint256[]"
              }
            ],
            "name": "FulfillmentAccepted",
            "type": "event"
          },
          {
            "anonymous": false,
            "inputs": [
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "uint256",
                "name": "_fulfillmentId",
                "type": "uint256"
              },
              {
                "indexed": false,
                "internalType": "address payable[]",
                "name": "_fulfillers",
                "type": "address[]"
              },
              {
                "indexed": false,
                "internalType": "string",
                "name": "_data",
                "type": "string"
              }
            ],
            "name": "FulfillmentUpdated",
            "type": "event"
          },
          {
            "constant": true,
            "inputs": [
              {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
              }
            ],
            "name": "bounties",
            "outputs": [
              {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
              },
              {
                "internalType": "address",
                "name": "token",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "tokenVersion",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "balance",
                "type": "uint256"
              },
              {
                "internalType": "bool",
                "name": "hasPaidOut",
                "type": "bool"
              }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
          },
          {
            "constant": true,
            "inputs": [],
            "name": "callStarted",
            "outputs": [
              {
                "internalType": "bool",
                "name": "",
                "type": "bool"
              }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
          },
          {
            "constant": true,
            "inputs": [],
            "name": "metaTxRelayer",
            "outputs": [
              {
                "internalType": "address",
                "name": "",
                "type": "address"
              }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
          },
          {
            "constant": true,
            "inputs": [],
            "name": "numBounties",
            "outputs": [
              {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
              }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
          },
          {
            "constant": true,
            "inputs": [],
            "name": "owner",
            "outputs": [
              {
                "internalType": "address",
                "name": "",
                "type": "address"
              }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
          },
          {
            "constant": true,
            "inputs": [
              {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
              }
            ],
            "name": "tokenBalances",
            "outputs": [
              {
                "internalType": "bool",
                "name": "",
                "type": "bool"
              }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_relayer",
                "type": "address"
              }
            ],
            "name": "setMetaTxRelayer",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address payable",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "address payable[]",
                "name": "_issuers",
                "type": "address[]"
              },
              {
                "internalType": "address[]",
                "name": "_approvers",
                "type": "address[]"
              },
              {
                "internalType": "string",
                "name": "_data",
                "type": "string"
              },
              {
                "internalType": "uint256",
                "name": "_deadline",
                "type": "uint256"
              },
              {
                "internalType": "address",
                "name": "_token",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_tokenVersion",
                "type": "uint256"
              }
            ],
            "name": "issueBounty",
            "outputs": [
              {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
              }
            ],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address payable",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "address payable[]",
                "name": "_issuers",
                "type": "address[]"
              },
              {
                "internalType": "address[]",
                "name": "_approvers",
                "type": "address[]"
              },
              {
                "internalType": "string",
                "name": "_data",
                "type": "string"
              },
              {
                "internalType": "uint256",
                "name": "_deadline",
                "type": "uint256"
              },
              {
                "internalType": "address",
                "name": "_token",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_tokenVersion",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_depositAmount",
                "type": "uint256"
              }
            ],
            "name": "issueAndContribute",
            "outputs": [
              {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
              }
            ],
            "payable": true,
            "stateMutability": "payable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address payable",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
              }
            ],
            "name": "contribute",
            "outputs": [],
            "payable": true,
            "stateMutability": "payable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_contributionId",
                "type": "uint256"
              }
            ],
            "name": "refundContribution",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256[]",
                "name": "_contributionIds",
                "type": "uint256[]"
              }
            ],
            "name": "refundMyContributions",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_issuerId",
                "type": "uint256"
              },
              {
                "internalType": "uint256[]",
                "name": "_contributionIds",
                "type": "uint256[]"
              }
            ],
            "name": "refundContributions",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address payable",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_issuerId",
                "type": "uint256"
              },
              {
                "internalType": "uint256[]",
                "name": "_amounts",
                "type": "uint256[]"
              }
            ],
            "name": "drainBounty",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "string",
                "name": "_data",
                "type": "string"
              }
            ],
            "name": "performAction",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "address payable[]",
                "name": "_fulfillers",
                "type": "address[]"
              },
              {
                "internalType": "string",
                "name": "_data",
                "type": "string"
              }
            ],
            "name": "fulfillBounty",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_fulfillmentId",
                "type": "uint256"
              },
              {
                "internalType": "address payable[]",
                "name": "_fulfillers",
                "type": "address[]"
              },
              {
                "internalType": "string",
                "name": "_data",
                "type": "string"
              }
            ],
            "name": "updateFulfillment",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_fulfillmentId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_approverId",
                "type": "uint256"
              },
              {
                "internalType": "uint256[]",
                "name": "_tokenAmounts",
                "type": "uint256[]"
              }
            ],
            "name": "acceptFulfillment",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "address payable[]",
                "name": "_fulfillers",
                "type": "address[]"
              },
              {
                "internalType": "string",
                "name": "_data",
                "type": "string"
              },
              {
                "internalType": "uint256",
                "name": "_approverId",
                "type": "uint256"
              },
              {
                "internalType": "uint256[]",
                "name": "_tokenAmounts",
                "type": "uint256[]"
              }
            ],
            "name": "fulfillAndAccept",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_issuerId",
                "type": "uint256"
              },
              {
                "internalType": "address payable[]",
                "name": "_issuers",
                "type": "address[]"
              },
              {
                "internalType": "address payable[]",
                "name": "_approvers",
                "type": "address[]"
              },
              {
                "internalType": "string",
                "name": "_data",
                "type": "string"
              },
              {
                "internalType": "uint256",
                "name": "_deadline",
                "type": "uint256"
              }
            ],
            "name": "changeBounty",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_issuerId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_issuerIdToChange",
                "type": "uint256"
              },
              {
                "internalType": "address payable",
                "name": "_newIssuer",
                "type": "address"
              }
            ],
            "name": "changeIssuer",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_issuerId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_approverId",
                "type": "uint256"
              },
              {
                "internalType": "address payable",
                "name": "_approver",
                "type": "address"
              }
            ],
            "name": "changeApprover",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_issuerId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_issuerIdToChange",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_approverIdToChange",
                "type": "uint256"
              },
              {
                "internalType": "address payable",
                "name": "_issuer",
                "type": "address"
              }
            ],
            "name": "changeIssuerAndApprover",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_issuerId",
                "type": "uint256"
              },
              {
                "internalType": "string",
                "name": "_data",
                "type": "string"
              }
            ],
            "name": "changeData",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_issuerId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_deadline",
                "type": "uint256"
              }
            ],
            "name": "changeDeadline",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_issuerId",
                "type": "uint256"
              },
              {
                "internalType": "address payable[]",
                "name": "_issuers",
                "type": "address[]"
              }
            ],
            "name": "addIssuers",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": false,
            "inputs": [
              {
                "internalType": "address",
                "name": "_sender",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              },
              {
                "internalType": "uint256",
                "name": "_issuerId",
                "type": "uint256"
              },
              {
                "internalType": "address[]",
                "name": "_approvers",
                "type": "address[]"
              }
            ],
            "name": "addApprovers",
            "outputs": [],
            "payable": false,
            "stateMutability": "nonpayable",
            "type": "function"
          },
          {
            "constant": true,
            "inputs": [
              {
                "internalType": "uint256",
                "name": "_bountyId",
                "type": "uint256"
              }
            ],
            "name": "getBounty",
            "outputs": [
              {
                "components": [
                  {
                    "internalType": "address payable[]",
                    "name": "issuers",
                    "type": "address[]"
                  },
                  {
                    "internalType": "address[]",
                    "name": "approvers",
                    "type": "address[]"
                  },
                  {
                    "internalType": "uint256",
                    "name": "deadline",
                    "type": "uint256"
                  },
                  {
                    "internalType": "address",
                    "name": "token",
                    "type": "address"
                  },
                  {
                    "internalType": "uint256",
                    "name": "tokenVersion",
                    "type": "uint256"
                  },
                  {
                    "internalType": "uint256",
                    "name": "balance",
                    "type": "uint256"
                  },
                  {
                    "internalType": "bool",
                    "name": "hasPaidOut",
                    "type": "bool"
                  },
                  {
                    "components": [
                      {
                        "internalType": "address payable[]",
                        "name": "fulfillers",
                        "type": "address[]"
                      },
                      {
                        "internalType": "address",
                        "name": "submitter",
                        "type": "address"
                      }
                    ],
                    "internalType": "struct StandardBounties.Fulfillment[]",
                    "name": "fulfillments",
                    "type": "tuple[]"
                  },
                  {
                    "components": [
                      {
                        "internalType": "address payable",
                        "name": "contributor",
                        "type": "address"
                      },
                      {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                      },
                      {
                        "internalType": "bool",
                        "name": "refunded",
                        "type": "bool"
                      }
                    ],
                    "internalType": "struct StandardBounties.Contribution[]",
                    "name": "contributions",
                    "type": "tuple[]"
                  }
                ],
                "internalType": "struct StandardBounties.Bounty",
                "name": "",
                "type": "tuple"
              }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
          }
        ],
        HumanStandardToken: [
          {
            constant: true,
            inputs: [],
            name: "name",
            outputs: [
              {
                name: "",
                type: "string"
              }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "totalSupply",
            outputs: [
              {
                name: "",
                type: "uint256"
              }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "decimals",
            outputs: [
              {
                name: "",
                type: "uint8"
              }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "version",
            outputs: [
              {
                name: "",
                type: "string"
              }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: true,
            inputs: [],
            name: "symbol",
            outputs: [
              {
                name: "",
                type: "string"
              }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            inputs: [
              {
                name: "_initialAmount",
                type: "uint256"
              },
              {
                name: "_tokenName",
                type: "string"
              },
              {
                name: "_decimalUnits",
                type: "uint8"
              },
              {
                name: "_tokenSymbol",
                type: "string"
              }
            ],
            payable: false,
            stateMutability: "nonpayable",
            type: "constructor"
          },
          {
            anonymous: false,
            inputs: [
              {
                indexed: false,
                name: "_from",
                type: "address"
              },
              {
                indexed: false,
                name: "_to",
                type: "address"
              },
              {
                indexed: false,
                name: "_value",
                type: "uint256"
              }
            ],
            name: "Transfer",
            type: "event"
          },
          {
            anonymous: false,
            inputs: [
              {
                indexed: false,
                name: "_owner",
                type: "address"
              },
              {
                indexed: false,
                name: "_spender",
                type: "address"
              },
              {
                indexed: false,
                name: "_value",
                type: "uint256"
              }
            ],
            name: "Approval",
            type: "event"
          },
          {
            constant: false,
            inputs: [
              {
                name: "_to",
                type: "address"
              },
              {
                name: "_value",
                type: "uint256"
              }
            ],
            name: "transfer",
            outputs: [
              {
                name: "success",
                type: "bool"
              }
            ],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              {
                name: "_from",
                type: "address"
              },
              {
                name: "_to",
                type: "address"
              },
              {
                name: "_value",
                type: "uint256"
              }
            ],
            name: "transferFrom",
            outputs: [
              {
                name: "success",
                type: "bool"
              }
            ],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [
              {
                name: "_owner",
                type: "address"
              }
            ],
            name: "balanceOf",
            outputs: [
              {
                name: "balance",
                type: "uint256"
              }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          },
          {
            constant: false,
            inputs: [
              {
                name: "_spender",
                type: "address"
              },
              {
                name: "_value",
                type: "uint256"
              }
            ],
            name: "approve",
            outputs: [
              {
                name: "success",
                type: "bool"
              }
            ],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
          },
          {
            constant: true,
            inputs: [
              {
                name: "_owner",
                type: "address"
              },
              {
                name: "_spender",
                type: "address"
              }
            ],
            name: "allowance",
            outputs: [
              {
                name: "remaining",
                type: "uint256"
              }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
          }
        ]
      }
    }
  }
};

export default contract;
