let concurrentStart = async function () {
    console.log('==CONCURRENT START with await==');
    const slow = resolveAfter2Seconds();
    const fast = resolveAfter1Second();
    console.log(await slow);
    console.log(await fast);
}
setTimeout(concurrentStart, 4000);

// ==CONCURRENT START with await==
// starting slow promise
// starting fast promise
// fast promise is done      (after 1s)
// slow promise is done      (after 2s)
// slow                      (after 2s)
// fast                      (immediately after slow)
