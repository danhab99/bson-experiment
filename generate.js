const BSON = require("bson");
const Long = BSON.Long;
const fs = require("fs");

console.log("-----------------------");

// Serialize a document
const doc = {
  abcd: 1000000,
  somekindastring: "asdfasdf",
  number: 99,
  nestedDoc: {
    a: 11,
  },
};
const data = BSON.serialize(doc);

console.log(
  "data:",
  [...Array(data.length).keys()]
    .map((i) => i.toString() + ": " + data[i].toString(16))
    .join("\n")
);

fs.writeFile("test.bson", data, () => {});
