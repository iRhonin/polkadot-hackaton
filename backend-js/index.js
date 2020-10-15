const { ApiPromise, WsProvider } = require("@polkadot/api");

async function main() {
  const api = await ApiPromise.create();

  let blockHash = process.argv.slice(2);

  if (blockHash.length === 0) {
    blockHash = await api.rpc.chain.getFinalizedHead();
  } else if (blockHash.length == 1) {
    blockHash = blockHash[0];
  } else {
    return -1;
  }

  const block = await api.rpc.chain.getBlock(blockHash);
  console.log(JSON.stringify(block, null, 2));
}

main()
  .catch(console.error)
  .finally(() => process.exit());
