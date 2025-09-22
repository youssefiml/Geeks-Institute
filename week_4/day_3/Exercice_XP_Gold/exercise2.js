function keysAndValues(obj) {
  const keys = Object.keys(obj).sort();
  const values = keys.map(key => obj[key]);

  return [keys, values];
}

console.log(keysAndValues({ a: 1, b: 2, c: 3 }));

console.log(keysAndValues({ a: "Samsung", b: "OpenAi", c: "Google" }));

console.log(keysAndValues({ key1: true, key2: false, key3: undefined }));