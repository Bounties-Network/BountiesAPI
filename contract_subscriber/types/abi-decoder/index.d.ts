declare module "abi-decoder" {
  import eth from "web3/eth";
  export function addABI(contract: eth["Contract"]): any;
  export function decodeMethod(method: string): any;
}
